from importlib.util import LazyLoader
from linecache import lazycache
from re import T
import sys
from socket import AF_INET, socket, SOCK_STREAM, error, gaierror
from tkinter import *
from tracemalloc import start
from turtle import undo
from tkinter import filedialog
from PIL import Image,ImageTk
from functools import partial
import tkinter as tk

def recv_msg(client=socket, total=int) -> bytearray:
    """
    Handles receiving entire message.
    ---------------------
    Input: Socket, Int
    Output: Bytearray
    """

    msg = bytearray(total)
    view = memoryview(msg)
    sz = 0
    while sz < total:
        n = client.recv_into(view[sz:], total - sz)
        sz += n
    return msg

def receive_msg(client=socket) -> str:
    """
    Handles receiving messages.
    ---------------------
    Input: Socket
    Output: String
    """

    # Receives length of the message first
    msg_sz = int(client.recv(NUMBUF).decode("utf8"))
    try:
        # Then, receives the message
        msg = recv_msg(client, msg_sz).decode("utf8")
    except error as e:
        MSG ("Error receiving data: %s" %e)
        sys.exit(1)
    return msg

# Images' filename created while receiving over socket
b_base = "b%s.png"
s_base = "s%s.png"

def recv_img(client=socket, img_path=str):
    """
    Handles receiving the image in binary and write on file.
    ---------------------
    Input: Socket, String
    Output: None
    """

    # Receives size of the image first
    img_sz = int(client.recv(NUMBUF).decode("utf8"))
    # Then, receives the image
    img_data = recv_msg(client, img_sz)
    # Saves the image
    with open(img_path, "wb") as img:
        img.write(img_data)


def receive_img(client=socket, type=True):
    """
    Handles receiving images.
    ---------------------
    Input: Socket, Boolean (True <-> Small Avatars || False <-> Big Avatars)
    Output: None
    """

    # Receives the number of images
    n = int(client.recv(NUMBUF).decode("utf8"))
    global text
    global imgs
    while n > 0:
        # Receives id and full name
        mem_info = receive_msg(client)
        id, fname = mem_info.split(",")
        global list_name
        list_name.append(str(id) + " - " + str(fname))
        #MSG("{} - {}".format(id, fname))
        send(client, msg=id)
        # Receives images
        try:
            if type == True:
                img_name = s_base % id
            else:
                img_name = b_base % id
            recv_img(client, img_name)
            global list_link
            list_link.append(img_name)
            # photo = PhotoImage(file = img_name)

            # # Resize image to fit on button
            # photoimage = photo.subsample(20,20)

            # # Position image on button
            # Im = text.image_create(END, image = photoimage)
            # Im.pack()
        except error as e:
            MSG ("Error receiving image's data: %s" %e)
            sys.exit(1)
        else:
            send(client, msg=DONE_MSG)
            n -= 1

            
def send(client=socket, msg=str):
    """
    Handles sending messages.
    ---------------------
    Input: Socket, String
    Output: None
    """

    client.sendall(bytes(msg, "utf8"))

def add_img():
    global text1
    global img_lienket
    global img1
    global imgs
    text1.config(state=NORMAL)
    img1 = ImageTk.PhotoImage(Image.open(img_lienket))
    imgs.append(img1)
    text1.image_create(INSERT, image = img1, align = BOTTOM)
    text1.pack()
    text1.config(state=DISABLED)

def add_img2():
    global text2
    global img_lienket
    global img1
    global imgs
    text2.config(state=NORMAL)
    img1 = ImageTk.PhotoImage(Image.open(img_lienket))
    imgs.append(img1)
    text2.image_create(INSERT, image = img1, align = BOTTOM)
    text2.pack()
    text2.config(state=DISABLED)

def data_tranfer(msg=str): # Test function
    try:
        send(client_socket, msg)
    except error as e:
        MSG ("Error sending data: %s" %e)
        sys.exit(1)
    else: # When there is no error.
        if msg == S_AVATAR_MSG: 
            receive_img(client_socket, True)
        elif msg == B_AVATAR_MSG:
            receive_img(client_socket, False)
        else:
            global list_info
            s = receive_msg(client_socket)
            list_info.append(s)
            MSG(s)

global Str
Str = ""

global dd_person
dd_person = 0

def Sol(event):
    global Str
    print(Str)
    global text
    global img_b
    global dd_person
    if dd_person == 0:
        global Varr
        Varr.set(1)
    dd_person = 0
    img_b = str("b" + Str +".png")
    if Str == "all": 
        text.config(state=NORMAL)
        text.edit_undo()
        text.edit_undo()
        text.edit_undo()
        text.config(state=DISABLED)
        all_m()
        return
    MSG("")
    data_tranfer(Str)
    Str = ""
    text.config(state=NORMAL)
    text.insert(INSERT, "Enter your command: ")
    text.config(state=DISABLED)

