import sys
from socket import socket, AF_INET, SOCK_DGRAM
import requests
import PIL.Image
from PIL import ImageTk
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import time
import threading
I_C=-1
SERVER_IP   = '127.0.0.1'
PORT_NUMBER = 5000
SIZE = 1024
print ("Test client sending packets to IP {0}, via port {1}\n".format(SERVER_IP, PORT_NUMBER))

mySocket = socket( AF_INET, SOCK_DGRAM )
myMessage = "Hello!"
myMessage1 = ""
i = 0
while i < 10:
    mySocket.sendto(myMessage.encode('utf-8'),(SERVER_IP,PORT_NUMBER))
    i = i + 1

mySocket.sendto(myMessage1.encode('utf-8'),(SERVER_IP,PORT_NUMBER))
data,addr = mySocket.recvfrom(1024)
img_link = data.decode()
r = requests.get(img_link,allow_redirects=True)
open('img.jpg','wb').write(r.content)
ans,addr=mySocket.recvfrom(1024);


def addtohistory():
    global I_C
    I_C=I_C +1
    mySocket.sendto(inp.get().encode('utf-8'),(SERVER_IP,PORT_NUMBER))
    # bit,addr=mySocket.recvfrom(1024)
    msg,addr=mySocket.recvfrom(1024)
    msg = msg.decode()
    listbox.insert(END, msg)
    # print(msg ,"\n", inp.get())
    if msg!=inp.get():
        listbox.itemconfig(I_C,{'fg':'Green'})
    inp.delete(0, END)

def updatetime():
    t = 10
    global my_var
    my_var.set(str(t))
   
    while(t!=0):
        root.update()
        t = t-1
        my_var.set(str(t))
        time.sleep(1)
    mySocket.sendto(('__').encode('utf-8'),(SERVER_IP,PORT_NUMBER))
    correct,addr = mySocket.recvfrom(1024)
    # correct = correct.decode()

    messagebox.showinfo('TIMES UP!','Answer = '+correct.decode()) 

root = Tk()  # create root window
my_var = StringVar()
fontObj = tkFont.Font(size=28)
fontObj1 = tkFont.Font(size=35)
root.title("Basic GUI Layout")  # title of the GUI window
root.maxsize(1300, 1300)  # specify the max size the window can expand to
root.config(bg="#b7e2f3")  # specify background color

# Create left,right and top frames
top_frame = LabelFrame(root, text="Guess the Prompt", width=800, height=100) 
top_frame.grid(row=0, column=0, padx=10, pady=10)
user_name = Label(top_frame,text = ans, font=fontObj).grid(row=0,column=0, padx=10, pady=10)
timr = Label(top_frame,textvariable=my_var,fg='Red', font=fontObj1)
timr.grid(row = 0,column=1, padx=10, pady=10)
subframe= Frame(root, width = 700, height= 400)
subframe.grid(row=1, column=0, padx=10, pady=10)

left_frame = LabelFrame(subframe, text="Image:", width=450, height=300)
left_frame.grid(row=0, column=0, padx=2, pady=2)

right_frame = LabelFrame(subframe, text="Chat", width=200, height=500)
right_frame.grid(row=0, column=1, padx=2, pady=2)

history = Frame(right_frame, width=350, height=400, bg='#E2E5DE')
history.grid(row=0, column=0)

inpframe = Frame(right_frame, width=200, height=400)
inpframe.grid(row=1, column=0, padx=1, pady=1)

inp = Entry(inpframe, width=50)
inp.grid(row=1, column=0, padx=1, pady=1)

send = Button(inpframe, text="Submit", bg='#E2E5DE', command=addtohistory)
send.grid(row=1, column=1, padx=1, pady=1)

# load image to be "edited"
image  = PIL.Image.open("img.jpg")
resize_image = image.resize((450,500))
img = ImageTk.PhotoImage(resize_image)
# Display image in right_frame
Label(left_frame, image=img).grid(row=0,column=0, padx=5, pady=5)


listbox = Listbox(history, width=55, height=30)
  
# Adding Listbox to the left
# side of root window
listbox.pack(side = LEFT, fill = BOTH, expand=True)
  
# Creating a Scrollbar and 
# attaching it to root window
scrollbar = Scrollbar(history)
  
# Adding Scrollbar to the right
# side of root window
scrollbar.pack(side = RIGHT, fill = BOTH) 
      
listbox.config(yscrollcommand = scrollbar.set)
  
scrollbar.config(command = listbox.yview)
t1 = threading.Thread(target=updatetime)
t1.start()
root.mainloop()