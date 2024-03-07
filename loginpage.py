import urllib
import pyttsx3
import pickle
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
import mysql.connector
from homePage import HomePage

class LoginPage(tk.Frame):
    def __init__(self, parent, login_callback):
        tk.Frame.__init__(self, parent, width=600, height=400, bg="#6FAE61")
        self.parent = parent
        self.pack(fill='both', expand=True)
        self.pack_propagate(0)  # Prevent the frame from resizing to fit its children
        self.master.geometry("600x400")  # Set the master window size, not the frame
        self.login_callback = login_callback  # Callback function to handle login
        self.myconn = mysql.connector.connect(host="localhost", user="root", passwd="1qaz2wsx", database="group15")
        self.cursor = self.myconn.cursor()

        # Load and resize the logo image
        logo_image = Image.open("image/hku-logo.jpg")  # Update with the path to your logo image
        logo_image = logo_image.resize((600, 120))  # Adjust the size as needed
        logo_image = ImageTk.PhotoImage(logo_image)
        self.logo_label = tk.Label(self, image=logo_image, bg="white")
        self.logo_label.image = logo_image  # Store a reference to the image to avoid garbage collection
        self.logo_label.pack()

        # Back Button
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(side=tk.TOP, anchor=tk.NW, pady=10)

        # UID Entry - Pack this first to ensure it shows up
        self.uid_entry = tk.Entry(self, bg="white", fg="black")
        self.uid_entry.pack(side=tk.LEFT, padx=(100, 5), anchor='n')  # Anchor north to align at the top

        # Login Button - Adjust padding so it does not push the entry off-screen
        self.login_button = tk.Button(self, text="Please Enter Your UID", command=self.perform_login, bg="chartreuse")
        self.login_button.pack(side=tk.LEFT, padx=(5, 10), anchor='n')

    def go_back(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()
        self.parent.show_start_page()

    def start_video_capture(self):
        _, frame = self.video_capture.read()
        frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a mirrored view
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the frame to RGB format

        # Resize the frame to match the camera view label size
        frame = cv2.resize(frame, (400, 200))

        # Convert the frame to PIL ImageTk format
        image = Image.fromarray(frame)
        image = ImageTk.PhotoImage(image)

        # Update the camera view label with the new image
        self.camera_view.configure(image=image)
        self.camera_view.image = image  # Store a reference to the image to avoid garbage collection

        # Schedule the next video capture
        self.camera_view.after(10, self.start_video_capture)

    def perform_login(self):
        # Get the entered UID from the entry widget
        uid = self.uid_entry.get()
        select = "SELECT * FROM student WHERE uid='%d'" % (int(uid))
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        if result:
            self.login_callback(True)
            #2 Load recognize and read label from model
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read("train.yml")
            labels = {"person_name": 1}
            with open("labels.pickle", "rb") as f:
                labels = pickle.load(f)
                labels = {v: k for k, v in labels.items()}
            # create text to speech
            engine = pyttsx3.init('dummy')
            rate = engine.getProperty("rate")
            engine.setProperty("rate", 175)
            # Define camera and detect face
            face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
            cap = cv2.VideoCapture(0)
            recognized = 0
            while True:
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

                for (x, y, w, h) in faces:
                    print(x, w, y, h)
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_color = frame[y:y + h, x:x + w]
                    # predict the id and confidence for faces
                    id_, conf = recognizer.predict(roi_gray)
            
                    # If the face is recognized
                    if conf >= 60:
                        # print(id_)
                        # print(labels[id_])
                        font = cv2.QT_FONT_NORMAL
                        id = 0
                        id += 1
                        name = labels[id_]
                        current_name = name
                        color = (255, 0, 0)
                        stroke = 2
                        cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
                        print("Your face is recognized")
                        recognized+=1
                    # If the face is unrecognized
                    else: 
                        color = (255, 0, 0)
                        stroke = 2
                        font = cv2.QT_FONT_NORMAL
                        cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
                        hello = ("Your face is not recognized")
                        print(hello)
                        engine.say(hello)
                        # engine.runAndWait()
                cv2.imshow('Attendance System', frame)
                k = cv2.waitKey(20) & 0xff
                print(recognized)
                if k == ord('q') or recognized == 0:
                    break
            cap.release()
            cv2.destroyAllWindows()
            #Go to home page
            for widget in self.master.winfo_children():
                widget.pack_forget()
            home_page = HomePage(self.master, int(uid))
            home_page.pack(fill="both", expand=True)
        else:
            self.login_callback(False)
