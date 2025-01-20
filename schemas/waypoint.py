# schemas/waypoint.py
from pydantic import BaseModel, Field, field_validator


class CoordinateBase(BaseModel):
    x: int
    y: int
    z: int


class CoordinateCreate(CoordinateBase):
    pass


class Coordinate(CoordinateBase):
    id: int

    class Config:
        orm_mode = True


class WaypointBase(BaseModel):
    name: str
    type: str
    color: int
    visibility: bool
    dimension: str
    file: str


class WaypointCreate(WaypointBase):
    coordinate_id: int


class Waypoint(WaypointBase):
    id: int
    coordinate: Coordinate

    class Config:
        orm_mode = True
