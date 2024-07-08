from .boat import MotorParts as MotorParts
from .stadium import StadiumTelCode as StadiumTelCode
from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, StrictInt as StrictInt
from typing import Literal

class Weather(Enum):
    FINE: int
    CLOUDY: int
    RAINY: int
    SNOWY: int
    TYPHOON: int
    FOG: int

class BettingMethod(Enum):
    TRIFECTA: int

class WinningTrick(Enum):
    NIGE: int
    SASHI: int
    MAKURI: int
    MAKURIZASHI: int
    NUKI: int
    MEGUMARE: int

class Disqualification(Enum):
    CAPSIZE: int
    FALL: int
    SINKING: int
    VIOLATION: int
    DISQUALIFICATION_AFTER_START: int
    ENGINE_STOP: int
    UNFINISHED: int
    REPAYMENT_OTHER_THAN_FLYING_AND_LATENESS: int
    FLYING: int
    LATENESS: int
    ABSENT: int

class _RaceIdentifier(BaseModel):
    race_holding_date: date
    stadium_tel_code: StadiumTelCode
    race_number: StrictInt

class _RaceEntryIdentifier(_RaceIdentifier):
    pit_number: StrictInt

class _BettingMixin(BaseModel):
    betting_method: BettingMethod
    betting_numbers: list[int]
    def validate_betting_numbers(cls, betting_numbers: list[int]) -> list[int]: ...

class RaceInformation(_RaceIdentifier):
    title: str
    number_of_laps: Literal[2, 3]
    deadline_at: datetime
    is_course_fixed: bool
    use_stabilizer: bool

class WeatherCondition(_RaceIdentifier):
    in_performance: bool
    weather: Weather
    wavelength: float | None
    wind_angle: float | None
    wind_velocity: float
    air_temperature: float
    water_temperature: float

class RaceEntry(_RaceEntryIdentifier):
    racer_registration_number: StrictInt
    is_absent: bool
    motor_number: StrictInt
    boat_number: StrictInt

class StartExhibitionRecord(_RaceEntryIdentifier):
    start_course: StrictInt
    start_time: float

class CircumferenceExhibitionRecord(_RaceEntryIdentifier):
    exhibition_time: float

class BoatSetting(_RaceEntryIdentifier):
    boat_number: int | None
    motor_number: int | None
    tilt: float | None
    is_new_propeller: bool | None
    motor_parts_exchanges: list[tuple[MotorParts, StrictInt]]

class Odds(_RaceIdentifier, _BettingMixin):
    ratio: float

class Payoff(_RaceIdentifier, _BettingMixin):
    amount: StrictInt

class RaceRecord(_RaceEntryIdentifier):
    start_course: StrictInt | None
    arrival: StrictInt | None
    total_time: float | None
    start_time: float | None
    winning_trick: WinningTrick | None
    disqualification: Disqualification | None
