import hashlib
import json
from typing import Any


class ProductHashService:
    @staticmethod
    def hash_dict(dict_json: dict[str, Any]) -> str:
        json_str = json.dumps(
            dict_json,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            default=str,
        )

        return hashlib.sha256(json_str.encode("utf-8")).hexdigest()
