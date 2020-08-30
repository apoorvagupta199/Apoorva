import socket
import threading
import tkinter as tk
from tkinter import messagebox


window = tk.Tk()
window.title("User")
user_name = " "

topFrame = tk.Frame(window)
labelName = tk.Label(topFrame, text = "Name:-").pack(side=tk.LEFT)
entryName = tk.Entry(topFrame)
entryName.pack(side=tk.LEFT)
buttonConnect = tk.Button(topFrame, text="Connect", command=lambda : connect())
buttonConnect.pack(side=tk.LEFT)

topFrame.pack(side=tk.TOP)

displayFrame = tk.Frame(window)
labelLine = tk.Label(displayFrame, text="Welcome aboard to Shinchan Chatroom! ").pack()
scrollBar = tk.Scrollbar(displayFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(displayFrame, height=20, width=55)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
tkDisplay.tag_config("tag_your_message", foreground="#89CFF0")
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#C08081", highlightbackground="#52307C", state="disabled")
displayFrame.pack(side=tk.TOP)


bottomFrame = tk.Frame(window)
tkMessage = tk.Text(bottomFrame, height=2, width=55)
tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
tkMessage.config(highlightbackground="#52307C", state="disabled")
tkMessage.bind("<Return>", (lambda event: getChatMessage(tkMessage.get("1.0", tk.END))))
bottomFrame.pack(side=tk.BOTTOM)


def connect():
    global user_name, user
    if len(entryName.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You must enter your first name (e.g. Apoorva)!")
    else:
        user_name = entryName.get()
        connect_to_server(user_name)


# User Network
user = None
HOST_ADDR = "27.0.0.0"
HOST_PORT = 9090

def connect_to_server(name):
    global user, HOST_PORT, HOST_ADDR
    try:
        user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        user.connect((HOST_ADDR, HOST_PORT))
        user.send(name) # For sending name to the server, after connecting

        entryName.config(state=tk.DISABLED)
        buttonConnect.config(state=tk.DISABLED)
        tkMessage.config(state=tk.NORMAL)

        # For receiving messages from server
        threading._start_new_thread(receive_message_from_server, (user, "m"))
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Unable to connect to the host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later!")


def receive_message_from_server(sck, m):
    while True:
        from_server = sck.recv(4096)

        if not from_server: break

        # Display message on the chat window recieved from the server

        # Enable the display area and insert the text and then disable.
        texts = tkDisplay.get("1.0", tk.END).strip()
        tkDisplay.config(state=tk.NORMAL)
        if len(texts) < 1:
            tkDisplay.insert(tk.END, from_server)
        else:
            tkDisplay.insert(tk.END, "\n\n"+ from_server)

        tkDisplay.config(state=tk.DISABLED)
        tkDisplay.see(tk.END)

        print("Server says: " +from_server)

    sck.close()
    window.destroy()


def getChatMessage(msg):

    msg = msg.replace('\n', '')
    texts = tkDisplay.get("1.0", tk.END).strip()

    tkDisplay.config(state=tk.NORMAL)
    if len(texts) < 1:
        tkDisplay.insert(tk.END, "You->" + msg, "tag_your_message") # no line
    else:
        tkDisplay.insert(tk.END, "\n\n" + "You->" + msg, "tag_your_message")

    tkDisplay.config(state=tk.DISABLED)

    send_mssage_to_server(msg)

    tkDisplay.see(tk.END)
    tkMessage.delete('1.0', tk.END)


def send_mssage_to_server(msg):
    user.send(msg)
    if msg == "exit":
        user.close()
        window.destroy()
    print("Sending message")


window.mainloop()




