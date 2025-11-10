from flask import Flask, Response, render_template, jsonify
import cv2
import threading
import time
from gpiozero import LED

app = Flask(__name__)

# ----------------------------
# GPIO Relay setup
# ----------------------------
relay = LED(17)
relay.off()

# ----------------------------
# Global status dictionary
# ----------------------------
status = {
    "face_detected": False,
    "relay_on": False,
    "power_used": 0.0,
    "power_saved": 0.0,
    "cost": 0.0
}
latest_frame = None

COST_PER_KWH = 6.5   # ₹ per kWh
WATT_CONSUMPTION = 60 # watts load
OFF_DELAY = 10        # seconds

def face_detection_loop():
    global latest_frame, status

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    last_seen = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        face_found = len(faces) > 0

        if face_found:
            relay.on()
            status["face_detected"] = True
            status["relay_on"] = True
            last_seen = time.time()
        elif status["relay_on"] and (time.time() - last_seen > OFF_DELAY):
            relay.off()
            status["face_detected"] = False
            status["relay_on"] = False

        # Power logic
        if status["relay_on"]:
            # convert 60W → Wh per second
            status["power_used"] += (WATT_CONSUMPTION / 3600)
        else:
            status["power_saved"] += (WATT_CONSUMPTION / 7200)

        status["cost"] = (status["power_used"] / 1000) * COST_PER_KWH

        # Draw status
        color = (0,255,0) if face_found else (0,0,255)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), color, 2)

        cv2.putText(frame, f"Relay: {'ON' if status['relay_on'] else 'OFF'}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        latest_frame = cv2.resize(frame, (640,480))
        time.sleep(0.2)

def generate_frames():
    global latest_frame
    while True:
        if latest_frame is not None:
            ret, buffer = cv2.imencode('.jpg', latest_frame)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        time.sleep(0.05)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def get_data():
    return jsonify(status)

if __name__ == '__main__':
    threading.Thread(target=face_detection_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
