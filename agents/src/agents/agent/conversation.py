"""Strands agent wrapper for conversation management"""

from strands import Agent
import boto3
from typing import AsyncGenerator
from agents.config import get_settings
import logging

logger = logging.getLogger(__name__)


class ConversationAgent:
    """Wrapper for Strands agent with streaming support"""

    def __init__(self):
        settings = get_settings()

        # Initialize AWS session
        self.session = boto3.Session(
            profile_name=settings.aws_default_profile,
            region_name=settings.aws_region
        )

        # Initialize Strands agent with Bedrock model
        self.agent = Agent(model=settings.bedrock_model)

        # Store conversation history per session
        self.conversations: dict[str, list[dict]] = {}

        logger.info(f"Initialized ConversationAgent with model: {settings.bedrock_model}")

    async def send_message(
        self,
        session_id: str,
        message: str
    ) -> AsyncGenerator[str, None]:
        """
        Send message to agent and stream response

        Args:
            session_id: Unique session identifier
            message: User message

        Yields:
            Chunks of agent response
        """
        # Get or create conversation history
        if session_id not in self.conversations:
            self.conversations[session_id] = []
            logger.info(f"Created new conversation for session: {session_id}")

        # Add user message to history
        self.conversations[session_id].append({
            "role": "user",
            "content": message
        })

        logger.debug(f"User message ({session_id}): {message}")

        # Call Strands agent
        # TODO: Implement streaming when Strands SDK supports it
        # For now, simple non-streaming response
        try:
            result = self.agent(message)

            # Extract text from AgentResult object
            if hasattr(result, 'text'):
                response = result.text
            elif hasattr(result, 'content'):
                response = result.content
            else:
                # Fallback: convert to string
                response = str(result)

            # Add assistant response to history
            self.conversations[session_id].append({
                "role": "assistant",
                "content": response
            })

            logger.debug(f"Agent response ({session_id}): {response}")

            # Yield response (streaming will be added later)
            yield response

        except Exception as e:
            logger.error(f"Error getting agent response ({session_id}): {e}")
            error_msg = "I'm sorry, I encountered an error processing your request. Please try again."
            yield error_msg

    def get_conversation(self, session_id: str) -> list[dict]:
        """Get conversation history for session"""
        return self.conversations.get(session_id, [])

    def clear_conversation(self, session_id: str):
        """Clear conversation history for session"""
        if session_id in self.conversations:
            del self.conversations[session_id]
            logger.info(f"Cleared conversation for session: {session_id}")


# Global agent instance
_agent: ConversationAgent | None = None


def get_agent() -> ConversationAgent:
    """Get or create global agent instance"""
    global _agent
    if _agent is None:
        _agent = ConversationAgent()
    return _agent
