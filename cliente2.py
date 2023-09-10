import socket
import json
import threading

class Peer:
    def __init__(self, username, host='127.0.0.1', port=12345):
        self.username = username
        self.host = host
        self.port = port
        self.contacts = {}  # {username: (ip, port)}
        self.connected_sockets = {}  # {username: socket}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def user_interface(self):
        while True:
            print("1. Conectar con otro Peer")
            print("2. Enviar mensaje")
            print("3. Mostrar contactos")
            print("4. Salir")
            choice = input("Elige una opción: ")
            if choice == "1":
                host = '127.0.0.1'
                port = int(input("Introduce el puerto del Peer: "))
                self.connect_to_peer(host, port)
            elif choice == "2":
                peer_name = input("Introduce el nombre del Peer a quien enviar el mensaje: ")
                message = input("Escribe tu mensaje: ")
                self.send_message(peer_name, message)
            elif choice == "3":
                self.show_contacts()
            elif choice == "4":
                # Close all sockets before exiting
                for sock in self.connected_sockets.values():
                    sock.close()
                self.server_socket.close()
                break

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Escuchando en {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            message_data = json.loads(data)
            from_username = message_data.get("from")
            message = message_data.get("message")
            print(f"Nuevo mensaje de {from_username}: {message}")
            if from_username not in self.contacts:
                self.contacts[from_username] = client_socket.getpeername()
            # Save the client socket for persistent connection
            self.connected_sockets[from_username] = client_socket

    def connect_to_peer(self, host, port):
        if host not in self.connected_sockets:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            self.send_initial_message(client_socket)
            # Start a dedicated thread to listen to messages from this peer
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            print(f"Conectado con {host}:{port}")

    def send_initial_message(self, client_socket):
        message_data = {
            "from": self.username,
            "message": f"Conectado con {self.username}"
        }
        client_socket.send(json.dumps(message_data).encode())

    def send_message(self, peer_name, message):
        if peer_name in self.connected_sockets:
            message_data = {
                "from": self.username,
                "message": message
            }
            self.connected_sockets[peer_name].send(json.dumps(message_data).encode())
        else:
            print("Peer no encontrado.")

    def show_contacts(self):
        for username, (ip, port) in self.contacts.items():
            print(f"{username}: {ip}:{port}")

if __name__ == "__main__":
    username = "u2"
    port = 2000
    p = Peer(username, port=port)
    server_thread = threading.Thread(target=p.start_server)
    server_thread.start()
    p.user_interface()