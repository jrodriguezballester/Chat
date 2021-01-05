import socket
import threading
from tkinter import *
from datetime import datetime
import time

PORT = 4000
# poner Direccion IP del servidor - localhost
SERVER = "192.168.1.47"


ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"

# Create a new client socket and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(ADDRESS)
except Exception as e:
    print ("No se conecta al servidor. Posibles causas: Servidor no ejecutado; direccion IP incorrecta")


# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self):


        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()

        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=200)
        # create a Label
        label_intro = Label(self.login, text="Please login to continue", justify=CENTER, font="Helvetica 14 bold")

        # create a Label
        label_name = Label(self.login, text="Name: ", font="Helvetica 12")

        # create a entry box for tyoing the message
        entry_name = Entry(self.login, font="Helvetica 14")

        # create a Continue Button along with action
        button_continue = Button(self.login, text="NEXT", font="Helvetica 14 bold",
                                 command=lambda: self.goAhead(entry_name.get()))
        # set the focus of the curser
        entry_name.focus()
        # posicionar
        label_intro.place(relx=0.2, rely=0.1)
        label_name.place(relx=0.1, rely=0.35)
        entry_name.place(relx=0.25, rely=0.35)
        button_continue.place(relx=0.4, rely=0.65)

        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)

        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    # The main layout of the chat
    def layout(self, name):

        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="#17202A")

        label_head = Label(self.Window, bg="#17202A", fg="#EAECEE", text=self.name, font="Helvetica 13 bold", pady=5)

        label_line = Label(self.Window, bg="red")

        self.textCons = Text(self.Window, width=20, height=2, bg="#17202A", fg="#EAECEE", font="Helvetica 11")
        self.textCons.tag_configure('tuMensaje', foreground="#EAECEE", justify='left')
        self.textCons.tag_configure('miMensaje', foreground='green', justify='right')

        label_bottom = Label(self.Window, bg="#adfEEE", height=60)

        self.entryMsg = Entry(label_bottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")

        self.entryMsg.focus()

        # create a Send Button
        button_send = Button(label_bottom, text="Send", font="Helvetica 10 bold", width=20, bg="#ABB2B9",
                             command=lambda: self.sendButton(self.entryMsg.get()))

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(cursor="arrow", state=DISABLED)

        # place the given widget into the gui window
        label_head.place(relwidth=1)
        label_line.place(relwidth=1, rely=0.07, relheight=0.012)
        label_bottom.place(relwidth=1, rely=0.825)
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)
        scrollbar.place(relheight=1, relx=0.974)

        # place the given widget into the label_bottom
        button_send.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        self.entryMsg.place(relx=0.011, rely=0.008, relheight=0.06, relwidth=0.74)

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.msg = msg

        self.textCons.config(state=DISABLED)
        self.entryMsg.delete(0, END)

        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    # function to receive messages
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)

                # if the messages from the server is NAME send the client's name
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:

                    nombre = message.split(':')[0]
                    text = datetime.now().strftime("%Y-%m-%d %H:%m")

                    self.textCons.config(state=NORMAL)  # insert messages to text box

                    if nombre == self.name:
                        self.textCons.insert(END, text + "   .\n" + message.split(':')[1] + "    .\n\n", 'miMensaje')
                    else:
                        self.textCons.insert(END, text + "\n" + message + "\n\n", 'tuMensaje')

                    self.textCons.config(state=DISABLED)  # no permite entrada de texto
                    self.textCons.see(END)  # posicion visible si es mas grande del Text
            except Exception as e:
                # print(e)
                print("An error occured!")
                client.close()
                break

    # function to send messages
    def sendMessage(self):

        self.textCons.config(state=DISABLED)
        while True:
            message = f"{self.name}: {self.msg}"
            client.send(message.encode(FORMAT))
            break


# create a GUI class object
g = GUI()
