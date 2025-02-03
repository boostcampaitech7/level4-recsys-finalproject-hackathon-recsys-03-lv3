import json
from typing import Any


def parse_json_to_list(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return []  # 변환 실패 시 빈 리스트 반환
    return value
