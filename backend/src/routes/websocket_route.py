import asyncio
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

ws = APIRouter()
websocket_connections = {}

logger = logging.getLogger(__name__)


@ws.websocket("/{userId}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """
    WebSocket 연결 관리
    사용자 로그인 시 WebSocket 연결을 유지하고, 로그아웃 시 연결을 해제한다.

    Args:
        websocket (WebSocket): FastAPI WebSocket 객체
        user_id (int): 사용자 ID
    """
    await websocket.accept()
    websocket_connections[user_id] = websocket

    try:
        while True:
            await websocket.receive_text()  # ping 연결용으로 사용
    except WebSocketDisconnect:
        websocket_connections.pop(user_id, None)


def notify_client(user_id: int, message: str):
    """
    특정 사용자에게 WebSocket을 통해 알림 전송

    Args:
        user_id (int): 사용자 ID
        message (str): 알림 내용
    """
    websocket = websocket_connections.get(user_id)
    if websocket:
        try:
            asyncio.run(websocket.send_text(message))
        except Exception as e:
            logger.error(f"WebSocket 알림 전송 실패 | user_id={user_id} | 오류: {str(e)}")
