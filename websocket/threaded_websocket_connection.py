import websocket    #websocket-client module
import json
import time
import threading
from typing import Optional, Dict
from collections import deque

class WebSocketClient:
    def __init__(self, uri: str, headers: Dict[str, str], max_retries: int = 5, backoff_factor: float = 2):
        self.uri = uri
        self.headers = headers
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.ws: Optional[websocket.WebSocket] = None
        self.message_queue = deque()
        self.running = False
        self.lock = threading.Lock()

    def connect(self) -> Optional[websocket.WebSocket]:
        for attempt in range(self.max_retries):
            try:
                ws = websocket.WebSocket()

                # ------------------------------
                # Custom headers logic goes here
                # ------------------------------
                
                ws.connect(self.uri, header=self.headers)
                self.ws = ws
                return ws
            except websocket.WebSocketException as e:
                delay = self.backoff_factor ** attempt
                print(f"Connection attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)
        print("Max reconnection attempts reached")
        return None

    def send_message(self, message: str):
        with self.lock:
            if not self.ws or self.ws.sock is None:
                self.message_queue.append(message)
                return
        try:
            self.ws.send(message)
        except websocket.WebSocketConnectionClosedException:
            self.message_queue.append(message)
            print("Cannot send: Connection closed")
        except Exception as e:
            print(f"Cannot send: {e}")

    def flush_queue(self):
        with self.lock:
            while self.message_queue and self.ws and self.ws.sock:
                message = self.message_queue.popleft()
                self.send_message(message)

    def receive_message(self):
        try:
            message = self.ws.recv()
            # -----------------------
            # Message Logic goes here
            print(message)
            # -----------------------
        except websocket.WebSocketConnectionClosedException:
            print("Connection closed")
            raise
        except Exception as e:
            print(f"Receive error: {e}")

    def send_ping(self):
        while self.running and self.ws and self.ws.sock:
            try:
                self.ws.ping()
                time.sleep(30)
            except Exception as e:
                print(f"Ping error: {e}")
                break

    def close(self):
        if self.ws:
            try:
                self.ws.close()
                print("Connection closed gracefully")
            except Exception as e:
                print(f"Close error: {e}")
            finally:
                self.ws = None

    def run(self):
        self.running = True
        # -----------------------
        # Initial message as defined by the connection server
        initial_message = json.dumps({})
        # -----------------------
        ping_thread = None
        while self.running:
            try:
                if not self.ws or self.ws.sock is None:
                    self.ws = self.connect()
                    if not self.ws:
                        break
                    self.send_message(initial_message)
                    self.flush_queue()
                ping_thread = threading.Thread(target=self.send_ping)
                ping_thread.start()
                self.receive_message()
            except (websocket.WebSocketConnectionClosedException, websocket.WebSocketTimeoutException):
                print("Connection lost, attempting to reconnect...")
                self.close()
                continue
            except KeyboardInterrupt:
                print("Shutting down...")
                self.running = False
                break
            finally:
                if ping_thread and ping_thread.is_alive():
                    # Note: Threads can't be cancelled like tasks; wait or flag
                    pass  # For simplicity, let it run; add stop flag if needed

        self.close()

def main():
    client = WebSocketClient(
        uri="wss://websocket server",
        headers={"Authorization": "Bearer token"}
    )
    client.run()

if __name__ == "__main__":
    main()