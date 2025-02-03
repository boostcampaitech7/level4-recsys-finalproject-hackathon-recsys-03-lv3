import json
from typing import Any


def parse_json_to_list(value: Any) -> Any:
    """
    주어진 값이 문자열이면 JSON으로 파싱하여 리스트로 변환하고, 그렇지 않으면 원래 값을 반환

    Args:
        value (Any): 파싱할 값 (보통 JSON 문자열)

    Returns:
        Any: JSON 파싱에 성공하면 리스트, 실패하면 빈 리스트, 문자열이 아니면 원래 값
    """
    if isinstance(value, str):
        try:
            return json.loads(value)
        except Exception:
            return []  # 변환 실패 시 빈 리스트 반환
    return value
