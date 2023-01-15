from socket import AF_INET, socket, SOCK_STREAM, error
from threading import Thread
import json
from tkinter import *


def send_img(client=socket, img_path=str):
    """
    Handles send the entire image in binary to a single client.
    ---------------------
    Input: Socket, String
    Output: None
    """

    with open(img_path, "rb") as img:
        img_data = img.read()
        # Sends image's size first
        img_sz = len(img_data)
        client.sendall(bytes(str(img_sz), "utf8"))
        try:
            # Then, sends image's data
            client.sendall(img_data)
        except error as e:
            MSG("Error sending image's data from the server: %s" %e)
            MSG("Byte stream at image: %s" %img_path)

def send_msg(client=socket, msg=str):
    """
    Handles send the entire message to a single client.
    ---------------------
    Input: Socket, String
    Output: None
    """

    byte_msg = bytes(msg, "utf8")
    # Sends message's size first
    msg_sz = len(byte_msg)
    client.sendall(bytes(str(msg_sz), "utf8"))
    try:
        # Then, sends the message
        client.sendall(byte_msg)
    except error as e:
        MSG("Error sending data from the server: %s" %e)
        MSG("Byte stream: %s" %msg)
        exit(0)

def on_new_client(client=socket):  
    """
    Handles a single client connection.
    ---------------------
    Input: Socket
    Output: None
    """
    

    # First message for testing connection
    name = client.recv(BUFSIZ).decode("utf8")
    send_msg(client, msg="Welcome back, %s!" % name)
    clients[client] = name

    # Sends and receives data loop
    while True:
        # Receives client's request
        msg = client.recv(BUFSIZ)
        if msg == bytes(ALL_MSG, "utf8"):
            # Sends id and fullname of members
            MSG("{} requests to get all members.".format(addresses[client]))
            # All members' id and full name are seperated by comma
            ans = ""
            for i in data:
                ans += i + "," + data[i]["fullname"] + ","
            ans = ans[:-1]
            send_msg(client, msg=ans)
        elif msg == bytes(B_AVATAR_MSG, "utf8"):
            # Sends id, fullname and big avatar of members
            MSG("{} requests to get all members' big avatar.".format(addresses[client]))
            # Sends the number of members first
            client.sendall(bytes(str(n_mems), "utf8"))
            for i in data:
                send_msg(client, msg=i + "," + data[i]["fullname"])
                # Postpones server's sending progression
                c_ans = client.recv(BUFSIZ)
                if c_ans != bytes(i, "utf8"):
                    MSG("Sending images progression is uncompleted!")
                    break
                # Sends his/her avatar
                send_img(client, img_path=data[i]["big"])
                # Postpones server's sending progression
                c_ans = client.recv(BUFSIZ)
                if c_ans != bytes(DONE_MSG, "utf8"):
                    MSG("Sending images progression is uncompleted!")
                    break
        elif msg == bytes(S_AVATAR_MSG, "utf8"):
            # Sends id, fullname and small avatar of members
            MSG("{} requests to get all members' small avatar.".format(addresses[client]))
            # Sends the number of members first
            client.sendall(bytes(str(n_mems), "utf8"))
            for i in data:
                send_msg(client, msg=i + "," + data[i]["fullname"])
                # Postpones server's sending progression
                c_ans = client.recv(BUFSIZ)
                if c_ans != bytes(i, "utf8"):
                    MSG("Sending images progression is uncompleted!")
                    break
                # Sends his/her avatar
                send_img(client, img_path=data[i]["small"])
                # Postpones server's sending progression
                c_ans = client.recv(BUFSIZ)
                if c_ans != bytes(DONE_MSG, "utf8"):
                    MSG("Sending images progression is uncompleted!")
                    break
        elif msg == bytes(QUIT_MSG, "utf8"):
            # Closes client's connect
            send_msg(client, msg="Goodbye. Have a nice day. See ya!")
            client.close()
            MSG("%s:%s has disconnected." % addresses[client])
            del clients[client]
            del addresses[client]
            break
        else:
            # Sends member's information based on id
            id = msg.decode("utf8")
            MSG("{} requests to get member has id={}.".format(addresses[client], id))
            # Member's information is seperated by comma
            ans = ""
            if id in data:
                # If the id requested is available
                ans = id + "," + data[id]["fullname"] + "," + data[id]["phone"] + "," + data[id]["email"]
            else:
                # If the id requested is not available
                ans = id + " is not found!"
            send_msg(client, msg=ans)

def accept_multiple_connections():
    """
    Sets up handling for incoming clients connection.
    ---------------------
    Input: None
    Output: None
    """

    while True:
        client, client_address = SERVER.accept()
        MSG("%s:%s has connected." % client_address)
        send_msg(client, msg="Your computer is connected to the server.")
        addresses[client] = client_address
        Thread(target=on_new_client, args=(client,)).start()

def MSG(str):
    global text
    text.config(state=NORMAL)
    text.insert(END, "\n" + str)
    text.pack()
    text.see(END)
    text.config(state=DISABLED)

def server_cl():
    SERVER.close()

def GUI():
    global gui
    global text

    # initialize tkinter object
    gui = Tk()
    # set title for the window
    gui.title("Server")
    # set size for the window
    gui.geometry("600x400+770+150")

    text = Text(gui, font=('Comic Sans MS', 12))

    frame = Frame(gui)
    frame.pack(side = LEFT)

    button1 = Button(frame, text="EXIT", fg="blue", command=server_cl)
    button1.pack( side = LEFT )

    SERVER.listen(5)
    text.config(state=NORMAL)
    text.insert(END, "Waiting for connection...")
    text.pack()
    text.see(END)
    text.config(state=DISABLED)
    ACCEPT_THREAD = Thread(target=accept_multiple_connections)
    ACCEPT_THREAD.start()
    gui.mainloop()
    ACCEPT_THREAD.join()
    SERVER.close()


# Global variables
clients = {}
addresses = {}

# Constants
HOST = "localhost"
PORT = 33000
BUFSIZ = 1024*2
ADDR = (HOST, PORT)

# Database
DATA_PATH = "data.json"
try:
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
        n_mems = len(data) # Count keys
except:
    MSG("Cannot open {}".format(DATA_PATH))

# Messages
ALL_MSG = "all" # Retrieve all members' information message
QUIT_MSG = "quit" # Client closes connection
B_AVATAR_MSG = "big" # Retrieve all members' big avatar message
S_AVATAR_MSG = "small" # Retrieve all members' small avatar message

DONE_MSG = "done"

# Server
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    GUI()