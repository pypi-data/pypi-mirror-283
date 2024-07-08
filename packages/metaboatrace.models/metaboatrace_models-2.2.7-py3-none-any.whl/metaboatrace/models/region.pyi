from enum import Enum

class Prefecture(Enum):
    HOKKAIDO: int
    AOMORI: int
    IWATE: int
    MIYAGI: int
    AKITA: int
    YAMAGATA: int
    FUKUSHIMA: int
    IBARAKI: int
    TOCHIGI: int
    GUNMA: int
    SAITAMA: int
    CHIBA: int
    TOKYO: int
    KANAGAWA: int
    NIIGATA: int
    TOYAMA: int
    ISHIKAWA: int
    FUKUI: int
    YAMANASHI: int
    NAGANO: int
    GIFU: int
    SHIZUOKA: int
    AICHI: int
    MIE: int
    SHIGA: int
    KYOTO: int
    OSAKA: int
    HYOGO: int
    NARA: int
    WAKAYAMA: int
    TOTTORI: int
    SHIMANE: int
    OKAYAMA: int
    HIROSHIMA: int
    YAMAGUCHI: int
    TOKUSHIMA: int
    KAGAWA: int
    EHIME: int
    KOCHI: int
    FUKUOKA: int
    SAGA: int
    NAGASAKI: int
    KUMAMOTO: int
    OITA: int
    MIYAZAKI: int
    KAGOSHIMA: int
    OKINAWA: int

class Branch(Enum):
    GUNMA: int
    SAITAMA: int
    TOKYO: int
    FUKUI: int
    SHIZUOKA: int
    AICHI: int
    MIE: int
    SHIGA: int
    OSAKA: int
    HYOGO: int
    OKAYAMA: int
    HIROSHIMA: int
    YAMAGUCHI: int
    TOKUSHIMA: int
    KAGAWA: int
    FUKUOKA: int
    SAGA: int
    NAGASAKI: int

class PrefectureFactory:
    @staticmethod
    def create(name: str) -> Prefecture: ...

class BranchFactory:
    @staticmethod
    def create(name: str) -> Branch: ...
