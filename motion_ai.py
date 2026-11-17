
import cv2
from ultralytics import YOLO
import pickle
import requests
from ethical_logic import calculate_ethical_score


def process_image(image_path, data):

    # -----------------------------
    # Get sensor data from Flask
    # -----------------------------
    temperature = data.get("temperature")
    humidity = data.get("humidity")

    # -----------------------------
    # 1. Load YOLO model
    # -----------------------------
    model = YOLO("yolo11n.pt")

    # -----------------------------
    # 2. Load captured image
    # -----------------------------
    image = cv2.imread(image_path)

    if image is None:
        print("Could not load image")
        return

    print("Image loaded successfully")

    # -----------------------------
    # 3. YOLO person detection
    # -----------------------------
    results = model(image)

    person_detected = False

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            # YOLO class 0 = person
            if class_id == 0 and confidence >= 0.50:

                person_detected = True

                print("Person Detected: YES")
                print("Confidence:", round(confidence, 2))

    if not person_detected:

        print("Person Detected: NO")
        print("No person found in the image.")

        return

    print("--------------------")

    # -----------------------------
    # 4. Load face embeddings
    # -----------------------------
    with open(
        "face_recognition/face_embeddings.pkl",
        "rb"
    ) as file:

        face_data = pickle.load(file)

    embeddings = face_data["embeddings"]
    labels = face_data["labels"]

    # -----------------------------
    # 5. Load YuNet
    # -----------------------------
    detector = cv2.FaceDetectorYN.create(
        "face_recognition/models/face_detection_yunet_2023mar.onnx",
        "",
        (320, 320)
    )

    # -----------------------------
    # 6. Load SFace
    # -----------------------------
    recognizer = cv2.FaceRecognizerSF.create(
        "face_recognition/models/face_recognition_sface_2021dec.onnx",
        ""
    )

    # -----------------------------
    # 7. Detect face
    # -----------------------------
    detector.setInputSize(
        (image.shape[1], image.shape[0])
    )

    _, faces = detector.detect(image)

    if faces is None:

        print("Face Detected: NO")
        print("Person ID: Unknown")

        return

    print("Face Detected: YES")

    # -----------------------------
    # 8. Recognize face
    # -----------------------------
    for face in faces:

        aligned_face = recognizer.alignCrop(
            image,
            face
        )

        feature = recognizer.feature(
            aligned_face
        )

        best_score = -1
        best_id = "Unknown"

        # Compare with registered faces
        for stored_feature, stored_id in zip(
            embeddings,
            labels
        ):

            score = recognizer.match(
                feature,
                stored_feature,
                cv2.FaceRecognizerSF_FR_COSINE
            )

            if score > best_score:

                best_score = score
                best_id = stored_id

        # Recognition threshold
        if best_score >= 0.363:

            person_id = best_id

        else:

            person_id = "Unknown"

        print("Person ID:", person_id)
        print(
            "Recognition Score:",
            round(best_score, 3)
        )

        # -----------------------------
        # 9. Ethical Compliance
        # -----------------------------
        ethical_result = calculate_ethical_score(
            True,
            person_id,
            temperature
        )

        print(
            "Safety:",
            ethical_result["safety"]
        )

        print(
            "Privacy:",
            ethical_result["privacy"]
        )

        print(
            "Ethical Score:",
            ethical_result["ethical_score"],
            "/100"
        )

        # -----------------------------
        # 10. Send AI result to Flask
        # -----------------------------
        try:

            response = requests.post(
                "http://127.0.0.1:5000/ai/result",

                json={
                    "person_detected": True,
                    "person_id": person_id,
                    "safety": ethical_result["safety"],
                    "privacy": ethical_result["privacy"],
                    "ethical_score": ethical_result["ethical_score"]
                },

                timeout=5
            )

            if response.status_code == 200:

                print("AI result sent to Flask.")

            else:

                print(
                    "Flask returned status:",
                    response.status_code
                )

        except requests.exceptions.RequestException as e:

            print(
                "Could not send AI result to Flask:",
                e
            )

        print("--------------------")

    print("AI processing completed.")

