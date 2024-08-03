import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
from tkinterdnd2 import TkinterDnD, DND_FILES
import pyttsx3
from main import startAssistant 
import time

button_clicked = False

def on_start_button_click():
    global button_clicked
    button_clicked = True
    start_button.config(background='green', foreground='white')
    speak("Starting the virtual assistant.....! . please wait for a second  ")
    startAssistant(on_assistant_exit)

def on_assistant_exit():
    speak("Assistant has exited. Closing the application.")
    root.destroy()

def on_enter(e):
    if not button_clicked:
      start_button.config(background='green', foreground='white')

def on_leave(e):
    if not button_clicked:
        start_button.config(background='red', foreground='white')

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

root = TkinterDnD.Tk()
root.title("Virtual Assistant")
root.geometry("650x700")
root.resizable(False, False)

image = Image.open("D:\\desk ai\\images\\image.webp")  
image = image.resize((650, 700), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)
label = Label(root, image=photo)
label.pack()

start_button = tk.Button(root, text="Start", command=on_start_button_click, font=("Helvetica", 20),
                         background='red', foreground='white', relief=tk.FLAT, width=10, height=2)
start_button.config(font=("Helvetica", 16, "bold")) 

start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)

button_x = 325 - (start_button.winfo_reqwidth() // 2)
button_y = 350 - (start_button.winfo_reqheight() // 2)
start_button.place(x=button_x, y=button_y)

engine = pyttsx3.init('sapi5')

root.mainloop()
