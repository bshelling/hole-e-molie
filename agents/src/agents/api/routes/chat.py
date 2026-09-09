"""WebSocket chat endpoint"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from agents.agent import get_agent
import json
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


class ConnectionManager:
    """Manage WebSocket connections"""

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket) -> str:
        """Accept connection and return session ID"""
        await websocket.accept()
        session_id = str(uuid.uuid4())
        self.active_connections[session_id] = websocket
        logger.info(f"Client connected: {session_id}")
        return session_id

    def disconnect(self, session_id: str):
        """Remove connection"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"Client disconnected: {session_id}")

    async def send_message(self, session_id: str, message: dict):
        """Send message to specific connection"""
        if session_id in self.active_connections:
            websocket = self.active_connections[session_id]
            await websocket.send_json(message)


manager = ConnectionManager()


@router.websocket("/chat")
async def chat_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat with agent

    Client sends: {"type": "message", "content": "user message"}
    Server sends: {"type": "message", "content": "agent response", "session_id": "..."}
    """
    session_id = await manager.connect(websocket)
    agent = get_agent()

    try:
        # Send welcome message
        await manager.send_message(session_id, {
            "type": "system",
            "content": "Connected to HoleeMoly agent. How can I help you report a pothole?",
            "session_id": session_id
        })

        while True:
            # Receive message from client
            data = await websocket.receive_text()

            try:
                message_data = json.loads(data)
                user_message = message_data.get("content", "")

                if not user_message:
                    continue

                logger.info(f"User message ({session_id}): {user_message}")

                # Send user message echo
                await manager.send_message(session_id, {
                    "type": "user",
                    "content": user_message,
                    "session_id": session_id
                })

                # Get agent response (streaming)
                agent_response = ""
                async for chunk in agent.send_message(session_id, user_message):
                    agent_response += chunk

                # Send agent response
                await manager.send_message(session_id, {
                    "type": "assistant",
                    "content": agent_response,
                    "session_id": session_id
                })

                logger.info(f"Agent response ({session_id}): {agent_response}")

            except json.JSONDecodeError:
                await manager.send_message(session_id, {
                    "type": "error",
                    "content": "Invalid message format. Expected JSON with 'content' field.",
                    "session_id": session_id
                })

    except WebSocketDisconnect:
        manager.disconnect(session_id)
        agent.clear_conversation(session_id)

    except Exception as e:
        logger.error(f"WebSocket error ({session_id}): {e}")
        manager.disconnect(session_id)
        agent.clear_conversation(session_id)
