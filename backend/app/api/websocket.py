import json
import logging
from collections import defaultdict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections grouped by match_id.

    Each match has its own set of connected clients. When a score
    update comes in, it is broadcast to all clients watching that match.
    """

    def __init__(self):
        # match_id -> set of WebSocket connections
        self.active_connections: dict[int, set[WebSocket]] = defaultdict(set)

    async def connect(self, websocket: WebSocket, match_id: int):
        """Accept a WebSocket connection and register it for a match."""
        await websocket.accept()
        self.active_connections[match_id].add(websocket)
        logger.info(
            "WebSocket connected for match %d, total connections: %d",
            match_id,
            len(self.active_connections[match_id]),
        )

    def disconnect(self, websocket: WebSocket, match_id: int):
        """Remove a WebSocket connection from a match."""
        self.active_connections[match_id].discard(websocket)
        if not self.active_connections[match_id]:
            del self.active_connections[match_id]
        logger.info("WebSocket disconnected for match %d", match_id)

    async def broadcast(self, match_id: int, data: dict):
        """Broadcast a message to all clients watching a specific match."""
        connections = self.active_connections.get(match_id, set())
        dead_connections = []

        for websocket in connections:
            try:
                await websocket.send_json(data)
            except Exception:
                dead_connections.append(websocket)

        # Clean up dead connections
        for ws in dead_connections:
            self.active_connections[match_id].discard(ws)

    async def broadcast_all(self, data: dict):
        """Broadcast a message to all connected clients across all matches."""
        for match_id in list(self.active_connections.keys()):
            await self.broadcast(match_id, data)

    def get_connection_count(self, match_id: int) -> int:
        """Get the number of active connections for a match."""
        return len(self.active_connections.get(match_id, set()))

    def get_total_connections(self) -> int:
        """Get the total number of active connections across all matches."""
        return sum(len(conns) for conns in self.active_connections.values())


# Singleton connection manager
manager = ConnectionManager()


@router.websocket("/live/{match_id}")
async def live_score(websocket: WebSocket, match_id: int):
    """WebSocket endpoint for real-time match score updates.

    Clients connect to receive live updates for a specific match.
    The server pushes events as they happen (goals, cards, etc.).

    Message format sent to clients:
    {
        "type": "score_update" | "event" | "status_change" | "heartbeat",
        "match_id": 123,
        "data": { ... }
    }
    """
    await manager.connect(websocket, match_id)

    # Send initial connection confirmation
    await websocket.send_json({
        "type": "connected",
        "match_id": match_id,
        "message": "已连接实时比分推送",
    })

    try:
        while True:
            # Keep the connection alive; receive messages from client
            raw = await websocket.receive_text()

            try:
                message = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "无效的 JSON 格式",
                })
                continue

            msg_type = message.get("type")

            if msg_type == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "match_id": match_id,
                })
            elif msg_type == "subscribe":
                # Client can switch to watching a different match
                new_match_id = message.get("match_id")
                if new_match_id and isinstance(new_match_id, int):
                    manager.disconnect(websocket, match_id)
                    match_id = new_match_id
                    manager.active_connections[match_id].add(websocket)
                    await websocket.send_json({
                        "type": "subscribed",
                        "match_id": match_id,
                    })
            else:
                await websocket.send_json({
                    "type": "error",
                    "message": f"未知的消息类型: {msg_type}",
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket, match_id)
    except Exception as e:
        logger.error("WebSocket error for match %d: %s", match_id, str(e))
        manager.disconnect(websocket, match_id)
