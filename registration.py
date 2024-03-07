from tkinter import *
import tkinter as tk
from tkinter import ttk
import mysql.connector 
import sys
from tkinter import messagebox
from face_capture import FaceCapture
from train import FaceTrainer
from loginpage import LoginPage
import os
from PIL import Image, ImageTk

class RegisterPage(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # Database connection
        self.myconn = mysql.connector.connect(host="localhost", user="root", passwd="1qaz2wsx", database="group15")
        self.cursor = self.myconn.cursor()

        # Styling
        style = ttk.Style()
        style.configure('TLabel', font=('Times New Roman', 20))
        style.configure('TButton', font=('Times New Roman', 20, 'bold'), background='blue')
        style.configure('TEntry', font=('Times New Roman', 20))

        #size of the window
        self.master.geometry("600x400")

        # Configure the grid layout
        self.grid_rowconfigure(0, weight=1)  # Adjust the minsize as needed for vertical spacing
        self.grid_columnconfigure(1, weight=3)  # Adjust the minsize as needed for horizontal spacing
        

        self.configure(background='#6FAE61')
        icon_image = Image.open("image/hku-logo.jpg")
        icon_image = icon_image.resize((400, 100))  # Adjust the size as needed
        icon_image = ImageTk.PhotoImage(icon_image)

         # Icon Label
        self.icon_label = tk.Label(self, image=icon_image)
        self.icon_label.image = icon_image  # Store a reference to the image to avoid garbage collection
        self.icon_label.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        # Add a back button
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.grid(row=1, column=0, sticky="w", padx=0, pady=10)

        # UID Label and Entry
        self.uid_label = ttk.Label(self, text="UID:", style='TLabel')
        self.uid_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.uid_entry = ttk.Entry(self, font=('Times New Roman', 20))
        self.uid_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=10, pady=10)

        # Name Label and Entry
        self.name_label = ttk.Label(self, text="Name:", style='TLabel')
        self.name_entry = ttk.Entry(self, font=('Times New Roman', 20))
        self.name_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.name_entry.grid(row=3, column=1, columnspan=2, sticky="ew", padx=10, pady=10)

        # Email Label and Entry
        self.email_label = ttk.Label(self, text="Email Address:", style='TLabel')
        self.email_entry = ttk.Entry(self, font=('Times New Roman', 20))
        self.email_label.grid(row=4, column=0, sticky="w", padx=10, pady=10)
        self.email_entry.grid(row=4, column=1, columnspan=2, sticky="ew", padx=10, pady=10)

         # Submit Button
        self.submit_button = ttk.Button(self, text="Register", command=self.on_submit, style='TButton')
        self.submit_button.grid(row=5, column=1, columnspan=1, pady=10)

        # Adjust the button padding to modify the size
        self.submit_button['padding'] = (10, 0)  # Adjust the padding values as needed

    
    def go_back(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()
        
        self.parent.show_start_page()

    def on_submit(self):
        select = "SELECT * FROM studentList WHERE uid='%d'" % (int(self.uid_entry.get()))
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        if result:
            message = "Information correct\n Do you want to proceed to face recognition?"
            response = messagebox.askquestion("Confirm", message, icon='question')
            if (response == 'no'):
                self.uid_entry.delete(0, tk.END)
                self.name_entry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)
            else:
                face_capture = FaceCapture(self.name_entry.get())
                face_capture.capture_faces()
                base_directory = os.path.dirname(os.path.abspath(__file__))
                data_directory = "data"
                cascade_file = 'haarcascade/haarcascade_frontalface_default.xml'
                face_trainer = FaceTrainer(base_directory, data_directory, cascade_file)
                face_trainer.train_faces()
                print("Training completed")
                #insert into database  
                insert = "INSERT INTO Student (uid, name, email) VALUES (%d, '%s', '%s')" % (int(self.uid_entry.get()), self.name_entry.get(), self.email_entry.get())
                self.cursor.execute(insert)
                self.myconn.commit()
                #success message
                message = "Student registered successfully"
                messagebox.showinfo("Success", message)
                #redirect to login page
                def login_callback(is_successful):
                    if is_successful:
                        print("UID recognized")
                # Here, you can switch to another page or perform other actions
                    else:
                        print("UID not recognized")
                # Optionally, handle failed login case
                for widget in self.master.winfo_children():
                    widget.pack_forget() 
                login_page = LoginPage(self.master, login_callback)
                login_page.pack(fill=tk.BOTH, expand=True)
                

                
            

        else:
            message = "Invaild UID, please try again."
            messagebox.showinfo("Error", message)
            #set input box to empty
            self.uid_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
