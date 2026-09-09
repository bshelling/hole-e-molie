"""WebSocket test client for HoleeMoly API"""

import asyncio
import websockets
import json
import sys


async def test_chat():
    """Test WebSocket chat endpoint"""
    uri = "ws://localhost:8000/api/chat"

    print(f"Connecting to {uri}...")

    try:
        async with websockets.connect(uri) as websocket:
            # Receive welcome message
            welcome = await websocket.recv()
            welcome_data = json.loads(welcome)
            print(f"\n[{welcome_data['type'].upper()}] {welcome_data['content']}")
            print(f"Session ID: {welcome_data['session_id']}\n")

            # Test messages
            test_messages = [
                "Hello, I want to report a pothole",
                "There's a big pothole on Magazine Street near Whole Foods",
                "Can you check the status of my reports?"
            ]

            for user_msg in test_messages:
                print(f"[YOU] {user_msg}")

                # Send message
                await websocket.send(json.dumps({
                    "type": "message",
                    "content": user_msg
                }))

                # Receive echo and response
                for _ in range(2):  # Expect user echo + agent response
                    response = await websocket.recv()
                    data = json.loads(response)

                    if data['type'] == 'assistant':
                        print(f"[AGENT] {data['content']}\n")
                    elif data['type'] == 'error':
                        print(f"[ERROR] {data['content']}\n")

                await asyncio.sleep(1)  # Brief pause between messages

            print("✓ All test messages sent successfully!")

    except websockets.exceptions.WebSocketException as e:
        print(f"✗ WebSocket error: {e}")
        print("\nMake sure the API server is running:")
        print("  cd /Users/shelling/Projects/holeemoly/agents")
        print("  make run-api")
        sys.exit(1)

    except ConnectionRefusedError:
        print("✗ Connection refused. Is the API server running?")
        print("\nStart the server with:")
        print("  cd /Users/shelling/Projects/holeemoly/agents")
        print("  make run-api")
        sys.exit(1)

    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_chat())
