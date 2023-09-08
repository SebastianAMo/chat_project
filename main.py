import socket
import json
import threading

class Peer:
    def __init__(self, username, host='127.0.0.1', port=12345):
        self.username = username
        self.host = host
        self.port = port
        self.contacts = {}  # {username: (ip, port)}
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
                if peer_name in self.contacts:
                    self.send_message(message, *self.contacts[peer_name])
                else:
                    print("Peer no encontrado.")
            elif choice == "3":
                self.show_contacts()
            elif choice == "4":
                break

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Escuchando en {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        data = client_socket.recv(1024).decode()
        message_data = dict(data)
        from_username = message_data.get("from")
        message = message_data.get("message")
        print(f"\nNuevo mensaje de {from_username}: {message}\n")
        if from_username not in self.contacts:
            self.contacts[from_username] = client_socket.getpeername()

    def connect_to_peer(self, host, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        self.contacts[host] = (host, port)
        self.send_message(f"Conectado con {self.username}", host, port)
        
        print(f"Conectado con {host}:{port}")

    def send_message(self, message, host, port):
        message_data = {
            "from": self.username,
            "message": message
        }
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        client_socket.send(json.dumps(message_data).encode())
        client_socket.close()

    def show_contacts(self):
        for username, (ip, port) in self.contacts.items():
            print(f"{username}: {ip}:{port}")

if __name__ == "__main__":
    username = input("Introduce tu nombre de usuario: ")
    port = int(input("Introduce puerto: "))
    p = Peer(username,port=port)
    server_thread = threading.Thread(target=p.start_server)
    server_thread.start()
    p.user_interface()
