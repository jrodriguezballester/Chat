import socket
import threading


class Servidor:

    def __init__(self, host=socket.gethostbyname(socket.gethostname()), port=4000):
        print("La IP del servidor es: " + host)
        # Address is stored as a tuple
        self.ADDRESS = (host, port)

        self.FORMAT = "utf-8"

        # Lists that will contains all the clients connected to the server and their names.
        self.clients, self.names = [], []

        # Create a new socket for the server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind the address of the server to the socket
        self.server.bind(self.ADDRESS)

        self.server.listen(10)

        aceptar = threading.Thread(target=self.startChat)
        # aceptar.daemon = True
        aceptar.start()

    # function to start the connection
    def startChat(self):

        while True:
            # aceptar conexiones y devoluciones un nuevo hilo con el cliente y la dirección vinculada a él
            conn, addr = self.server.accept()

            print("Conected")

            conn.send("NAME".encode(self.FORMAT))

            # 1024 represents the max amount of data that can be received (bytes)
            name = conn.recv(1024).decode(self.FORMAT)

            # append the name and client to the respective list
            self.names.append(name)
            self.clients.append(conn)

            print(f"Name is: {name}")
            msg_string = f"{name} has joined the chat!"
            # broadcast message
            self.msg_to_all(msg_string.encode(self.FORMAT))

            conn.send('Connection successful!'.encode(self.FORMAT))

            # Start the handling thread
            thread = threading.Thread(target=self.handle, args=(conn, addr))
            thread.start()

            # no. of clients connected to the server
            print(f"active connections {threading.activeCount() - 2}")

        # method to handle the incoming messages

    def handle(self, conn, addr):
        with conn:
            print(f"new connection {addr}")
            bandera = True
            while bandera:
                # recieve message
                try:
                    # message = conn.recv(1024).decode(self.FORMAT)
                    message = conn.recv(1024)
                except Exception as e:
                    message = f"{addr} Ha abandonado el chat ".encode(self.FORMAT)
                    print(f"FIN connection {addr}")
                    bandera = False
                    pass
                    # broadcast message
                self.msg_to_all(message)

    # method for broadcasting messages to the each clients
    def msg_to_all(self, message):
        for client in self.clients:
            try:  # evitamos error cuando se ha cerrado un cliente
                client.send(message)
            except:
                self.clients.remove(client)


# call the method to begin the communication
Servidor()
