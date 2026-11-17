import cv2
import os
import numpy as np
import pickle

# Load face detection model
detector = cv2.FaceDetectorYN.create(
    "models/face_detection_yunet_2023mar.onnx",
    "",
    (320, 320)
)

# Load face recognition model
recognizer = cv2.FaceRecognizerSF.create(
    "models/face_recognition_sface_2021dec.onnx",
    ""
)

dataset_path = "dataset"

embeddings = []
labels = []

# Go through each person's folder
for person_id in os.listdir(dataset_path):

    person_folder = os.path.join(dataset_path, person_id)

    if not os.path.isdir(person_folder):
        continue

    for filename in os.listdir(person_folder):

        image_path = os.path.join(person_folder, filename)

        image = cv2.imread(image_path)

        if image is None:
            print("Could not read:", image_path)
            continue

        # Set image size for detector
        detector.setInputSize((image.shape[1], image.shape[0]))

        # Detect face
        _, faces = detector.detect(image)

        if faces is None:
            print("No face detected:", image_path)
            continue

        # Use first detected face
        face = faces[0]

        # Align face
        aligned_face = recognizer.alignCrop(image, face)

        # Generate face embedding
        feature = recognizer.feature(aligned_face)

        embeddings.append(feature)
        labels.append(person_id)

        print("Processed:", person_id, filename)

# Save embeddings
data = {
    "embeddings": embeddings,
    "labels": labels
}

with open("face_embeddings.pkl", "wb") as file:
    pickle.dump(data, file)

print()
print("Face embeddings created successfully!")
print("Total faces:", len(embeddings))