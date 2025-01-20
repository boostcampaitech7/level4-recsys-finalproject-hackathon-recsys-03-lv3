ERROR_MESSAGES = {
    "BAD_REQUEST": {
        "status": 400,
        "message": "요청이 잘못되었습니다. 입력 데이터({})를 확인하고 다시 시도하세요."
    },
    "UNAUTHORIZED": {
        "status": 401,
        "message": "인증되지 않았습니다. 로그인 후 다시 시도하세요."
    },
    "FORBIDDEN": {
        "status": 403,
        "message": "접근 권한이 없습니다. 요청이 거부되었습니다."
    },
    "NOT_FOUND": {
        "status": 404,
        "message": "요청한 리소스({})를 찾을 수 없습니다. URL 또는 요청 내용을 확인하세요."
    },
    "REQUEST_TIMEOUT": {
        "status": 408,
        "message": "요청 시간이 초과되었습니다. 다시 시도해주세요."
    },
    "CONFLICT": {
        "status": 409,
        "message": "요청이 서버 상태와 충돌했습니다. 입력 데이터를 확인하거나 중복된 요청인지 확인하세요."
    },
    "UNPROCESSABLE_ENTITY": {
        "status": 422,
        "message": "요청한 데이터의 처리에 실패했습니다. 유효성 검증 오류가 발생했습니다: {}"
    },
    "TOO_MANY_REQUESTS": {
        "status": 429,
        "message": "너무 많은 요청을 보냈습니다. 잠시 후 다시 시도하세요."
    }
}