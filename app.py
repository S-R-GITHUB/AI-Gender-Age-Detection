from flask import Flask, render_template, request, Response
import os
from detector import detect_image, generate_frames

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
    
        <a
            href='/{result_path}'
            download
        >
    
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

<html>

<head>

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

<style>

body{
    background:#0f172a;
    color:white;
    text-align:center;
    padding-top:40px;
}

.live-box{
    background:#1e293b;
    padding:30px;
    border-radius:20px;
    width:85%;
    margin:auto;
}

img{
    border-radius:15px;
    margin-top:20px;
    width:80%;
    border:4px solid #38bdf8;
}

.btn-custom{
    margin-top:20px;
    padding:12px 25px;
    font-size:18px;
}

</style>

</head>

<body>

<div class="live-box">

    <h1>
        Live AI Detection
    </h1>

    <img src="/video_feed">

    <br>

    <a href="/">

        <button class="btn btn-danger btn-custom">

            Stop Camera

        </button>

    </a>

    <a href="/">

        <button class="btn btn-primary btn-custom">

            Back To Home

        </button>

    </a>

</div>

</body>

</html>

"""


@app.route('/video_feed')
def video_feed():

    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


if __name__ == "__main__":
    app.run(debug=True)