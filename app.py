from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from ai_engine import detect_face_file, verify_identity, load_workers
from db import save_attendance, get_dashboard_data, get_all_records, init_db

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

workers = load_workers()
init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/face", methods=["POST"])
def face():
    image = request.files["image"]
    result = detect_face_file(image)

    if not result:
        return jsonify({"success": False})

    return jsonify({
        "success": True,
        "face_id": result["face_id"],
        "name": result["name"]
    })

@app.route("/api/verify", methods=["POST"])
def verify():
    data = request.json

    qr_id = data["qr_id"]
    face_id = data["face_id"]

    if not verify_identity(qr_id, face_id):
        return jsonify({"success": False, "message": "Mismatch"})

    name = workers.get(face_id, "Unknown")
    result = save_attendance(face_id, name)

    return jsonify({"success": True, "result": result})

@app.route("/api/dashboard")
def dashboard():
    return jsonify(get_dashboard_data(workers))

@app.route("/api/records")
def records():
    return jsonify(get_all_records())

if __name__ == "__main__":
    app.run()