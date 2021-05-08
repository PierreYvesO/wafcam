import asyncio
import websockets

class WebSocket:
    def __init__(self):
        self.start_server = websockets.serve(self.hello, "localhost", 8765)
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()

    async def hello(self, websocket, path):
        name = await websocket.recv()
        print(f"< {name}")

        greeting = f"Hello {name}!"

        await websocket.send(greeting)
        print(f"> {greeting}")



