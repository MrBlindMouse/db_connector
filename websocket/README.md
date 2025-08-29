# Websocket Implementation
Simple scripts to create and maintain websocket connections.

## How to use
Copy code from the files.

Supply the class with uri and headers

Edit code to handle message logic as you require.

```python
    def receive_message(self):
        try:
            message = self.ws.recv()

            json_message = json.loads(message)
            response = None
            if json_message["type"] == "UPDATE":
                response = sample_function(json_message["data"])
            if response:
                self.send_message(json.dumps(response))

        except websocket.WebSocketConnectionClosedException:
            print("Connection closed")
            raise
        except Exception as e:
            print(f"Receive error: {e}")
```

## Notes
async_websocket_connection - Requires 'websockets'
threaded_websocket_connection - Requires 'websocket-client'
websocket_connection - Requires 'websocket-client'