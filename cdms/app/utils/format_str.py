class FormatString:
    def tranform_text(self, value: str | None) -> str | None:
        if value is None:
            return None
        value = str(value).strip()
        return value or None