def Query(event):
    global text
    global Str
    if event.char == '\b':
        Str = Str[:-1]
        text.config(state=NORMAL)
        text.edit_undo()
        text.config(state=DISABLED)
        return
    Str = Str + event.char
    text.config(state=NORMAL)
    text.edit_separator()
    text.insert(INSERT, event.char)
    #text.edit_separator()
    text.pack()
    #text.see(END)
    text.config(state=DISABLED)
    #if Str == "quit": exit(0)

def MSG(str):
    global text
    text.config(state=NORMAL)
    text.insert(END, str + "\n")
    text.pack()
    text.see(END)
    text.config(state=DISABLED)

def MSG1(str):
    global text1
    text1.config(state=NORMAL)
    text1.insert(END, str + "\n")
    text1.pack()
    text1.see(END)
    text1.config(state=DISABLED)

def next_img():
    global text1
    global i
    global img_size
    i = i + 1
    if i == -1: i = img_size - 1
    if i == img_size: i = 0
    global list_name
    #img_namenow = list_name[i]
    global list_link
    global img_lienket
    img_lienket = list_link[i]
    #MSG1(img_namenow)
    text1.config(state=NORMAL)
    text1.destroy()
    text1 = Text(ui, font=('Comic Sans MS', 12), undo = True)
    img_now = str(list_name[i])
    text1.insert(INSERT, img_now + "\n")
    text1.pack()
    text1.config(state=DISABLED)
    add_img()

def prev_img():
    global text1
    global i
    global img_size
    i = i - 1
    if i == -1: i = img_size - 1
    if i == img_size: i = 0
    global list_name
    #img_namenow = list_name[i]
    global list_link
    global img_lienket
    img_lienket = list_link[i]
    #MSG1(img_namenow)
    text1.config(state=NORMAL)
    text1.destroy()
    text1 = Text(ui, font=('Comic Sans MS', 12), undo = True)
    img_now = str(list_name[i])
    text1.insert(INSERT, img_now + "\n")
    text1.pack()
    text1.config(state=DISABLED)
    add_img()

def process2(host1, port1):
    global PORT
    global HOST
    HOST = str(host1.get())
    PORT = int(port1.get())
    #ui1.update()
    return

def disable_event():
   pass

def inp_sv():
    global ui1
    ui1 = Toplevel(gui)
    ui1.protocol("WM_DELETE_WINDOW", disable_event)
    ui1.grab_set() 
    global lay
    lay.append(ui1)
    ui1.geometry('400x150+610+20')
    ui1.title("FORM") 

    global process2

    hostLabel = Label(ui1, text="HOST").grid(row=0, column=0)
    host1 = StringVar()
    hostEntry = Entry(ui1, textvariable=host1).grid(row=0, column=1)

    portLabel = Label(ui1,text="PORT").grid(row=1, column=0)  
    port1 = StringVar()
    portEntry = Entry(ui1, textvariable=port1).grid(row=1, column=1)

    process2 = partial(process2, host1, port1)
    #process2 = IntVar()

    global Buttonok
    Buttonok = Button(ui1, text="CONNECT", command=process2).grid(row=4, column=0) 
    var = tk.IntVar()
    global Buttonok1
    Buttonok1 = tk.Button(ui1, text="QUIT", command=lambda: var.set(1))
    Buttonok1.place(relx=.9, rely=.1, anchor="c")

    Buttonok1.wait_variable(var)
    ui1.destroy()


def create_inf():#tao window infor
    
    global ui
    ui = Toplevel(gui)

    #lay.append(ui)

    # set size for the window
    ui.geometry("900x500+150+100")

    # set title
    ui.title("Infomation")

    frame1 = Frame(ui)
    frame1.pack(side = LEFT)

    frame2 = Frame(ui)
    frame2.pack(side = RIGHT)

    global text1

    text1 = Text(ui, font=('Comic Sans MS', 12), undo = True)
    text1.config(state=DISABLED)

    photo = PhotoImage(file="icon/right.png")

    button1 = Button(frame2, image=photo, command=next_img)
    button1.pack( side = RIGHT)

    photo1 = PhotoImage(file="icon/left.png")

    button2 = Button(frame1, image=photo1, command=prev_img)
    button2.pack( side = LEFT )
    button2.image=photo1

    global i
    i = 0
    global img_size
    global list_name
    global list_link
    global img_lienket
    img_size = len(list_link)
    img_namenow = str(list_name[0])
    if img_size == 0: return
    img_lienket = list_link[0]
    text1.config(state=NORMAL)
    text1.insert(INSERT, img_namenow + "\n")
    text1.pack()
    text1.config(state=DISABLED)
    add_img()
    ui.mainloop()


def all_m():
    global list_link
    global list_name
    list_link.clear()
    list_name.clear()
    global Str 
    global text
    Str = "small"
    MSG("all")
    data_tranfer(Str)
    Str = ""
    text.config(state=NORMAL)
    text.insert(END, "Enter your command: ")
    text.pack()
    text.see(END)
    text.config(state=DISABLED)
    create_inf()

