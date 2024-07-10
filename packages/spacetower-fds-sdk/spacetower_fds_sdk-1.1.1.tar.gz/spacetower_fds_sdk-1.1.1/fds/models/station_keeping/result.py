from dataclasses import dataclass
from datetime import datetime, UTC

from leo_station_keeping import NumericalLeoStationKeepingResponse, NumericalLeoStationKeepingResponseResults

from fds.models.actions import ActionFiring, AttitudeMode, ActionAttitude
from fds.models.orbits import Orbit
from fds.models.quaternion import Quaternion
from fds.models.roadmaps import RoadmapFromActions
from fds.utils.dates import convert_date_to_utc, DateRange
from fds.utils.log import log_and_raise


class ResultStationKeeping:
    @dataclass
    class Report:
        number_of_burns: int
        total_thrust_duration: float
        total_consumption: float
        total_delta_v: float
        thruster_mean_duty_cycle: float
        total_warmup_duty_cycle: float
        mean_burn_duration_estimation: float
        simulation_duration: float
        number_of_orbital_periods: int
        total_impulse: float
        final_duty_cycle: float
        maneuver_model: str
        final_orbit: Orbit | None

        @classmethod
        def create_from_api_results(cls, results: NumericalLeoStationKeepingResponseResults):
            return cls(
                number_of_burns=results.number_of_burns,
                total_thrust_duration=results.thrust_duration,
                total_consumption=results.used_propellant,
                total_delta_v=results.delta_v,
                thruster_mean_duty_cycle=results.thruster_mean_duty_cycle,
                total_warmup_duty_cycle=results.total_warmup_duty_cycle,
                mean_burn_duration_estimation=results.mean_burn_duration_estimation,
                simulation_duration=results.mission_duration,
                number_of_orbital_periods=results.number_of_periods,
                total_impulse=results.total_impulse,
                final_duty_cycle=results.final_duty_cycle,
                maneuver_model=results.maneuver_model,
                final_orbit=results.final_orbit
            )

    def __init__(
            self,
            report: Report,
            raw_ephemerides: list[list[float]],
            field_indexes: list[dict[str, int | str]],
            start_date: datetime,
            raw_spacecraft_states: dict | None = None,
    ):
        """
        Args:
            report (Report): The report object.
            raw_ephemerides (list[list[float]]): The raw ephemerides.
            field_indexes (list[dict[str, int | str]]): The field indexes.
            start_date (datetime): The start date of the use case.
            raw_spacecraft_states (dict): The raw spacecraft states data.
        """
        self._report = report
        self._raw_ephemerides = raw_ephemerides
        self._field_indexes = field_indexes
        self._start_date = convert_date_to_utc(start_date)
        self._raw_spacecraft_states = raw_spacecraft_states

    @property
    def report(self) -> Report:
        return self._report

    @property
    def raw_ephemerides(self) -> list[list[float]]:
        return self._raw_ephemerides

    @property
    def ephemerides_field_indexes(self) -> list[dict[str, int | str]]:
        return self._field_indexes

    @property
    def ephemerides_field_keys(self) -> list[str]:
        return [field["key"] for field in self.ephemerides_field_indexes]

    @property
    def raw_spacecraft_states(self) -> dict:
        return self._raw_spacecraft_states

    @property
    def start_date(self) -> datetime:
        return self._start_date

    @classmethod
    def from_microservice_format(cls, response: NumericalLeoStationKeepingResponse, start_date: datetime):
        return cls(
            report=cls.Report.create_from_api_results(response.results),
            raw_ephemerides=response.ephemerides,
            field_indexes=[r.to_dict() for r in response.field_indexes],
            raw_spacecraft_states=response.spacecraft_states.to_dict() if response.spacecraft_states else None,
            start_date=start_date,
        )

    def export_raw_ephemerides_data(self) -> list[dict]:
        res = []
        for eph in self.raw_ephemerides:
            line = {}
            for field_index in self.ephemerides_field_indexes:
                line[field_index["key"]] = eph[field_index["index"]]
            line["date"] = convert_date_to_utc(
                datetime.fromtimestamp(line.get("simulationDuration") + self.start_date.timestamp(), tz=UTC))
            res.append(line)
        return res

    def _export_ephemerides(self, prefix_list: str | list[str], remove_prefix: bool = True):
        if not isinstance(prefix_list, list):
            prefix_list = [prefix_list]

        def remove_prefix_if_present(key: str) -> str:
            for p in prefix_list:
                if key.startswith(p):
                    return key.replace(p, "")
            return key

        def update_key(key: str) -> str:
            if remove_prefix:
                return remove_prefix_if_present(key)
            return key

        raw = self.export_raw_ephemerides_data()

        keys = [key for key in raw[0].keys() if any([key.startswith(p) for p in prefix_list])]
        res = []
        for eph in raw:
            line = {update_key(key): eph[key] for key in keys}
            line["date"] = eph["date"]
            res.append(line)
        return res

    def export_keplerian_ephemerides_data(self) -> list[dict]:
        if not any(key.startswith("keplerian") for key in self.ephemerides_field_keys):
            msg = "Keplerian ephemerides are not available."
            log_and_raise(ValueError, msg)
        return self._export_ephemerides("keplerian")

    def export_state_error_ephemerides_data(self) -> list[dict]:
        if not any(key.startswith("positionError") for key in self.ephemerides_field_keys):
            msg = "State error ephemerides are not available."
            log_and_raise(ValueError, msg)
        return self._export_ephemerides(["positionError", "velocityError"], remove_prefix=False)

    def export_cartesian_ephemerides_data(self) -> list[dict]:
        if not any(key.startswith("cartesian") for key in self.ephemerides_field_keys):
            msg = "Cartesian ephemerides are not available."
            log_and_raise(ValueError, msg)
        return self._export_ephemerides("cartesian")

    def generate_maneuver_roadmap(self) -> RoadmapFromActions:
        """
        Generate a roadmap with the maneuvers performed during the station keeping. The roadmap will contain the
        quaternions and the firing dates.
        """
        if self.raw_spacecraft_states is None:
            msg = ("Impossible to generate a roadmap without raw spacecraft states. Add a SpacecraftStatesRequest to"
                   " the output requests.")
            log_and_raise(ValueError, msg)
        raw_firings_info = self.raw_spacecraft_states.get('thrusting')
        firing_date_ranges = [DateRange(start=firing.get('begin'), end=firing.get('end')) for firing in
                              raw_firings_info]

        quaternions_osculating = self._get_quaternions()

        # create roadmap with firing dates and attitude quaternions
        firing_actions = [ActionFiring.from_firing_date_range(
            firing_date_range,
            firing_attitude_mode=AttitudeMode.QUATERNION,
            post_firing_attitude_mode=AttitudeMode.QUATERNION
        ) for firing_date_range in firing_date_ranges]

        attitude_action = ActionAttitude(
            attitude_mode=AttitudeMode.QUATERNION,
            transition_date=quaternions_osculating[0].date,
            quaternions=quaternions_osculating
        )

        return RoadmapFromActions(actions=[attitude_action] + firing_actions)

    def _get_quaternions(self, kind: str = 'osculating'):
        raw_quaternions_osculating = self.raw_spacecraft_states.get(kind).get('attitude').get('rotation')
        raw_dates = self.raw_spacecraft_states.get('timestamps')
        quaternions_osculating = Quaternion.from_collections(raw_quaternions_osculating, raw_dates)
        date_map = {}
        # Create a map with the dates as key and the quaternions as value (multiple quaternions can have the same date)
        for q in quaternions_osculating:
            date_map.setdefault(q.date, []).append(q)
        quaternions = []
        for date, qs in date_map.items():
            if len(qs) == 1 or (len(qs) == 2 and qs[0] == qs[1]):
                # If there is only one quaternion or two quaternions that are the same, we keep only one
                quaternions.append(qs[0])
        return sorted(quaternions, key=lambda q: q.date)
