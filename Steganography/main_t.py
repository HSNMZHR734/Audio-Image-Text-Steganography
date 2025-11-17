from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
import os

from text_stg import TextStg  # Import the TextStg class
from file_handler import fileHandler
from utils import compatible_path

# ALL PATHS
DIR_PATH = compatible_path(os.path.dirname(os.path.realpath(__file__)))
TEXT_PATH = ""
MEDIA_PATH = ""  # This will store the cover text file path
DEST_PATH = DIR_PATH
TEXT_STG = TextStg()  # Create an instance of the TextStg class

RESOURCES = f"{DIR_PATH}\\resources\\"

LOGS = {
    "media_path": 0,
    "txt_path": 0,
    "dest_path": 0
}

def change_log(reset=False):
    text_log = ""
    T.config(state=NORMAL)
    T.delete('1.0', END)

    if not reset:
        # TEXT PATH
        if LOGS["txt_path"] == 0:
            text_log += "(?)-TEXT FILE IS NOT SELECTED!\n\n"
        else:
            text_log += "(OK)-TEXT FILE IS SELECTED.\n\n"
        # MEDIA PATH (Cover Text)
        if LOGS["media_path"] == 0:
            text_log += "(?)-COVER TEXT FILE IS NOT SELECTED!\n\n"
        else:
            text_log += "(OK)-COVER TEXT FILE IS SELECTED.\n\n"
        # DESTINATION PATH
        if LOGS["dest_path"] == 0:
            text_log += "(?)-DEST FOLDER IS NOT SELECTED!\n\n"
        else:
            text_log += "(OK)-DEST FOLDER IS SELECTED.\n\n"

    T.insert(END, text_log)
    T.config(state=DISABLED)

def get_error(mode="embed"):
    """
    This function checks if the required paths are selected.
    and returns 0 if there is no error.
    """
    if mode == "embed" and TEXT_PATH == "":
        messagebox.showinfo("INFO", "TEXT PATH IS NOT SELECTED!")
        return 1
    
    if MEDIA_PATH == "":
        messagebox.showinfo("INFO", "COVER TEXT FILE IS NOT SELECTED!")
        return 1
    
    return 0

def select_text_btn():
    global TEXT_PATH
    TEXT_PATH = filedialog.askopenfilename()
    if TEXT_PATH and TEXT_PATH.endswith(".txt"):
        LOGS["txt_path"] = 1
    else:
        TEXT_PATH = ""
        LOGS["txt_path"] = 0
    
    change_log()

def select_media_btn():
    global MEDIA_PATH
    MEDIA_PATH = filedialog.askopenfilename()
    if MEDIA_PATH.endswith('.txt'):
        LOGS["media_path"] = 1
    else:
        MEDIA_PATH = ""
        LOGS["media_path"] = 0
    
    change_log()

def select_dest_btn():
    global DEST_PATH
    DEST_PATH = filedialog.askdirectory()
    if DEST_PATH:
        LOGS["dest_path"] = 1
    else:
        LOGS["dest_path"] = 0
    change_log()

def embed_btn():
    if get_error("embed") == 0:
        # Define output file path
        output_file = os.path.join(DEST_PATH, "embedded_file.txt")
        threading.Thread(target=TEXT_STG.embed, args=(MEDIA_PATH, TEXT_PATH, output_file)).start()

def extract_btn():
    if get_error("extract") == 0:
        # Define output file path
        output_file = os.path.join(DEST_PATH, "extracted_text.txt")
        threading.Thread(target=TEXT_STG.extract, args=(MEDIA_PATH, output_file)).start()

def reset_btn():
    global TEXT_PATH, MEDIA_PATH, DEST_PATH
    if messagebox.askquestion("Reset Settings", "Are you sure?\nSelected paths will be deleted!") == "yes":
        TEXT_PATH = ""
        MEDIA_PATH = ""
        DEST_PATH = DIR_PATH

        LOGS["txt_path"] = 0
        LOGS["media_path"] = 0
        LOGS["dest_path"] = 0

        T.delete('1.0', END)

        change_log(reset=True)

# GUI - TKINTER
window = Tk()
window.title("TEXT STEGANOGRAPHY")
window.geometry("689x665")
window.configure(bg="#ffffff")

canvas = Canvas(
    window,
    bg="#ffffff",
    height=665,
    width=689,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

background_img = PhotoImage(file=compatible_path(RESOURCES + "background_t.png"))
background = canvas.create_image(344.5, 332.5, image=background_img)

img0 = PhotoImage(file=compatible_path(RESOURCES + "img0.png"))
b0 = Button(
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=reset_btn,
    relief="flat")
b0.place(x=606, y=227, width=69, height=72)

img1 = PhotoImage(file=compatible_path(RESOURCES + "img1.png"))
b1 = Button(
    image=img1,
    borderwidth=0,
    highlightthickness=0,
    command=embed_btn,
    activebackground="#E8CCCC",
    relief="flat")
b1.place(x=21, y=450, width=108, height=111)

img2 = PhotoImage(file=compatible_path(RESOURCES + "img2.png"))
b2 = Button(
    image=img2,
    borderwidth=0,
    highlightthickness=0,
    command=extract_btn,
    activebackground="#E6C7C7",
    relief="flat")
b2.place(x=195, y=450, width=108, height=111)

img3 = PhotoImage(file=compatible_path(RESOURCES + "img3.png"))
b3 = Button(
    image=img3,
    borderwidth=0,
    highlightthickness=0,
    command=select_dest_btn,
    activebackground="#EAD1D1",
    relief="flat")
b3.place(x=21, y=316, width=74, height=75)

img4 = PhotoImage(file=compatible_path(RESOURCES + "img4.png"))
b4 = Button(
    image=img4,
    borderwidth=0,
    highlightthickness=0,
    command=select_media_btn,
    activebackground="#EBD3D3",
    relief="flat")
b4.place(x=21, y=230, width=74, height=75)

img5 = PhotoImage(file=compatible_path(RESOURCES + "img5.png"))
b5 = Button(
    image=img5,
    borderwidth=0,
    highlightthickness=0,
    command=select_text_btn,
    activebackground="#ECD6D6",
    relief="flat")
b5.place(x=21, y=144, width=74, height=75)

T = Text(window, height=5, width=65)
T.insert(END, "...")
T.place(x=55, y=35)
T.config(borderwidth=0, state=DISABLED)

window.resizable(False, False)
window.mainloop()
