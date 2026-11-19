from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.utils.format_str import FormatString


@dataclass(frozen=True, slots=True)
class CategoryItemBuilder(FormatString):
    category_code: str
    category_name: str | None = None

    def __post_init__(self) -> None:
        code = self.tranform_text(self.category_code)
        if code is None:
            raise ValueError("categoryCode must not be empty")

        name = self.tranform_text(self.category_name)

        object.__setattr__(self, "category_code", code)
        object.__setattr__(self, "category_name", name)

    @classmethod
    def tranform_with_string(cls, value: Any) -> tuple[CategoryItemBuilder, ...]:
        if value is None:
            return ()
        items: list[CategoryItemBuilder] = []
        for chunk in str(value).split(";"):
            if not chunk.strip():
                continue
            code, _, name = chunk.partition(":")
            items.append(cls(category_code=code, category_name=name))
        return tuple(items)
