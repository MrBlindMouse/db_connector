import websocket
import json
import time
from typing import Dict, Optional
from collections import deque

class WebSocketClient:
    def __init__(self, uri: str, headers: Dict[str, str], max_retries: int = 5, backoff_factor: float = 2):
        self.uri = uri
        self.headers = headers
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.ws: Optional[websocket.WebSocketApp] = None
        self.message_queue = deque()
        self.running = False
        self.attempts = 0

    def on_open(self, ws: websocket.WebSocketApp):
        print("Connection established")
        self.attempts = 0
        # Send initial message as per connection server instruction
        initial_message = json.dumps({})
        ws.send(initial_message)
        self.flush_queue(ws)

    def on_message(self, ws: websocket.WebSocketApp, message: str):
        
        # -----------------------
        # Message Logic goes here
        print(f"Received: {message}")
        # -----------------------

    def on_error(self, ws: websocket.WebSocketApp, error: Exception):
        print(f"Error: {error}")

    def on_close(self, ws: websocket.WebSocketApp, close_status_code: Optional[int], close_msg: Optional[str]):
        print(f"Connection closed: {close_status_code}, {close_msg}")
        self.running = False
        self.ws = None

    def send_message(self, message: str):
        if not self.ws or not self.running:
            self.message_queue.append(message)
            return
        try:
            self.ws.send(message)
        except websocket.WebSocketConnectionClosedException:
            self.message_queue.append(message)
            print("Cannot send: Connection closed")
        except Exception as e:
            print(f"Cannot send: {e}")

    def flush_queue(self, ws: websocket.WebSocketApp):
        while self.message_queue and self.running:
            message = self.message_queue.popleft()
            try:
                ws.send(message)
            except Exception as e:
                print(f"Failed to send queued message: {e}")
                self.message_queue.appendleft(message)  # Re-queue on failure
                break

    def connect(self):
        self.attempts += 1
        if self.attempts > self.max_retries:
            print("Max reconnection attempts reached")
            self.running = False
            return
        try:
            self.ws = websocket.WebSocketApp(
                self.uri,
                header=self.headers,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            self.running = True
            self.ws.run_forever(ping_interval=30, reconnect=5)
        except Exception as e:
            delay = self.backoff_factor ** (self.attempts - 1)
            print(f"Connection attempt {self.attempts} failed: {e}. Retrying in {delay}s...")
            time.sleep(delay)
            self.connect()

    def close(self):
        if self.ws:
            try:
                self.ws.close()
                print("Connection closed gracefully")
            except Exception as e:
                print(f"Close error: {e}")
            finally:
                self.ws = None
                self.running = False

    def run(self):
        self.running = True
        while self.running:
            try:
                self.connect()
                if self.attempts >= self.max_retries:
                    break
            except KeyboardInterrupt:
                print("Shutting down...")
                self.running = False
                break
        self.close()

def main():
    client = WebSocketClient(
        uri="wss://websocket-server",
        headers={"Authorization": "Bearer token"}
    )
    client.run()

if __name__ == "__main__":
    main()