import leo_station_keeping

from fds.utils.enum import EnumFromInput


class StationKeepingOutputRequest:
    def __init__(self, mean: bool, osculating: bool):
        self._mean = mean
        self._osculating = osculating

    @property
    def mean(self) -> bool:
        return self._mean

    @property
    def osculating(self) -> bool:
        return self._osculating


class EphemeridesRequest(StationKeepingOutputRequest):
    class EphemeridesType(EnumFromInput):
        KEPLERIAN = "KEPLERIAN"
        CARTESIAN = "CARTESIAN"

    def __init__(self, timestep: float, types: list[str | EphemeridesType], mean: bool, osculating: bool):
        super().__init__(mean, osculating)
        self._timestep = timestep
        self._types = [EphemeridesRequest.EphemeridesType.from_input(t) for t in types]

    @property
    def timestep(self) -> float:
        return self._timestep

    @property
    def types(self) -> list[str]:
        return self._types

    def to_microservice_format(self):
        return leo_station_keeping.NumericalLeoStationKeepingRequestOutputsOrbitalEphemerides(
            timestep=self.timestep,
            types=self.types,
            mean=self.mean,
            osculating=self.osculating
        )


class SpacecraftStatesRequest(StationKeepingOutputRequest):
    def __init__(self, mean: bool, osculating: bool):
        super().__init__(mean, osculating)

    def to_microservice_format(self):
        return leo_station_keeping.NumericalLeoStationKeepingRequestOutputsSpacecraftStates(
            mean=self.mean,
            osculating=self.osculating
        )


class ThrustEphemeridesRequest(StationKeepingOutputRequest):
    def __init__(self, mean: bool, osculating: bool):
        super().__init__(mean, osculating)

    def to_microservice_format(self):
        return leo_station_keeping.NumericalLeoStationKeepingRequestOutputsThrustEphemerides(
            mean=self.mean,
            osculating=self.osculating
        )
