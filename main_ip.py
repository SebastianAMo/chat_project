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
        self.messages ={} # {username: [{"from": sender, "message": message}, ...]}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True  # control variable for the server loop

    def view_messages(self):
        peer_name = input("Introduce el nombre del Peer cuyos mensajes quieres ver: ")
        if peer_name in self.messages:
            print("\n-------------Mensajes-------------")
            print(f"Mensajes con {peer_name}:")
            for msg in self.messages[peer_name]:
                print(f"{msg['from']}: {msg['message']}")
            print("-----------------------------------\n")
        else:
            print("No hay mensajes con ese Peer.")

    def start_server(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Escuchando en {self.host}:{self.port}")
            while self.running:
                client_socket, _ = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        except socket.error as e:
            if e.winerror == 10038:
                # Si el error es porque el socket ha sido cerrado, simplemente sal del método
                return
            print(f"Socket error while starting server: {e}")
        except Exception as e:
            print(f"Error while starting server: {e}")


    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                message_data = json.loads(data)
                from_username = message_data.get("from")
                
                # Storing the received message in the 'messages' dictionary
                if from_username not in self.messages:
                    self.messages[from_username] = []
                self.messages[from_username].append({"from": from_username, "message": message_data['message']})

                if from_username not in self.contacts:
                    self.contacts[from_username] = client_socket.getpeername()
                    port = message_data.get("port")
                    host = message_data.get("host")
                    self.connect_to_peer(host,int(port))
                    
                # Save the client socket for persistent connection
                self.connected_sockets[from_username] = client_socket
        except socket.error as e:
            print(f"Socket error while handling client {client_socket.getpeername()}: {e}")
        except Exception as e:
            print(f"Error while handling client {client_socket.getpeername()}: {e}")

    def connect_to_peer(self, host, port):
        try:
            if host not in self.connected_sockets:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((host, port))
                self.send_initial_message(client_socket)
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
                print(f"Conectado con {host}:{port}")
        except socket.error as e:
            print(f"Socket error while connecting to peer: {e}")
        except Exception as e:
            print(f"Error while connecting to peer: {e}")

    def send_initial_message(self, client_socket):
        try:
            message_data = {
                "from": self.username,
                "message": f"Conectado con {self.username}",
                "port": f"{self.port}",
                "host": f"{self.host}"
            }
            client_socket.send(json.dumps(message_data).encode())
        except socket.error as e:
            print(f"Socket error while sending initial message: {e}")
        except Exception as e:
            print(f"Error while sending initial message: {e}")

    def send_message(self, peer_name, message):
        try:
            if peer_name in self.connected_sockets:
                message_data = {
                    "from": self.username,
                    "message": message
                }
                self.connected_sockets[peer_name].send(json.dumps(message_data).encode())
                
                # Storing the sent message in the 'messages' dictionary
                if peer_name not in self.messages:
                    self.messages[peer_name] = []
                self.messages[peer_name].append({"from": self.username, "message": message})
            else:
                print("Peer no encontrado.")
        except socket.error as e:
            print(f"Socket error while sending message: {e}")
        except Exception as e:
            print(f"Error while sending message: {e}")

    def show_contacts(self):
        for username, (ip, port) in self.contacts.items():
            print("\n-------------Contactos-------------")
            print(f"{username}: {ip}:{port}")
            print("-----------------------------------\n")


class Interface(Peer):
    def __init__(self, username, host='127.0.0.1', port=12345):
        super().__init__(username, host, port)
        
    def user_interface(self):
        while True:
            print("1. Conectar con otro Peer")
            print("2. Enviar mensaje")
            print("3. Mostrar contactos")
            print("4. Ver mensajes")
            print("5. Salir")
            choice = input("Elige una opción: ")
            try:
                if choice == "1":
                    host = input("Introduce la ip del Peer: ")
                    port = int(input("Introduce el puerto del Peer: "))
                    self.connect_to_peer(host, port)
                elif choice == "2":
                    peer_name = input("Introduce el nombre del Peer a quien enviar el mensaje: ")
                    message = input("Escribe tu mensaje: ")
                    self.send_message(peer_name, message)
                elif choice == "3":
                    self.show_contacts()
                elif choice == "4":
                    self.view_messages()
                elif choice == "5":
                    self.running = False  # stop the server loop
                    for sock in self.connected_sockets.values():
                        sock.close()
                    self.server_socket.close()
                    break
            except socket.error as e:
                print(f"Socket error: {e}")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    username = input("Introduce tu nombre de usuario: ")
    port = int(input("Introduce puerto: "))
    ip = input("Introduce ip: ")
    peer = Interface(username, port=port, host=ip)
    threading.Thread(target=peer.start_server).start()
    peer.user_interface()
    