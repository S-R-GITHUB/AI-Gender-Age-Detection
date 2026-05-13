from flask import Flask, render_template, request
import os
import base64
from detector import detect_image

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "image" not in request.files:
        return "No file uploaded"

    file = request.files["image"]

    if file.filename == "":
        return "No selected file"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    result_path = detect_image(filepath)

    return f"""

    <html>

    <head>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>

    body{{
        background:#0f172a;
        color:white;
        text-align:center;
        padding-top:50px;
    }}

    .result-box{{
        background:#1e293b;
        padding:30px;
        border-radius:20px;
        width:80%;
        margin:auto;
    }}

    img{{
        border-radius:15px;
        margin-top:20px;
        width:70%;
        border:4px solid cyan;
    }}

    .btn-custom{{
        margin-top:25px;
        padding:12px 25px;
        font-size:18px;
    }}

    </style>

    </head>

    <body>

    <div class="result-box">

        <h1>
            Detection Result
        </h1>

        <img src='/{result_path}'>

        <br>

        <a href='/{result_path}' download>

            <button class="btn btn-success btn-custom">

                Download Result

            </button>

        </a>

        <br>

        <a href="/">

            <button class="btn btn-primary btn-custom">

                Back To Home

            </button>

        </a>

    </div>

    </body>

    </html>

    """


@app.route('/live')
def live():

    return """

<!DOCTYPE html>

<html>

<head>

<title>Live AI Detection</title>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<style>

body{
    background:#0f172a;
    color:white;
    text-align:center;
    padding-top:40px;
    font-family:Arial;
}

.live-box{
    background:#1e293b;
    padding:30px;
    border-radius:20px;
    width:85%;
    margin:auto;
}

video{
    width:80%;
    border-radius:20px;
    margin-top:20px;
    border:4px solid #38bdf8;
}

button{
    padding:12px 25px;
    margin-top:20px;
    font-size:18px;
    border:none;
    border-radius:10px;
    cursor:pointer;
}

</style>

</head>

<body>

<div class="live-box">

    <h1>Live AI Detection</h1>

    <video id="video" autoplay playsinline></video>

    <br>

    <button class="btn btn-success" onclick="capture()">
        Capture & Detect
    </button>

    <a href="/">
        <button class="btn btn-primary">
            Back To Home
        </button>
    </a>

    <canvas id="canvas" style="display:none;"></canvas>

    <form id="form" method="POST" action="/upload_live">
        <input type="hidden" name="image_data" id="image_data">
    </form>

</div>

<script>

navigator.mediaDevices.getUserMedia({
    video:true
})
.then(stream=>{
    document.getElementById("video").srcObject = stream;
})
.catch(err=>{
    alert("Camera access denied or not available");
});

function capture(){

    const canvas = document.getElementById("canvas");
    const video = document.getElementById("video");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(video,0,0);

    const image = canvas.toDataURL("image/jpeg");

    document.getElementById("image_data").value = image;

    document.getElementById("form").submit();
}

</script>

</body>

</html>

"""


@app.route("/upload_live", methods=["POST"])
def upload_live():

    image_data = request.form["image_data"]

    image_data = image_data.split(",")[1]

    image_bytes = base64.b64decode(image_data)

    filepath = "static/uploads/live.jpg"

    with open(filepath, "wb") as f:
        f.write(image_bytes)

    result_path = detect_image(filepath)

    return f"""

    <html>

    <head>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>

    body{{
        background:#0f172a;
        color:white;
        text-align:center;
        padding-top:50px;
    }}

    .result-box{{
        background:#1e293b;
        padding:30px;
        border-radius:20px;
        width:80%;
        margin:auto;
    }}

    img{{
        border-radius:15px;
        margin-top:20px;
        width:70%;
        border:4px solid cyan;
    }}

    </style>

    </head>

    <body>

    <div class="result-box">

        <h1>Live Detection Result</h1>

        <img src='/{result_path}'>

        <br><br>

        <a href="/live">

            <button class="btn btn-success">
                Detect Again
            </button>

        </a>

        <a href="/">

            <button class="btn btn-primary">
                Back To Home
            </button>

        </a>

    </div>

    </body>

    </html>

    """


if __name__ == "__main__":
    app.run(debug=True)
