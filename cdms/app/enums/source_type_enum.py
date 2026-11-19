from enum import StrEnum


class SourceTypeEnum(StrEnum):
    POLLING = "POLLING"
    WEBHOOK = "WEBHOOK"
    EXCEL = "EXCEL"
