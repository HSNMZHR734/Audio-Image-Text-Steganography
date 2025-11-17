import os
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import subprocess
import threading

# Function to run a specified script in a new thread
def run_script(script_name):
    def thread_function(script_path):
        try:
            subprocess.run(["python", script_path], check=True)
        except subprocess.CalledProcessError as e:
            # Display an error message with the script's output
            error_message = f"Failed to run {script_name}.\nError:\n{e}"
            messagebox.showerror("Script Execution Error", error_message)

    script_path = os.path.join(os.getcwd(), script_name)
    thread = threading.Thread(target=thread_function, args=(script_path,))
    thread.start()

# Create the main window
window = Tk()
window.title("Steganography")
window.geometry("689x665")  # Adjust size as needed
window.resizable(False, False)

# Load background image
background_path = os.path.join(os.getcwd(), 'resources', 'back1.png')
background_image = Image.open(background_path)
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to display the background image
background_label = Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Function to create styled buttons with hover effects
def create_hover_button(image_path, command, x, y):
    button_image = Image.open(image_path)
    button_image = button_image.resize((200, 100), Image.LANCZOS)  # Resize to 200x100 pixels
    button_photo = ImageTk.PhotoImage(button_image)
    
    style = ttk.Style()
    style.configure('TButton', padding=5, relief="flat", borderwidth=0)
    
    button = ttk.Button(window, image=button_photo, command=command, style='TButton')
    button.image = button_photo  # Keep a reference to avoid garbage collection
    button.place(x=x, y=y)

    # Function to change button style on hover
    def on_enter(event):
        button.state(['!pressed', 'hover'])
        button.configure(style='Hover.TButton')

    def on_leave(event):
        button.state(['!pressed', '!hover'])
        button.configure(style='TButton')

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    return button

# Configure hover style
hover_style = ttk.Style()
hover_style.configure('Hover.TButton', background='gray', relief='raised', borderwidth=1)

# Starting y-coordinate for the buttons
start_y = 100
button_spacing = 170  # 100 pixels for the button height + 70 pixels for spacing

# Create button to run main.py
create_hover_button(os.path.join(os.getcwd(), 'resources', 'btn_i.png'), lambda: run_script('main.py'), 75, start_y)

# Create button to run main_a.py
create_hover_button(os.path.join(os.getcwd(), 'resources', 'btn_a.png'), lambda: run_script('main_a.py'), 75, start_y + button_spacing)

# Create button to run main_t.py
create_hover_button(os.path.join(os.getcwd(), 'resources', 'btn_t.png'), lambda: run_script('main_t.py'), 75, start_y + 2 * button_spacing)

# Run the Tkinter main loop
window.mainloop()
