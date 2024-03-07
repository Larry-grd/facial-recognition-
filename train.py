import os
import numpy as np
from PIL import Image
import cv2
import pickle

class FaceTrainer:
    def __init__(self, base_dir, data_folder, cascade_path):
        self.base_dir = base_dir
        self.data_folder = data_folder
        self.cascade_path = cascade_path
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

    def train_faces(self):
        label_ids = {}
        current_id = 0
        y_labels = []
        x_train = []
        image_dir = os.path.join(self.base_dir, self.data_folder)

        for root, dirs, files in os.walk(image_dir):
            for file in files:
                if file.endswith("png") or file.endswith("jpg"):
                    path = os.path.join(root, file)
                    label = os.path.basename(root).replace(" ", "").upper()  # name

                    if label not in label_ids:
                        label_ids[label] = current_id
                        current_id += 1

                    id_ = label_ids[label]
                    pil_image = Image.open(path).convert("L")  # Convert to grayscale
                    image_array = np.array(pil_image, "uint8")
                    faces = self.face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

                    for (x, y, w, h) in faces:
                        roi = image_array[y:y+h, x:x+w]
                        x_train.append(roi)
                        y_labels.append(id_)

        with open("labels.pickle", "wb") as f:
            pickle.dump(label_ids, f)

        self.recognizer.train(x_train, np.array(y_labels))
        self.recognizer.save("train.yml")
        print("Training completed")