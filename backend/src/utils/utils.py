import json
from typing import Union, List


def parse_json_to_list(value: str) -> List[Union[int, float, str]]:
    """
    주어진 값이 문자열이면 JSON으로 파싱하여 리스트로 변환

    Args:
        value (str): 파싱할 값 (보통 JSON 문자열)

    Returns:
        List[Union[int, str]]: JSON 파싱에 성공하면 리스트, 실패하면 빈 리스트
    """
    try:
        return json.loads(value)
    except Exception:
        return []  # 변환 실패 시 빈 리스트 반환
