let stream = null;
let faceId = null;
let qrId = null;

async function startCamera() {

    const video = document.getElementById("video");

    stream = await navigator.mediaDevices.getUserMedia({
        video:{
            facingMode:"user"
        }
    });

    video.srcObject = stream;
}

async function captureFace() {

    const video = document.getElementById("video");

    const canvas = document.createElement("canvas");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(video,0,0);

    canvas.toBlob(async(blob)=>{

        const fd = new FormData();

        fd.append("image",blob,"face.jpg");

        const res = await fetch("/api/face",{
            method:"POST",
            body:fd
        });

        const data = await res.json();

        if(data.success){

            faceId = data.face_id;

            document.getElementById("result").innerHTML =
            "✅ Face: " + data.name;

        }else{

            document.getElementById("result").innerHTML =
            "❌ Face Not Recognized";
        }

    },"image/jpeg");
}
