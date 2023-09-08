import asyncio
import json
from models.message import Message

async def send_message(host, port, message, user_label, user_port):
    reader, writer = await asyncio.open_connection(host, port)
    message.sender = f"{user_label}@{host}:{user_port}"
    writer.write(message.to_json().encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()