def small_m():
    global list_link
    global list_name
    list_link.clear()
    list_name.clear()
    global Str 
    global text
    Str = "small"
    MSG("small")
    data_tranfer(Str)
    Str = ""
    text.config(state=NORMAL)
    text.insert(END, "Enter your command: ")
    text.pack()
    text.see(END)
    text.config(state=DISABLED)
    create_inf()

def big_m1():
    global list_link
    global list_name
    list_link.clear()
    list_name.clear()
    global Str 
    global text
    Str = ""
    MSG("big")
    text.config(state=NORMAL)
    text.insert(END, "Enter the code: ")
    text.config(state=DISABLED)

def create_inf1(linkk):#tao window infor
    
    global ui2
    ui2 = Toplevel(gui)

    # set size for the window
    ui2.geometry("900x500+150+100")

    # set title
    ui2.title("Infomation")

    global text2

    text2 = Text(ui2, font=('Comic Sans MS', 12), undo = True)
    text2.config(state=DISABLED)

    global list_info
    global img_lienket
    img_namenow = str(list_info[len(list_info) - 1])
    img_lienket = linkk
    text2.config(state=NORMAL)
    text2.insert(INSERT, img_namenow + "\n")
    text2.pack()
    text2.config(state=DISABLED)
    add_img2()
    ui2.mainloop()

def big_m2():
    global Str 
    data_tranfer("big")
    global img_b
    create_inf1(img_b)

def big_m():
    global Varr
    global text
    Varr = IntVar()
    big_m1()
    text.wait_variable(Varr)
    big_m2()

def quit_m():
    global list_link
    global list_name
    list_link.clear()
    list_name.clear()
    global Str 
    global text
    Str = "quit"
    MSG("quit")
    data_tranfer(Str)

def person_m():
    global dd_person
    dd_person = 1
    global list_link
    global list_name
    list_link.clear()
    list_name.clear()
    global Str 
    global text
    Str = ""
    MSG("person")
    text.config(state=NORMAL)
    text.insert(END, "Enter the code: ")
    text.config(state=DISABLED)

# initialize tkinter object
gui = Tk()

# set title for the window
gui.title("Client")
# set size for the window
gui.geometry("600x400+50+150")

global text
global img1
global img_lienket
global imgs
global list_name
global list_link
global text1
global lay
global list_info
global img_b

list_info = []
imgs = []
list_name = []
list_link = []
lay = []

text = Text(gui, font=('Comic Sans MS', 12), undo = True)
text.config(state=DISABLED)

frame = Frame(gui)
frame.pack(side = LEFT)

button1 = Button(frame, text="ALL", fg="blue", command=all_m, height = 3, width = 6)
button1.pack( side = TOP )

button2 = Button(frame, text="SMALL", fg="blue", command=small_m, height = 3, width = 6)
button2.pack( side = TOP )

button3 = Button(frame, text="BIG", fg="blue", command=lambda: [big_m()], height = 3, width = 6)
button3.pack( side = TOP )

button5 = Button(frame, text="PERSON", fg="blue", command=person_m, height = 3, width = 6)
button5.pack( side = TOP )

button4 = Button(frame, text="QUIT", fg="blue", command=quit_m, height = 3, width = 6)
button4.pack( side = TOP )

gui.bind('<Return>', Sol)
gui.bind('<Key>', Query)


# Messages
ALL_MSG = "all" # Retrieve all members' information message
QUIT_MSG = "quit" # Client closes connection
B_AVATAR_MSG = "big" # Retrieve all members' big avatar message
S_AVATAR_MSG = "small" # Retrieve all members' small avatar message

DONE_MSG = "done"

#----Now comes the sockets part----
#HOST = input('Enter host: ')
#PORT = input('Enter port: ')
#

MSG("all: Retrieve all members' information")
MSG("quit: Close connection")
MSG("big: Retrieve big avatar of all member")
MSG("small: Retrieve small avatar of all member")
MSG("person: Retrieve one member's information using their ID")

HOST = "localhost"
PORT = 33000

inp_sv()

#print(HOST, PORT)

#ui1.grab_release() 

if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)
NUMBUF = 8
BUFSIZ = 1024*2
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
try:
    client_socket.connect(ADDR)
except gaierror as e:
    MSG ("Address-related error connecting to server: %s" %e)
    sys.exit(1)
except error as e:
    MSG ("Connection error: %s" %e)
    sys.exit(1)

# Status of Connection to the server 
status = receive_msg(client_socket)
MSG(str(status))

# Server welcomes Client
send(client_socket, msg="Woman coffee")
welcome = receive_msg(client_socket)
MSG(str(welcome))

text.config(state=NORMAL)
text.insert(END, "Enter your command: ")
text.pack()
text.see(END)
text.config(state=DISABLED)

gui.mainloop()

client_socket.close()