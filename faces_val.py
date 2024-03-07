import cv2
import pyttsx3
import pickle
import mysql.connector
from datetime import datetime

class FaceRecognitionSystem:
    def __init__(self):
        # Initialize database connection
        self.myconn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="1qaz2wsx",
            database="group15"
        )
        self.cursor = self.myconn.cursor()

        # Initialize the face recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("train.yml")

        # Load labels
        with open("labels.pickle", "rb") as f:
            self.labels = pickle.load(f)
            self.labels = {v: k for k, v in self.labels.items()}

        # Initialize text to speech
        self.engine = pyttsx3.init('dummy')
        self.engine.setProperty("rate", 175)

        # Face detection classifier
        self.face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

    def recognize_and_respond(self):
        # Open the camera and start the recognition process
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            result = self.process_frame(frame)

            # Display the frame
            cv2.imshow('Attendance System', frame)
            if cv2.waitKey(20) & 0xff == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return result

    def process_frame(self, frame):
        # Process each frame for face recognition
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        true = 0
        false = 0

        for (x, y, w, h) in faces:
            if self.handle_face(frame, gray, x, y, w, h):
                true += 1
            
        
            
            

    def handle_face(self, frame, gray, x, y, w, h):
        # Handle each detected face
        roi_gray = gray[y:y + h, x:x + w]
        id_, conf = self.recognizer.predict(roi_gray)

        if conf >= 40:
            name = self.labels.get(id_, "Unknown")
            self.update_display(frame, name, x, y, w, h)
            return True
            
            
            #self.update_database(name)
        else:
            self.update_display(frame, "UNKNOWN", x, y, w, h)
            return False


    def update_display(self, frame, name, x, y, w, h):
        # Update the display with name and rectangle around the face
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (255, 0, 0)
        stroke = 2
        cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, stroke)

    def update_database(self, name):
        # Update the database with attendance information
        if name != "UNKNOWN":
            current_time = datetime.now().strftime("%H:%M:%S")
            date = datetime.utcnow()
            update = "UPDATE Student SET login_date=%s, login_time=%s WHERE name=%s"
            val = (date, current_time, name)
            self.cursor.execute(update, val)
            self.myconn.commit()
            self.say_message(f"Hello {name}, your attendance has been recorded.")

    def say_message(self, message):
        # Convert text to speech
        self.engine.say(message)
        self.engine.runAndWait()