import cv2 as cv
import os
faceProto = "models/opencv_face_detector.pbtxt"
faceModel = "models/opencv_face_detector_uint8.pb"

ageProto = "models/age_deploy.prototxt"
ageModel = "models/age_net.caffemodel"

genderProto = "models/gender_deploy.prototxt"
genderModel = "models/gender_net.caffemodel"

MODEL_MEAN_VALUES = (
    78.4263377603,
    87.7689143744,
    114.895847746
)

ageList = [
    '(0-2)',
    '(4-6)',
    '(8-12)',
    '(15-20)',
    '(25-32)',
    '(38-43)',
    '(48-53)',
    '(60-100)'
]

genderList = ['Male', 'Female']

faceNet = cv.dnn.readNet(faceModel, faceProto)

ageNet = cv.dnn.readNet(ageModel, ageProto)

genderNet = cv.dnn.readNet(genderModel, genderProto)
def detect_image(image_path):

    frame = cv.imread(image_path)

    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    blob = cv.dnn.blobFromImage(
        frame,
        1.0,
        (300, 300),
        [104, 117, 123],
        True,
        False
    )

    faceNet.setInput(blob)

    detections = faceNet.forward()

    for i in range(detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > 0.7:

            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)

            face = frame[
                max(0, y1-20):min(y2+20, frame.shape[0]-1),
                max(0, x1-20):min(x2+20, frame.shape[1]-1)
            ]

            blob2 = cv.dnn.blobFromImage(
                face,
                1.0,
                (227, 227),
                MODEL_MEAN_VALUES,
                swapRB=False
            )

            genderNet.setInput(blob2)
            genderPreds = genderNet.forward()

            gender = genderList[genderPreds[0].argmax()]

            genderConfidence = genderPreds[0].max() * 100


            ageNet.setInput(blob2)
            agePreds = ageNet.forward()

            age = ageList[agePreds[0].argmax()]

            ageConfidence = agePreds[0].max() * 100


            label = (
                f"{gender} ({genderConfidence:.1f}%) "
                f"| {age} ({ageConfidence:.1f}%)"
            )

            cv.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 255),
                3
            )

            label_y = y1 - 15 if y1 - 15 > 15 else y1 + 15

            cv.rectangle(
                frame,
                (x1, label_y - 25),
                (x1 + 320, label_y + 5),
                (0, 255, 255),
                -1
            )

            cv.putText(
                frame,
                label,
                (x1 + 5, label_y),
                cv.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2
            )

    output_path = "static/output/result.jpg"

    cv.imwrite(output_path, frame)

    return output_path
    
def generate_frames():

    cap = cv.VideoCapture(0, cv.CAP_DSHOW)

    while True:

        success, frame = cap.read()

        if not success:
            break

        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        blob = cv.dnn.blobFromImage(
            frame,
            1.0,
            (300, 300),
            [104, 117, 123],
            True,
            False
        )

        faceNet.setInput(blob)

        detections = faceNet.forward()

        for i in range(detections.shape[2]):

            confidence = detections[0, 0, i, 2]

            if confidence > 0.7:

                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)

                face = frame[
                    max(0, y1-20):min(y2+20, frame.shape[0]-1),
                    max(0, x1-20):min(x2+20, frame.shape[1]-1)
                ]

                blob2 = cv.dnn.blobFromImage(
                    face,
                    1.0,
                    (227, 227),
                    MODEL_MEAN_VALUES,
                    swapRB=False
                )

                genderNet.setInput(blob2)
                genderPreds = genderNet.forward()

                gender = genderList[genderPreds[0].argmax()]

                genderConfidence = genderPreds[0].max() * 100


                ageNet.setInput(blob2)
                agePreds = ageNet.forward()

                age = ageList[agePreds[0].argmax()]

                ageConfidence = agePreds[0].max() * 100


                label = (
                    f"{gender} ({genderConfidence:.1f}%) "
                    f"| {age} ({ageConfidence:.1f}%)"
                )

                cv.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 255),
                    3
                )

                label_y = y1 - 15 if y1 - 15 > 15 else y1 + 15
                
                cv.rectangle(
                    frame,
                    (x1, label_y - 25),
                    (x1 + 320, label_y + 5),
                    (0, 255, 255),
                    -1
                )
                
                cv.putText(
                    frame,
                    label,
                    (x1 + 5, label_y),
                    cv.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 0),
                    2
                )

        ret, buffer = cv.imencode('.jpg', frame)

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )