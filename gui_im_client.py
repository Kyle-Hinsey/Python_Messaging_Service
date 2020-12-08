# Kyle Hinsey, CIS 345, TTh 12:00, A8
from tkinter import *
from tkinter import messagebox
from socket import *
from threading import Thread


def connect_func():
    """will create socket and connect to the chat_server"""
    global ip_var, sname_var, connect_btn, chat_frame, client_socket
    # test to see if there is a valid IP and some type of screen name
    if len(ip_var.get()) > 6 and len(sname_var.get()) > 0:
        # create addr and socket object
        ADDR = (ip_var.get(), 49000)
        client_socket = socket(AF_INET, SOCK_STREAM)
        # try statement to connect to the server
        try:
            client_socket.connect(ADDR)
            client_socket.send(sname_var.get().encode())
        except:
            client_socket.close()
            client_socket = None
        else:
            # if try successful create a thread
            x = Thread(target=receive_func, daemon=True)
            x.start()
        # change the appearance and functionality of the conncect btn
        connect_btn.config(bg="gold", fg="black", command=disconnect_func, text="Disconnect")
        # add frame to window
        chat_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    # if there is an error with the ip or screen name
    else:
        messagebox.showinfo("Error", "Please enter in an appropriate IP address and/or a Screen Name")


def disconnect_func():
    """will disconnect from the server and reformat the window"""
    global client_socket, chat_frame, ip_var, sname_var, connect_btn, win, message_var
    # send exit code to server
    try:
        client_socket.send('[Q]'.encode())
    except:
        pass
    finally:
        # close socket and set it equal to none
        client_socket.close()
        client_socket = None
    # change format and functionality of the button
    connect_btn.config(bg='maroon', fg='white', text='Connect', command=connect_func)
    # remove chat box frame
    chat_frame.grid_forget()
    # set the message to a blank string
    message_var.set("")


def event_handler_key(event):
    """will only allow certain key to be pressed when entering the IP Address"""
    global ip_var, ip_txt
    valid_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '\b', '']
    # break if not a valid key
    if event.char not in valid_keys:
        return "break"


def receive_func():
    """will allow the client to receive messages from other clients and the server"""
    global client_socket, sname_var, chat_box
    # infinite loop
    while True:
        try:
            # try to receive a message
            receive_message = client_socket.recv(1024)
        except:
            receive_message = None
            break
        else:
            # add message to the end of the listbox
            chat_box.insert(END, receive_message.decode())


def send_func():
    """send messages to the server"""
    global client_socket, message_var
    # store message in a variable
    message_send = message_var.get()
    if message_send == '[Q]':
        # call discount if entered exit key
        disconnect_func()
    elif message_send != "":
        # try to send message if not blank
        try:
            client_socket.send(message_send.encode())
        except OSError:
            disconnect_func()
        finally:
            message_var.set("")


def window_closing():
    """close the window and discount sock if there is one"""
    global client_socket, win
    if client_socket:
        disconnect_func()
    win.quit()

# create window
win = Tk()
win.title("A8 - Kyle Hinsey")

# Variables
ip_var = StringVar()
sname_var = StringVar()
message_var = StringVar()
client_socket = None

# IP Address label and Entry Box
ip_lbl = Label(win, text="Server IP:")
ip_lbl.grid(row=0, column=0, sticky=W, padx=(10, 0), pady=5)
ip_txt = Entry(win, textvariable=ip_var, width=50)
ip_txt.grid(row=0, column=1, sticky=E, padx=(0, 10), pady=5)
ip_txt.bind('<Key>', event_handler_key)

# Screen Name label and Entry Box
sname_lbl = Label(win, text="Screen Name:")
sname_lbl.grid(row=1, column=0, sticky=W, padx=(10, 0), pady=5)
sname_txt = Entry(win, textvariable=sname_var, width=50)
sname_txt.grid(row=1, column=1, sticky=E, padx=(0, 10), pady=5)

# Connect/Disconnect Button
connect_btn = Button(win, text="Connect", width=55, bg="maroon", fg="white", command=connect_func)
connect_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# Frame where the chat box, message box, and send btn will go
chat_frame = Frame(win, bg='maroon')

# chat box with the scroll bar
chat_scrbar_frame = Frame(chat_frame)
chat_scrbar_frame.grid(row=0, column=0, columnspan=2, padx=7, pady=7)
scrollbar = Scrollbar(chat_scrbar_frame)
chat_box = Listbox(chat_scrbar_frame, yscrollcommand=scrollbar.set, width=62)
scrollbar.config(command=chat_box.yview)
chat_box.pack(side=LEFT)
scrollbar.pack(side=RIGHT, ipady=58)

# message box to send messages
message_txt = Entry(chat_frame, textvariable=message_var, width=50)
message_txt.grid(row=1, column=0, sticky=W, padx=(7, 0), pady=(3, 7))

# send button to send messages to the server
send_btn = Button(chat_frame, text='Send', bg='gold', command=send_func)
send_btn.grid(row=1, column=1, sticky=E, padx=(0, 7), pady=(3, 7))

# will close and program and any sockets opened
win.protocol("WM_DELETE_WINDOW", window_closing)

win.mainloop()
# end application
