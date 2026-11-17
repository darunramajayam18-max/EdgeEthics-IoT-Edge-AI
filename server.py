from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ==============================================
# Motion and Sensor Data
# ==============================================
motion_detected = False
temperature = None
humidity = None

# ==============================================
# AI and Ethical Compliance Data
# ==============================================
person_detected = False
person_id = "—"
safety = "—"
privacy = "—"
ethical_score = "—"


# ==============================================
# HOME
# ==============================================
@app.route("/")
def home():

    return "Ethical Compliance Server is Running"


# ==============================================
# ESP32 → Flask
# Receives PIR + DHT11 data
# ==============================================
@app.route("/motion", methods=["POST"])
def motion():

    global motion_detected
    global temperature
    global humidity

    data = request.json

    print("\n==============================")
    print("MOTION SIGNAL RECEIVED")
    print("Data:", data)
    print("==============================")

    if data.get("motion") == "detected":

        motion_detected = True

        temperature = data.get("temperature")
        humidity = data.get("humidity")

    return jsonify({
        "status": "received"
    })


# ==============================================
# Camera Trigger → Flask
# Gets latest motion + sensor data
# ==============================================
@app.route("/motion/status", methods=["GET"])
def motion_status():

    global motion_detected
    global temperature
    global humidity

    if motion_detected:

        motion_detected = False

        return jsonify({
            "motion": "detected",
            "temperature": temperature,
            "humidity": humidity
        })

    return jsonify({
        "motion": "none"
    })


# ==============================================
# AI → Flask
# Receives AI result
# ==============================================
@app.route("/ai/result", methods=["POST"])
def ai_result():

    global person_detected
    global person_id
    global safety
    global privacy
    global ethical_score

    data = request.json

    person_detected = data.get(
        "person_detected",
        False
    )

    person_id = data.get(
        "person_id",
        "Unknown"
    )

    safety = data.get(
        "safety",
        "—"
    )

    privacy = data.get(
        "privacy",
        "—"
    )

    ethical_score = data.get(
        "ethical_score",
        "—"
    )

    print("\n==============================")
    print("AI RESULT RECEIVED")
    print("Person Detected:", person_detected)
    print("Person ID:", person_id)
    print("Safety:", safety)
    print("Privacy:", privacy)
    print("Ethical Score:", ethical_score)
    print("==============================")

    return jsonify({
        "status": "AI result received"
    })


# ==============================================
# React Dashboard → Flask
# Returns complete system result
# ==============================================
@app.route("/dashboard", methods=["GET"])
def dashboard():

    return jsonify({

        "motion": "detected"
        if motion_detected
        else "none",

        "person_detected": person_detected,

        "person_id": person_id,

        "safety": safety,

        "privacy": privacy,

        "ethical_score": ethical_score,

        "temperature":
            temperature
            if temperature is not None
            else "—",

        "humidity":
            humidity
            if humidity is not None
            else "—"
    })


# ==============================================
# START FLASK SERVER
# ==============================================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )

