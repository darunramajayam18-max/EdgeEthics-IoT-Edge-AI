import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened")
    exit()

print("Camera started successfully")
print("Press Q to close the camera")

while True:
    ret, frame = camera.read()

    if not ret:
        print("Failed to capture frame")
        break

    cv2.imshow("Laptop Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()