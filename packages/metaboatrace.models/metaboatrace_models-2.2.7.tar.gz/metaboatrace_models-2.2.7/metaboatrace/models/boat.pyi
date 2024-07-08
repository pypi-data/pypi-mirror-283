from .stadium import StadiumTelCode as StadiumTelCode
from datetime import date
from enum import Enum
from pydantic import BaseModel, StrictInt as StrictInt

class MotorParts(Enum):
    ELECTRICAL_SYSTEM: int
    CARBURETOR: int
    PISTON: int
    PISTON_RING: int
    CYLINDER: int
    CRANKSHAFT: int
    GEAR_CASE: int
    CARRIER_BODY: int

class BoatPerformance(BaseModel):
    stadium_tel_code: StadiumTelCode
    recorded_date: date
    number: StrictInt
    quinella_rate: float | None
    trio_rate: float | None

class MotorPerformance(BaseModel):
    stadium_tel_code: StadiumTelCode
    recorded_date: date
    number: StrictInt
    quinella_rate: float | None
    trio_rate: float | None
