import asyncio
from models.message import Message
from utils.serializer import message_to_json, json_to_message

async def handle_client(reader, writer):
    data = await reader.read(100)
    message = json_to_message(data.decode())
    print(f"Received {message.content} from {message.sender}")
    writer.close()
    await writer.wait_closed()

async def start_server(port, handle_client_func):
    server = await asyncio.start_server(handle_client_func, '0.0.0.0', port)
    async with server:
        await server.serve_forever()
