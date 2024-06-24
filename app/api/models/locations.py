"""API models"""

from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.coordinate import Latitude, Longitude


class Location(BaseModel):
    name: str
    latitude: Latitude
    longitude: Longitude

    @property
    def point_coordinate(self):
        return f"POINT({self.latitude} {self.longitude})"


class LocationPublic(Location):
    model_config = ConfigDict(from_attributes=True)

    id: int


class LocationsPublic(BaseModel):
    data: list[LocationPublic]
    count: int


class LocationPayload(Location):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=3, max_length=45)
