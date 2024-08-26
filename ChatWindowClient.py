# Chat window - client program

import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

HEADER = 64
PORT = 5069
FORMAT = 'UTF-8'
SERVER = '138.68.140.83'
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def sendMessage():
    global inputField
    global client
    msg = inputField.get()
    if msg:
        clientName = "Naga Lakshmi"
        formattedMessage = f"{clientName}: {msg}\n"
        message = formattedMessage.encode(FORMAT)
        messageLength = len(message)
        sendLength = str(messageLength).encode(FORMAT)
        sendLength += b' ' * (HEADER - len(sendLength))
        client.send(sendLength)
        client.send(message)
        inputField.delete(0, tk.END)

def receiveMessage():
    global chatArea
    global client
    global root
    while True:
        try:
            message = client.recv(2048).decode(FORMAT)
            if message:
                chatArea.config(state=tk.NORMAL)
                chatArea.insert(tk.END, message)
                chatArea.config(state=tk.DISABLED)
            if 'bye' in message.lower():
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
    root.quit()

def onClosing():
    global client
    try:
        client.send(f"{clientName}left the chat.".encode(FORMAT))
    except:
        pass
    client.close()
    root.quit()

def makeGUI():
    global chatArea
    global inputField
    global root
    root = tk.Tk()
    root.title("Chat Window")
    root.geometry("400x500")

    chatArea = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
    chatArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    inputField = tk.Entry(root)
    inputField.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10), fill=tk.X, expand=True)

    sendButton = tk.Button(root, text="Send", command=sendMessage)
    sendButton.pack(side=tk.RIGHT, padx=(0, 10), pady=(0, 10))

    root.bind('<Return>', lambda event: sendMessage())

    receive_thread = threading.Thread(target=receiveMessage, daemon=True)
    receive_thread.start()

    root.protocol("WM_DELETE_WINDOW", onClosing)
    root.mainloop()

makeGUI()
