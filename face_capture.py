import cv2
import os

class FaceCapture:
    def __init__(self, user_name, num_imgs=400):
        self.user_name = user_name
        self.num_imgs = num_imgs
        self.face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
        self.setup_user_folder()
        self.video_capture = None

    def setup_user_folder(self):
        if not os.path.exists(f'data/{self.user_name}'):
            os.mkdir(f'data/{self.user_name}')

    def start_video_capture(self):
        if self.video_capture is None:
            self.video_capture = cv2.VideoCapture(0)

    def capture_faces(self):
        self.start_video_capture()
        cnt = 1
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottom_left_corner_of_text = (350, 50)
        font_scale = 1
        font_color = (102, 102, 225)
        line_type = 2

        while cnt <= self.num_imgs:
            ret, frame = self.video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Display the resulting frame
            cv2.imshow('Video', frame)

            # Store the captured images
            cv2.imwrite(f"data/{self.user_name}/{self.user_name}{cnt:03d}.jpg", frame)
            cnt += 1

            key = cv2.waitKey(100)

        # Release the capture
        self.video_capture.release()
        cv2.destroyAllWindows()
 
faceCascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)

