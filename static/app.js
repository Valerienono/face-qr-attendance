const video = document.getElementById("video");

navigator.mediaDevices.getUserMedia({ video: true })
.then(stream => {
    video.srcObject = stream;
});

function captureFace() {

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    canvas.toBlob(blob => {

        let formData = new FormData();
        formData.append("image", blob);

        fetch("/api/face", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {

            document.getElementById("result").innerText =
                "Face: " + JSON.stringify(data);

        });

    }, "image/jpeg");
}

let qrScanner = new Html5Qrcode("qr-reader");

qrScanner.start(
    { facingMode: "environment" },
    { fps: 10, qrbox: 200 },
    qrCodeMessage => {

        document.getElementById("result").innerText =
            "QR: " + qrCodeMessage;

        // OPTIONAL: send to backend
        window.lastQR = qrCodeMessage;
    }
);

function verify(face_id) {

    fetch("/api/verify", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            qr_id: window.lastQR,
            face_id: face_id
        })
    })
    .then(res => res.json())
    .then(data => {

        document.getElementById("result").innerText =
            "Verify: " + JSON.stringify(data);

    });
}

