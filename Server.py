import socket
import threading
import tkinter as tk

window = tk.Tk()
window.title("Sever")

#The top frame has to buttons: t Start and Stop
topFrame = tk.Frame(window)
buttonStart = tk.Button(topFrame, background="#B57EDC", text="Connect", command=lambda : start_server())
buttonStart.pack(side=tk.LEFT)
buttonStop = tk.Button(topFrame, background="#B57EDC", text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
buttonStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

#Middle frame consists two labels to display host and port information
middleFrame = tk.Frame(window)
labelHost = tk.Label(middleFrame, text = "Host: X.X.X.X")
labelHost.pack(side=tk.LEFT)
labelPort = tk.Label(middleFrame, text = "Port:XXXX")
labelPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

#The user frame shows the user area
userFrame = tk.Frame(window)
labelLine = tk.Label(userFrame, text="------------Users List------------").pack()
scrollBar = tk.Scrollbar(userFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(userFrame, height=15, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#C08081", highlightbackground="#52307C", state="disabled")
userFrame.pack(side=tk.BOTTOM, pady=(5, 10))


server = None
HOST_ADDR = "27.0.0.0"
HOST_PORT = 9090
user_name = " "
user = []
user_names = []


#Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT 
    buttonStart.config(state=tk.DISABLED)
    buttonStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print (socket.AF_INET)
    print (socket.SOCK_STREAM)
    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  

    threading._start_new_thread(accept_users, (server, " "))

    labelHost["text"] = "Host: " + HOST_ADDR
    labelPort["text"] = "Port: " + str(HOST_PORT)


#Stop server function
def stop_server():
    global server
    buttonStart.config(state=tk.NORMAL)
    buttonStop.config(state=tk.DISABLED)


def accept_users(the_server, y):
    while True:
        user, addr = the_server.accept()
        user.append(user)

        # use a thread so as not to clog the gui thread
        threading._start_new_thread(send_receive_user_message, (user, addr))


#To receive message from current user
#Amd send that message to other contacts
def send_receive_user_message(user_connection, user_ip_addr):
    global server, user_name, user, user_addr
    user_msg = " "

    user_name  = user_connection.recv(4096)
    user_connection.send("Its so good to see you here " + user_name + "! :) Use 'exit' to quit")

    user_names.append(user_name)

    update_user_names_display(user_names)


    while True:
        data = user_connection.recv(4096)
        if not data: break
        if data == "exit": break

        user_msg = data

        idx = get_user_index(user, user_connection)
        sending_user_name = user_names[idx]

        for u in user:
            if u != user_connection:
                u.send(sending_user_name + "->" + user_msg)

    #Find the user index then remove from both lists
    idx = get_user_index(user, user_connection)
    del user_names[idx]
    del user[idx]
    user_connection.send("Tussi Jaa Rahe Ho? Theek, Koi Nahi :(")
    user_connection.close()
    update_user_names_display(user_names)  


def get_user_index(user_list, curr_user):
    idx = 0
    for conn in user_list:
        if conn == curr_user:
            break
        idx = idx + 1

    return idx


# Update name display when a new user connects or disconnects
def update_user_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for u in name_list:
        tkDisplay.insert(tk.END, u+"\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()
