
import cv2
import requests
import time
import subprocess
import webbrowser

from motion_ai import process_image


# ==============================================
# START REACT FRONTEND AUTOMATICALLY
# ==============================================

print("Starting React frontend...")

frontend = subprocess.Popen(
    ["npm", "run", "dev"],
    cwd="frontend",
    shell=True
)

# Give Vite some time to start
time.sleep(5)

# Open dashboard automatically
webbrowser.open("http://localhost:5173/")

print("React dashboard opened automatically.")


# ==============================================
# FLASK SERVER
# ==============================================

FLASK_URL = "http://127.0.0.1:5000/motion/status"


# ==============================================
# CAMERA
# ==============================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("Camera could not be opened")
    exit()


print("Camera ready")
print("Waiting for motion...")


# ==============================================
# MAIN LOOP
# ==============================================

while True:

    try:

        response = requests.get(FLASK_URL)

        if response.status_code == 200:

            data = response.json()

            if data.get("motion") == "detected":

                print("Motion detected!")
                print("Capturing image...")

                ret, frame = camera.read()

                if ret:

                    filename = "motion_capture.jpg"

                    cv2.imwrite(
                        filename,
                        frame
                    )

                    print(
                        "Image captured successfully!"
                    )

                    print(
                        "Saved as:",
                        filename
                    )

                    print(
                        "Starting AI processing..."
                    )

                    print(
                        "Sensor data sent to AI:",
                        data
                    )

                    process_image(
                        filename,
                        data
                    )

                else:

                    print(
                        "Failed to capture image"
                    )

                time.sleep(3)

    except Exception as e:

        print("Error:", e)

    time.sleep(0.5)

