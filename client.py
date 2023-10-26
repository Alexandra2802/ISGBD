
import socket
from tkinter import *

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "Disconnect"

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    #receive message from server
    resp_length = client.recv(HEADER).decode(FORMAT)
    if resp_length:
        resp_length = int(resp_length)
        resp = client.recv(resp_length).decode(FORMAT)
    return resp

# def update_result_label():
#     my_string_var.set(receive())





#GUI
# root = Tk()

# label = Label(root, text="Enter SQL query")
# label.grid(row=0, column=0)

# e = Entry(root, width=35)
# e.grid(row=1, column=0,columnspan=2)
# my_string_var = StringVar()

# submit_button = Button(root, text="Submit", command=lambda: [send(e.get()), e.delete(0,END),update_result_label()])
# submit_button.grid(row=2, column=0)

# result_label = Label(root, textvariable=my_string_var)
# result_label.grid(row=3, column=0)

# database_name_label = Label(text='Database Name')
# database_name_label.grid(row=4,column=0)
# database_name_entry = Entry(root, width=35)
# database_name_entry.grid(row=4,column=1)
# create_database_button = Button(root, text='Create Database',command=lambda: [send('CREATE DATABASE '+ database_name_entry.get()), 
#                                                                               database_name_entry.delete(0,END),
#                                                                               update_result_label()])
# create_database_button.grid(row=5,column=0)
# drop_database_button = Button(root, text='Drop Database', command=lambda: [send('DROP DATABASE '+ database_name_entry.get()), 
#                                                                               database_name_entry.delete(0,END),
#                                                                               update_result_label()])
# drop_database_button.grid(row=6,column=0)
# use_database_button = Button(root, text='Use Database', command=lambda: [send('USE '+ database_name_entry.get()), 
#                                                                               database_name_entry.delete(0,END),
#                                                                               update_result_label()])
# use_database_button.grid(row=7, column=0)

# table_name_label = Label(text='Table Name')
# table_name_label.grid(row=8, column=0)
# table_name_entry = Entry(root, width=35)
# table_name_entry.grid(row=8, column=1)
# drop_table_button = Button(root, text='Drop table',command=lambda: [send('DROP TABLE '+ table_name_entry.get()), 
#                                                                               table_name_entry.delete(0,END),
#                                                                               update_result_label()])
# drop_table_button.grid(row=9, column=0)

# # create table
# create_table_label = Label(text='Create table').grid(row=10,column=0)
# create_table_name_label = Label(text='name').grid(row=11,column=0)
# create_table_name_entry = Entry(root, width=15).grid(row=11,column=1)

# # columns info
# def add_column_frame(row):
#     column_frame = Frame(root,padx=15,pady=5).grid(row=row,column=0)
#     column_name_label = Label(column_frame, text='name').grid(row=0,column=0)
#     column_name_entry = Entry(column_frame, width=15).grid(row=0,column=1)
#     column_type_label = Label(column_frame, text='type').grid(row=0,column=2)
#     column_type_entry = Entry(column_frame, width=15).grid(row=0,column=3)
#     column_pk_label = Label(column_frame, text='primary key').grid(row=0,column=4)
#     pk = IntVar()
#     column_pk_checkbutton = Checkbutton(column_frame,variable=pk).grid(row=0,column=5)
#     row += 1
#     more_columns_button = Button(column_frame, text='+',command=lambda: add_column_frame(row)).grid(row=0,column=6)

# columns_label = Label(root, text='COLUMNS').grid(row=12,column=0)

# row = 13
# add_column_frame(row)

# column_frame = Frame(root,padx=15,pady=5).grid(row=13,column=0)
# column_name_label = Label(column_frame, text='name').grid(row=0,column=0)
# column_name_entry = Entry(column_frame, width=15).grid(row=0,column=1)
# column_type_label = Label(column_frame, text='type').grid(row=0,column=2)
# column_type_entry = Entry(column_frame, width=15).grid(row=0,column=3)
# column_pk_label = Label(column_frame, text='primary key').grid(row=0,column=4)
# pk = IntVar()
# column_pk_checkbutton = Checkbutton(column_frame,variable=pk).grid(row=0,column=5)
# more_columns_button = Button(column_frame, text='+',command=lambda: add_column_frame(root)).grid(row=0,column=6)

# disconnect_button = Button(root, text="Disconnect", command=lambda: send(DISCONNECT_MESSAGE))
# disconnect_button.grid(row=15, column=0)

# root.mainloop()


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\alexa\OneDrive\Desktop\facultate\master_sem1\build\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

window.geometry("810x505")
window.configure(bg = "#0F1971")


#SQL Query Frame
sql_query_canvas = Canvas(
    window,
    bg = "#0F1971",
    height = 505,
    width = 810,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

sql_query_canvas.place(x = 0, y = 0)
sql_query_canvas.create_text(
    409.0,
    124.0,
    anchor="nw",
    text="Enter SQL query",
    fill="#FFFFFF",
    font=("Jomolhari Regular", 20 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
indexes_button = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
indexes_button.place(
    x=409.0,
    y=431.0,
    width=180.28500366210938,
    height=36.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = sql_query_canvas.create_image(
    553.5,
    189.0,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=409.0,
    y=172.0,
    width=289.0,
    height=32.0
)

sql_query_canvas.create_text(
    119.0,
    23.0,
    anchor="nw",
    text="Database Management System",
    fill="#FFFFFF",
    font=("Jomolhari Regular", 40 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
tables_button = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
tables_button.place(
    x=409.0,
    y=382.0,
    width=180.28500366210938,
    height=34.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
databases_button = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("databases button clicked"),
    relief="flat"
)
databases_button.place(
    x=409.0,
    y=328.0,
    width=180.28500366210938,
    height=34.99999237060547
)

execution_result_label = sql_query_canvas.create_text(
    405.0,
    281.0,
    anchor="nw",
    text="",
    fill="#FFFFFF",
    font=("Jomolhari Regular", 24 * -1)
)



button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
submit_button = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:  [send(entry_1.get("1.0", "end-1c")), entry_1.delete("1.0", "end-1c"),sql_query_canvas.itemconfig(execution_result_label, text=receive())],
    relief="flat"
)
submit_button.place(
    x=409.0,
    y=227.0,
    width=121.0,
    height=35.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = sql_query_canvas.create_image(
    196.0,
    293.0,
    image=image_image_1
)


window.resizable(True, True)
window.mainloop()



