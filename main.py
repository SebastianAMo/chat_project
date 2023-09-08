import asyncio
import json
from client import send_message
from models.message import Message, message_from_json
from models.contact import Contact

contacts = []
user_label = ''

def load_contacts():
    global contacts
    try:
        with open('data.json', 'r') as f:
            contacts_data = json.load(f)
            for contact_data in contacts_data:
                contact = Contact(contact_data['ip'], contact_data['port'], contact_data['label'])
                contacts.append(contact)
    except FileNotFoundError:
        pass

def save_contacts():
    contacts_data = [{'ip': contact.ip, 'port': contact.port, 'label': contact.label} for contact in contacts]
    with open('data.json', 'w') as f:
        json.dump(contacts_data, f)

async def handle_client(reader, writer):
    data = await reader.read(100)
    message = message_from_json(data.decode())
    print(f"Received {message.content} from {message.sender}")

async def start_server(port, callback):
    server = await asyncio.start_server(callback, '0.0.0.0', port)
    async with server:
        await server.serve_forever()

async def main():
    global user_label
    load_contacts()
    port = int(input("Enter your port: "))
    user_label = input("Enter your label or username: ")
    asyncio.create_task(start_server(port, handle_client))

    try:
        while True:
            print("1. Send Message")
            print("2. Add Contact")
            print("3. List Contacts")
            choice = input("Choose an option: ")

            if choice == "1":
                idx = int(input("Enter contact index: "))
                contact = contacts[idx]
                msg_content = input("Enter your message: ")
                message = Message(f'localhost:{port}', msg_content)
                asyncio.create_task(send_message(contact.ip, contact.port, message, user_label, port))

            elif choice == "2":
                ip = input("Enter contact IP: ")
                contact_port = int(input("Enter contact port: "))
                label = input("Enter contact label: ")
                contacts.append(Contact(ip, contact_port, label))
                save_contacts()

            elif choice == "3":
                for idx, contact in enumerate(contacts):
                    print(f"{idx}. {contact.label} ({contact.ip}:{contact.port})")

    except KeyboardInterrupt:
        print("\nExiting chat...")

if __name__ == "__main__":
    asyncio.run(main())
