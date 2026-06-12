import cv2
import csv
import numpy as np
import os

print("LOADING AI_ENGINE FROM:", __file__)

# =====================
# LOAD MODELS
# =====================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# ✅ CREATE FIRST
recognizer = cv2.face.LBPHFaceRecognizer_create()

# ✅ THEN LOAD MODEL SAFELY

# ✅ THEN LOAD MODEL SAFELY

if os.path.exists("face_model.yml"):
    recognizer.read("face_model.yml")
    print("Model loaded successfully")
else:
    print("face_model.yml not found. Please train model first.")

qr_detector = cv2.QRCodeDetector()

FACE_THRESHOLD = 70

# =====================
# LOAD WORKERS
# =====================

def load_workers():
    workers = {}

    try:
        with open("workers.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                workers[row["ID"]] = row["Name"]

    except Exception as e:
        print("Worker load error:", e)

    return workers


# =====================
# FACE RECOGNITION (FRAME VERSION)
# =====================

def detect_face_frame(frame):

    workers = load_workers()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in faces:

        id_, conf = recognizer.predict(gray[y:y+h, x:x+w])

        if conf < FACE_THRESHOLD:

            face_id = str(id_)

            return {
                "face_id": face_id,
                "name": workers.get(face_id, "Unknown"),
                "confidence": conf,
                "box": (x, y, w, h)
            }

    return None


# =====================
# FACE RECOGNITION (FLASK IMAGE VERSION) ⭐ NEW
# =====================

def detect_face_file(file):

    workers = load_workers()

    img_array = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in faces:

        id_, conf = recognizer.predict(gray[y:y+h, x:x+w])

        if conf < FACE_THRESHOLD:

            face_id = str(id_)

            return {
                "face_id": face_id,
                "name": workers.get(face_id, "Unknown"),
                "confidence": conf,
                "box": (x, y, w, h)
            }

    return None


# =====================
# QR DETECTION (FRAME VERSION)
# =====================

def detect_qr(frame):

    data, bbox, _ = qr_detector.detectAndDecode(frame)

    if data:
        return data.strip()

    return None


# =====================
# QR (STRING VERSION FOR MOBILE)
# =====================

def detect_qr_text(qr_text):

    if qr_text:
        return qr_text.strip()

    return None


# =====================
# VERIFY QR + FACE
# =====================

def verify_identity(qr_id, face_id):

    return qr_id == face_id