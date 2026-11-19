from typing import Any


class FormatString:
    def tranform_text(self, value: str | None) -> str | None:
        if value is None:
            return None
        value = str(value).strip()
        return value or None

    @staticmethod
    def split_string_tuple(value: str) -> tuple[str, ...]:
        if value is None:
            return ()

        string_to_list = str(value).split(",")
        return tuple(part for part in string_to_list)

    @staticmethod
    def format_bool(value: Any, default_value: bool) -> bool:
        if value is None:
            return default_value

        tranform_text = str(value).strip().lower()
        TRUE_VALUES = {"true", "1", "yes", "y"}
        FALSE_VALUES = {"false", "0", "no", "n"}

        if tranform_text == "":
            return default_value
        if tranform_text in TRUE_VALUES:
            return True
        if tranform_text in FALSE_VALUES:
            return False

        raise ValueError(f"invalid boolean value '{value}'")
