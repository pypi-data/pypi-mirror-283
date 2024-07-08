from datetime import date
from enum import Enum
from pydantic import BaseModel, StrictInt as StrictInt
from typing_extensions import Self

class StadiumTelCode(Enum):
    KIRYU: int
    TODA: int
    EDOGAWA: int
    HEIWAJIMA: int
    TAMAGAWA: int
    HAMANAKO: int
    GAMAGORI: int
    TOKONAME: int
    TSU: int
    MIKUNI: int
    BIWAKO: int
    SUMINOE: int
    AMAGASAKI: int
    NARUTO: int
    MARUGAME: int
    KOJIMA: int
    MIYAJIMA: int
    TOKUYAMA: int
    SHIMONOSEKI: int
    WAKAMATSU: int
    ASHIYA: int
    FUKUOKA: int
    KARATSU: int
    OMURA: int

class SeriesGrade(Enum):
    SG: int
    G1: int
    G2: int
    G3: int
    NO_GRADE: int
    @classmethod
    def from_string(cls, s: str) -> SeriesGrade: ...

class SeriesKind(Enum):
    UNCATEGORIZED: int
    ALL_LADIES: int
    VENUS: int
    ROOKIE: int
    SENIOR: int
    DOUBLE_WINNER: int
    TOURNAMENT: int

class Event(BaseModel):
    stadium_tel_code: StadiumTelCode
    starts_on: date
    days: StrictInt
    grade: SeriesGrade
    kind: SeriesKind
    title: str

class MotorRenewal(BaseModel):
    stadium_tel_code: StadiumTelCode
    date: date

class EventHoldingStatus(Enum):
    OPEN: str
    CANCELED: str
    POSTPONED: str

class EventHolding(BaseModel):
    stadium_tel_code: StadiumTelCode
    date: date | None
    status: EventHoldingStatus
    progress_day: int | None
    def validate_status_and_progress_day(self) -> Self: ...
