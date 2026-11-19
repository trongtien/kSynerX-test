from enum import Enum

from sqlalchemy import Enum as SQLEnum


def pg_enum(enum_cls: type[Enum], type_name: str) -> SQLEnum:
    return SQLEnum(
        enum_cls,
        name=type_name,
        create_type=False,
        values_callable=lambda members: [m.value for m in members],
    )
