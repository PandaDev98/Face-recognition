import cv2
from PIL import Image, ImageTk
import PIL.Image

import tkinter as tk
from tkinter import ttk
import customtkinter


class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Face Recognition System")

        # Set the  width and height of the window
        master.geometry("875x720")

        # Set the background color to blue
        customtkinter.set_appearance_mode("dark")

        # Create label with instructions
        label_style = ttk.Style()
        label_style.configure(
            "My.TLabel", foreground="white", font=("Helvetica", 14))
        self.label = ttk.Label(
            master, text="Please choose an option:", style="My.TLabel")
        self.label.configure(background='#212325')
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        # Create buttons for each option
        button_style = ttk.Style()
        button_style.configure("My.TButton", foreground="black",
                               background="#1c4e80", font=("Helvetica", 12), padding=10)

        self.button1 = ttk.Button(
            master, text="Recognice user", style="My.TButton", command=self.option1)
        self.button1.grid(row=1, column=1, rowspan=1, pady=5)
        self.button2 = ttk.Button(
            master, text="Train person model", style="My.TButton", command=self.option2)
        self.button2.grid(row=2, column=1, rowspan=1, pady=5)
        self.button3 = ttk.Button(
            master, text="Option 3", style="My.TButton", command=self.option3)
        self.button3.grid(row=3, column=1, rowspan=1, pady=5)

        # Create a frame to hold the video feed
        self.video_frame = tk.Frame(master, width=640, height=480)
        self.video_frame.grid(row=1, rowspan=4, column=0, padx=30)
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()
        # Create exit button
        self.exit_button = ttk.Button(
            master, text="Exit", style="My.TButton", command=master.quit)
        self.exit_button.grid(row=4, column=1, rowspan=1, pady=10)

        # Initialize video capture from camera
        self.cap = cv2.VideoCapture(0)
        self.update_video()

    def option1(self):
        print("Option 1 selected")

    def option2(self):
        print("Option 2 selected")

    def option3(self):
        print("Option 3 selected")
        # do something related to option 3
        # Start the video feed

    def update_video(self):
        ret, frame = self.cap.read()

        if ret:
           # Convert the cv2 frame to a PIL image
            image = PIL.Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Resize the image
            image = image.resize((640, 480), PIL.Image.ANTIALIAS)

            # Convert the PIL image to a Tkinter compatible image
            photo = PIL.ImageTk.PhotoImage(image)

            # Update the video label with the new image
            self.video_label.config(image=photo)
            self.video_label.image = photo

        # Repeat every 10 milliseconds
        self.master.after(10, self.update_video)


root = customtkinter.CTk()
my_gui = MyGUI(root)
root.mainloop()


def cameraFrames():
    # Initialize video capture from camera
    cap = cv2.VideoCapture(0)
    # Capture frame-by-frame
    ret, frame = cap.read()
