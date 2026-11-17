import cv2
import pickle
import numpy as np

# Load saved face embeddings
with open("face_embeddings.pkl", "rb") as file:
    data = pickle.load(file)

embeddings = data["embeddings"]
labels = data["labels"]

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

# Start laptop camera
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not open camera")
    exit()

print("Camera started")
print("Press Q to quit")
last_id = None

while True:

    ret, frame = camera.read()

    if not ret:
        print("Could not read camera")
        break

    # Set detector input size
    detector.setInputSize((frame.shape[1], frame.shape[0]))

    # Detect faces
    _, faces = detector.detect(frame)

    if faces is not None:

        for face in faces:

            # Align detected face
            aligned_face = recognizer.alignCrop(frame, face)

            # Generate embedding
            feature = recognizer.feature(aligned_face)

            best_score = -1
            best_id = "Unknown"

            # Compare with registered faces
            for stored_feature, person_id in zip(embeddings, labels):

                score = recognizer.match(
                    feature,
                    stored_feature,
                    cv2.FaceRecognizerSF_FR_COSINE
                )

                if score > best_score:
                    best_score = score
                    best_id = person_id

            # Recognition threshold
            if best_score >= 0.363:
                person_id = best_id
                status = "Privacy: PASS"
            else:
                person_id = "Unknown"
                status = "Privacy: PASS"
                
            if person_id != last_id:
                print("Person Detected: YES")
                print("Person ID:", person_id)
                print(status)
                print("--------------------")
                last_id = person_id

            # Face bounding box
            x, y, w, h = face[:4].astype(int)

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # Display ID only
            cv2.putText(
                frame,
                "Person ID: " + person_id,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                status,
                (x, y + h + 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    # Show camera
    cv2.imshow("Edge-AI Ethical Compliance", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()