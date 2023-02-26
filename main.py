import tkinter as tk
from tkinter import ttk
import customtkinter


class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Face Recognition System")

        # Set the height and width of the window
        master.geometry("400x300")
        
        # Set the background color to blue
        customtkinter.set_appearance_mode("dark")
        
        # Create label with instructions
        label_style = ttk.Style()
        label_style.configure("My.TLabel", foreground="white", font=("Helvetica", 14))
        self.label = ttk.Label(master, text="Please choose an option:", style="My.TLabel")
        self.label.configure(background='#212325')  
        self.label.pack(pady=10)
        
        # Create buttons for each option
        button_style = ttk.Style()
        button_style.configure("My.TButton", foreground="black", background="#1c4e80", font=("Helvetica", 12), padding=10)
        self.button1 = ttk.Button(master, text="Option 1", style="My.TButton", command=self.option1)
        self.button1.pack(pady=5)
        self.button2 = ttk.Button(master, text="Option 2", style="My.TButton", command=self.option2)
        self.button2.pack(pady=5)
        self.button3 = ttk.Button(master, text="Option 3", style="My.TButton", command=self.option3)
        self.button3.pack(pady=5)
        
        # Create exit button
        self.exit_button = ttk.Button(master, text="Exit", style="My.TButton", command=master.quit)
        self.exit_button.pack(pady=10)
    
    def option1(self):
        print("Option 1 selected")
        # do something related to option 1
    
    def option2(self):
        print("Option 2 selected")
        # do something related to option 2
    
    def option3(self):
        print("Option 3 selected")
        # do something related to option 3
        
root = customtkinter.CTk()
my_gui = MyGUI(root)
root.mainloop()
