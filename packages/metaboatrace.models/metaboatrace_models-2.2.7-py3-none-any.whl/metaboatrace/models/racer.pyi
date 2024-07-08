from .region import Branch as Branch, Prefecture as Prefecture
from _typeshed import Incomplete
from datetime import date
from enum import Enum
from pydantic import BaseModel, StrictInt as StrictInt

class Gender(Enum):
    MALE: int
    FEMALE: int

class RacerRank(Enum):
    A1: int
    A2: int
    B1: int
    B2: int
    @classmethod
    def from_string(cls, s: str) -> RacerRank: ...

class Racer(BaseModel):
    registration_number: StrictInt
    last_name: str
    first_name: str
    gender: Gender | None
    term: StrictInt | None
    birth_date: date | None
    height: StrictInt | None
    born_prefecture: Prefecture | None
    branch: Branch | None
    current_rating: RacerRank | None

class RacerCondition(BaseModel):
    recorded_on: date
    racer_registration_number: StrictInt
    weight: float
    adjust: float

class RacerPerformance(BaseModel):
    racer_registration_number: StrictInt
    aggregated_on: date
    rate_in_all_stadium: float
    rate_in_event_going_stadium: float

class EvaluationPeriodType(Enum):
    FIRST_HALF: int
    SECOND_HALF: int

class RacerRatingEvaluationTerm:
    FIRST_HALF_START_MONTH: int
    SECOND_HALF_START_MONTH: int
    year: Incomplete
    period_type: Incomplete
    def __init__(self, year: int, period_type: EvaluationPeriodType) -> None: ...
    def prev(self) -> RacerRatingEvaluationTerm: ...
    def next(self) -> RacerRatingEvaluationTerm: ...
