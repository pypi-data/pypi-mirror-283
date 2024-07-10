import os

import leo_station_keeping
import numpy as np
from leo_station_keeping import Axis, SolarArrayFace

from fds.constants import EARTH_RADIUS
from fds.models.orbital_state import OrbitalState
from fds.models.spacecraft import SpacecraftSphere, SpacecraftBox
from fds.models.station_keeping.requests import StationKeepingOutputRequest, EphemeridesRequest, \
    SpacecraftStatesRequest, ThrustEphemeridesRequest
from fds.models.station_keeping.result import ResultStationKeeping
from fds.models.station_keeping.strategy import StationKeepingStrategy
from fds.models.station_keeping.tolerance import Tolerance
from fds.utils.dates import datetime_to_iso_string
from fds.utils.log import log_and_raise


class LeoStationKeeping:
    ResultType = ResultStationKeeping
    URL: str = "http://numerical-leo-station-keeping.exoops.37.59.31.223.sslip.io/"

    def __init__(
            self,
            initial_orbital_state: OrbitalState,
            maximum_duration: int,
            tolerance: Tolerance,
            output_requests: list[StationKeepingOutputRequest],
            strategy: StationKeepingStrategy = None,
            drag_lift_ratio: float = 0.0,
            srp_absorption_coefficient: float = 1.0,
            average_on_board_power: float = 50.0,
            nametag: str = None
    ):
        """
        Args:
            initial_orbital_state (OrbitalState): The initial orbital state object.
            maximum_duration (int): The maximum duration of the maneuver.
            tolerance (Tolerance): The tolerance object (SMA or ALONG_TRACK).
            output_requests (list[StationKeepingOutputRequest]): The list of output requests.
            strategy (StationKeepingStrategy): The strategy object. If None, the default strategy is used.
            drag_lift_ratio (float): The drag lift ratio. Defaults to 0.5.
            srp_absorption_coefficient (float): The SRP absorption coefficient. Defaults to 1.0.
            average_on_board_power (float): The average on board power. Defaults to 50.0.
            nametag (str): The name of the use case. Defaults to None.
        """
        self._initial_orbital_state = initial_orbital_state
        self._maximum_duration = maximum_duration
        self._tolerance = tolerance
        self._strategy = strategy
        self._drag_lift_ratio = drag_lift_ratio
        self._average_on_board_power = average_on_board_power
        self._srp_absorption_coefficient = srp_absorption_coefficient
        self._output_requests = output_requests
        self._nametag = nametag

        self._response = None
        self._result = None
        self._microservice_configuration = self._get_microservice_configuration()
        self._request = self._prepare_request()

    @property
    def initial_orbital_state(self) -> OrbitalState:
        return self._initial_orbital_state

    @property
    def start_date(self):
        return self.initial_orbital_state.date

    @property
    def initial_altitude(self) -> float:
        return self.initial_orbital_state.osculating_orbit.orbital_elements.SMA - EARTH_RADIUS / 1e3

    @property
    def tolerance(self) -> Tolerance:
        return self._tolerance

    @property
    def maximum_duration(self) -> int:
        return self._maximum_duration

    @property
    def strategy(self) -> StationKeepingStrategy:
        return self._strategy

    @property
    def drag_lift_ratio(self) -> float:
        return self._drag_lift_ratio

    @property
    def average_on_board_power(self) -> float:
        return self._average_on_board_power

    @property
    def srp_absorption_coefficient(self) -> float:
        return self._srp_absorption_coefficient

    @property
    def output_requests(self) -> list[StationKeepingOutputRequest]:
        return self._output_requests

    @property
    def response(self) -> leo_station_keeping.NumericalLeoStationKeepingResponse:
        return self._response

    @property
    def request(self) -> leo_station_keeping.NumericalLeoStationKeepingRequest:
        return self._request

    @property
    def result(self) -> ResultStationKeeping:
        return self._result

    @property
    def microservice_configuration(self) -> leo_station_keeping.Configuration:
        return self._microservice_configuration

    @property
    def nametag(self) -> str:
        return self._nametag

    def _get_microservice_configuration(self):
        url = os.environ.get("SK_MS_HOST")
        if url is None:
            url = self.URL
        return leo_station_keeping.Configuration(host=url)

    def _prepare_request(self):
        # Map orbit
        orbit = self._map_orbit()

        # Map platform
        platform = self._map_platform()

        # Map spacecraft geometry
        spacecraft_geometry = self._map_spacecraft_geometry()

        # Map propulsion system
        propulsion_system = self._map_propulsion_system()

        # Map perturbations
        perturbations = self._map_perturbations()

        # Map tolerance
        tolerance = self.tolerance.to_microservice_format()

        # Map strategy
        strategy = None
        if self.strategy is not None:
            strategy = self.strategy.to_microservice_format()

        inputs = leo_station_keeping.NumericalLeoStationKeepingRequestInputs(
            mission_date_time=datetime_to_iso_string(self.start_date),
            maximum_duration=self.maximum_duration,
            initial_orbit=orbit,
            propulsion_system=propulsion_system,
            platform=platform,
            spacecraft_geometry=spacecraft_geometry,
            tolerance=tolerance,
            perturbations=perturbations,
            target_date_definition_type="DURATION",
            custom_maneuvering_strategy=strategy
        )

        # Outputs
        output_requests = self._map_output_requests()

        return leo_station_keeping.NumericalLeoStationKeepingRequest(
            inputs=inputs,
            outputs=output_requests
        )

    def _map_output_requests(self):
        requests = {}
        for output_request in self.output_requests:
            if isinstance(output_request, EphemeridesRequest):
                requests["orbital_ephemerides"] = output_request.to_microservice_format()
            elif isinstance(output_request, SpacecraftStatesRequest):
                requests["spacecraft_states"] = output_request.to_microservice_format()
            elif isinstance(output_request, ThrustEphemeridesRequest):
                requests["thrust_ephemerides"] = output_request.to_microservice_format()
            else:
                raise ValueError("Output request not recognized.")
        return leo_station_keeping.NumericalLeoStationKeepingRequestOutputs(**requests)

    def _map_perturbations(self):
        spacecraft = self.initial_orbital_state.spacecraft
        model = self.initial_orbital_state.propagation_context.model

        perturbations = []
        for pert in model.perturbations:
            match pert.value:
                case "DRAG":
                    perturbations.append(
                        leo_station_keeping.DragPerturbation(
                            type="DRAG",
                            drag_coefficient=spacecraft.drag_coefficient,
                            lift_ratio=self.drag_lift_ratio,
                            custom_solar_flux=model.solar_flux
                        ))
                case "SRP":
                    perturbations.append(
                        leo_station_keeping.SrpPerturbation(
                            type="SRP",
                            absorption_coefficient=self.srp_absorption_coefficient,
                            reflection_coefficient=spacecraft.reflectivity_coefficient,
                        ))
                case "EARTH_POTENTIAL":
                    perturbations.append(leo_station_keeping.EarthPotentialPerturbation(
                        type="EARTH_POTENTIAL",
                        custom_maximum_degree=model.earth_potential_deg,
                        custom_maximum_order=model.earth_potential_ord
                    ))
                case "THIRD_BODY":
                    perturbations.append(leo_station_keeping.ThirdBodyPerturbation(
                        type="THIRD_BODY",
                    ))
        return perturbations if len(perturbations) > 0 else None

    def _map_propulsion_system(self):
        spacecraft = self.initial_orbital_state.spacecraft
        propulsion_system = leo_station_keeping.PropulsionSystem()
        propulsion_system.type = spacecraft.propulsion_kind
        propulsion_system.isp = spacecraft.thruster.isp
        propulsion_system.power = spacecraft.thruster.power
        propulsion_system.thrust = spacecraft.thruster.thrust
        propulsion_system.standby_power = spacecraft.thruster.stand_by_power
        propulsion_system.warm_up_power = spacecraft.thruster.warm_up_power
        propulsion_system.warm_up_duration = spacecraft.thruster.warm_up_duration
        propulsion_system.propellant_mass = spacecraft.thruster.propellant_mass
        propulsion_system.total_mass = spacecraft.thruster.wet_mass
        propulsion_system.propellant_capacity_choice = "PROPELLANT"
        return propulsion_system

    def _map_spacecraft_geometry(self):
        spacecraft = self.initial_orbital_state.spacecraft
        spacecraft_geometry = None
        if isinstance(spacecraft, SpacecraftSphere):
            spacecraft_geometry = leo_station_keeping.SphericalSpacecraftGeometry()
            spacecraft_geometry.spherical_cross_section = spacecraft.cross_section  # Compute for box
            spacecraft_geometry.type = "SPHERICAL"
        elif isinstance(spacecraft, SpacecraftBox):

            # Map solar array
            if spacecraft.solar_array.surface is None or spacecraft.solar_array.surface == 0:
                raise ValueError("The surface of the solar array must be defined. Please initialise the solar array"
                                 " with a surface value.")
            solar_array = self._map_solar_array()

            spacecraft_geometry = leo_station_keeping.BoxSpacecraftGeometry()
            spacecraft_geometry.dimensions = leo_station_keeping.SpacecraftGeometryDimension(
                x=spacecraft.length.x,
                y=spacecraft.length.y,
                z=spacecraft.length.z
            )
            spacecraft_geometry.thruster_axis = Axis(
                x=spacecraft.thruster.axis_in_satellite_frame[0],
                y=spacecraft.thruster.axis_in_satellite_frame[1],
                z=spacecraft.thruster.axis_in_satellite_frame[2]
            )
            spacecraft_geometry.solar_array = solar_array
            spacecraft_geometry.type = "BOX"
        return spacecraft_geometry

    def _map_solar_array(self):
        def _map_solar_array_body():
            faces = None
            if spacecraft.solar_array.satellite_faces is not None:
                faces = [SolarArrayFace(f.value) for f in spacecraft.solar_array.satellite_faces]
            return leo_station_keeping.BodySolarArray(faces=faces, type=spacecraft.solar_array.kind.value)

        def _map_solar_array_deployable_fixed():
            return leo_station_keeping.DeployableFixedSolarArray(
                normal_direction=Axis(x=spacecraft.solar_array.normal_in_satellite_frame[0],
                                      y=spacecraft.solar_array.normal_in_satellite_frame[1],
                                      z=spacecraft.solar_array.normal_in_satellite_frame[2]),
                surface=spacecraft.solar_array.surface,
                type=spacecraft.solar_array.kind.value
            )

        def _map_solar_array_deployable_rotating():
            return leo_station_keeping.DeployableRotatingSolarArray(
                rotation_axis=Axis(x=spacecraft.solar_array.axis_in_satellite_frame[0],
                                   y=spacecraft.solar_array.axis_in_satellite_frame[1],
                                   z=spacecraft.solar_array.axis_in_satellite_frame[2]),
                surface=spacecraft.solar_array.surface,
                type=spacecraft.solar_array.kind.value
            )

        spacecraft = self.initial_orbital_state.spacecraft
        match spacecraft.solar_array.kind:
            case spacecraft.solar_array.Kind.BODY:
                return _map_solar_array_body()
            case spacecraft.solar_array.Kind.DEPLOYABLE_FIXED:
                return _map_solar_array_deployable_fixed()
            case spacecraft.solar_array.Kind.DEPLOYABLE_ROTATING:
                return _map_solar_array_deployable_rotating()

    def _map_platform(self):
        spacecraft = self.initial_orbital_state.spacecraft
        platform = leo_station_keeping.Platform()
        platform.mass = spacecraft.platform_mass
        platform.on_board_average_power = self.average_on_board_power  # TODO: clarify this value
        return platform

    def _map_orbit(self):
        orbit = leo_station_keeping.Orbit()
        orbit_sdk = self.initial_orbital_state.mean_orbit
        orbit.inclination = np.radians(orbit_sdk.orbital_elements.INC)
        orbit.sma = orbit_sdk.orbital_elements.SMA * 1e3
        orbit.eccentricity = orbit_sdk.orbital_elements.ECC
        orbit.parameters = leo_station_keeping.EllipticalSmaEccentricityOrbitParameters()
        orbit.parameters.parameters_type = "ELLIPTICAL_SMA_ECC"

        orbit.advanced_parameters = leo_station_keeping.AdvancedOrbitParameters()
        orbit.advanced_parameters.orbit_date = datetime_to_iso_string(
            self.start_date)  # TODO: temporary fix to map the orbit date (instead of mission_date_time)
        orbit.advanced_parameters.ascending_node_type = "RAAN"
        orbit.advanced_parameters.raan = orbit_sdk.orbital_elements.RAAN
        orbit.advanced_parameters.anomaly_type = "TRUE"
        orbit.advanced_parameters.anomaly = orbit_sdk.orbital_elements.TA
        orbit.advanced_parameters.orbital_element_type = "MEAN"
        orbit.advanced_parameters.perigee_argument = orbit_sdk.orbital_elements.AOP
        return orbit

    def run(self):

        with leo_station_keeping.ApiClient(self.microservice_configuration) as api_client:
            api = leo_station_keeping.api.DefaultApi(api_client)
            response = api.compute_numerical_leo_station_keeping(self.request)
            if len(response.errors) > 0:
                msg = f"Computation terminated with errors : {response.errors[0].message}"
                log_and_raise(ValueError, msg)

        # Map the response to the Result object
        self._response = response
        self._result = self.ResultType.from_microservice_format(self.response, self.initial_orbital_state.date)
        return self
