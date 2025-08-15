import websockets
import asyncio
from typing import Optional
from collections import deque

class WebSocketClient():
    def __init__(self, uri:str, headers:str, max_retries: int=5, backoff_factor: float=2):
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
            
    def send_message():
        pass

    def receive_message():
        pass
    
    def flush_message():
        pass

    def send_ping():
        pass

    def close():
        pass

    def run():
        pass