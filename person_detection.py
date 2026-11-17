from ultralytics import YOLO

# Load the YOLO model
model = YOLO("yolo11n.pt")

# Detect objects in the captured image
results = model("motion_capture.jpg")

# Check the detected objects
for result in results:
    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        class_name = model.names[class_id]

        print(f"Detected: {class_name} | Confidence: {confidence:.2f}")