import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageDraw, ImageOps, ImageTk
from registration import RegisterPage
from loginpage import LoginPage


class LoginScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master

        self.create_widgets()

    def create_widgets(self):
        # set the size
        self.master.geometry("600x600")

        # Load and resize the face recognition icon
        face_icon = Image.open("image/face_id_logo.png")
        face_icon = face_icon.resize((150, 150), Image.ANTIALIAS)
        self.face_icon_image = ImageTk.PhotoImage(face_icon)

        self.label_title = tk.Label(self, text="Intelligent Course Management System", font=("Arial", 24))
        self.label_title.pack(pady=20)

        self.label_icon = tk.Label(self, image=self.face_icon_image)
        self.label_icon.pack(pady=(50, 20))

        self.label_subtitle = tk.Label(self, text="Please log in using facial recognition.", font=("Arial", 16))
        self.label_subtitle.pack(pady=10)

        # Create a style for the buttons
        style = ttk.Style()
        style.configure("TButton",
                        font=("Arial", 14),
                        padding=10,
                        relief="flat",
                        background="#4CAF50",  # You can choose a different color for the button
                        foreground="black"
                        )

        self.button_login = ttk.Button(self, text="Log in", style="TButton", command=self.login_and_defocus)
        self.button_login.pack(pady=20)

        # Add a Register button
        style.configure("TButton",
                        font=("Arial", 14),
                        padding=10,
                        relief="flat",
                        background="#008CBA",  # You can choose a different color for the button
                        foreground="black"
                        )

        self.button_register = ttk.Button(self, text="Register", style="TButton", command=self.register_and_defocus)
        self.button_register.pack(pady=20)


    def register_and_defocus(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()  # or widget.destroy() if you don't need them anymore

    # Then pack the new content
        self.register_page = RegisterPage(self.master)
        self.register_page.pack(fill=tk.BOTH, expand=True)

    def login_and_defocus(self):
        # Clear current content
        for widget in self.master.winfo_children():
            widget.pack_forget()  # or widget.destroy() if you don't need them anymore

        # Define a callback function for successful or failed login
        def login_callback(is_successful):
            if is_successful:
                print("UID recognized")
                # Here, you can switch to another page or perform other actions
            else:
                print("UID not recognized")
                # Optionally, handle failed login case

        # Create and display the login page
        login_page = LoginPage(self.master, login_callback)
        login_page.pack(fill=tk.BOTH, expand=True)
