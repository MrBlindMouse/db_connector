import websockets    #websockets module
import asyncio
import json
from typing import Optional, Dict
from collections import deque

class WebSocketClient:
    def __init__(self, uri: str, headers: Dict[str, str], max_retries: int = 5, backoff_factor: float = 2):
        self.uri = uri
        self.headers = headers
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.message_queue = deque()
        self.running = False

    async def connect(self) -> Optional[websockets.WebSocketClientProtocol]:
        for attempt in range(self.max_retries):
            try:

                # ------------------------------
                # Custom headers logic goes here
                # ------------------------------

                self.websocket = await asyncio.wait_for(
                    websockets.connect(self.uri, additional_headers=self.headers, ping_interval=30),
                    timeout=10
                )
                return self.websocket
            except (websockets.exceptions.WebSocketException, asyncio.TimeoutError) as e:
                delay = self.backoff_factor ** attempt
                print(f"Connection attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                await asyncio.sleep(delay)
        print("Max reconnection attempts reached")
        return None

    async def send_message(self, message: str):
        if not self.websocket or self.websocket.closed:
            self.message_queue.append(message)
            return
        try:
            await self.websocket.send(message)
        except websockets.exceptions.ConnectionClosed:
            self.message_queue.append(message)
            print("Cannot send: Connection closed")
        except Exception as e:
            print(f"Cannot send: {e}")

    async def flush_queue(self):
        while self.message_queue and self.websocket and not self.websocket.closed:
            message = self.message_queue.popleft()
            await self.send_message(message)

    async def receive_message(self):
        try:
            message = await asyncio.wait_for(self.websocket.recv(), timeout=60)

            # -----------------------
            # Message Logic goes here
            print(message)
            # -----------------------

        except asyncio.TimeoutError:
            print("No message received within timeout")
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
            raise
        except Exception as e:
            print(f"Receive error: {e}")

    async def send_ping(self):
        while self.running and self.websocket and not self.websocket.closed:
            try:
                await self.websocket.ping()
                await asyncio.sleep(30)
            except Exception as e:
                print(f"Ping error: {e}")
                break

    async def close(self):
        if self.websocket:
            try:
                await self.websocket.close()
                print("Connection closed gracefully")
            except Exception as e:
                print(f"Close error: {e}")
            finally:
                self.websocket = None

    async def run(self):
        self.running = True

        # -----------------------
        # Initial message as defined by the connection server
        initial_message = json.dumps({})
        # -----------------------

        ping_task = None
        while self.running:
            try:
                if not self.websocket or self.websocket.closed:
                    self.websocket = await self.connect()
                    if not self.websocket:
                        break
                    await self.send_message(initial_message)
                    await self.flush_queue()
                ping_task = asyncio.create_task(self.send_ping())
                await self.receive_message()
            except (websockets.exceptions.ConnectionClosed, asyncio.CancelledError):
                print("Connection lost, attempting to reconnect...")
                await self.close()
                continue
            except KeyboardInterrupt:
                print("Shutting down...")
                self.running = False
                break
            finally:
                if ping_task:
                    ping_task.cancel()

        await self.close()

async def main():
    client = WebSocketClient(
        uri="wss://websocket server",
        headers={"Once-off header": "value"}
    )
    await client.run()

if __name__ == "__main__":
    asyncio.run(main())