import cv2
import numpy as np
import os
labels = []
images = []
def detection(_frame):
    global labels
    global images
    # 웹캠 신호 받기
    #VideoSignal = cv2.VideoCapture(0)
    # YOLO 가중치 파일과 CFG 파일 로드

    YOLO_net = cv2.dnn.readNet(r"yolov2-tiny.weights",r"yolov2-tiny.cfg")

    # YOLO NETWORK 재구성
    classes = []
    with open(r"yolo.names", "r", encoding='utf-8') as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = YOLO_net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in YOLO_net.getUnconnectedOutLayers()]

    while True:
        key = cv2.waitKey(100)
        # 웹캠 프레임
        #ret, frame = VideoSignal.read()
        frame = _frame
        h, w, c = frame.shape
        cap_flag = False
        game_mode = False

        # YOLO 입력
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
        True, crop=False)
        YOLO_net.setInput(blob)
        outs = YOLO_net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []
        labels = []
        images = []
        for out in outs:

            for detection in out:

                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * w)
                    center_y = int(detection[1] * h)
                    dw = int(detection[2] * w)
                    dh = int(detection[3] * h)
                    # Rectangle coordinate
                    x = int(center_x - dw / 2)
                    y = int(center_y - dh / 2)
                    boxes.append([x, y, dw, dh])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)
        temp_img = frame.copy()
        if key == ord('c'):
            cap_flag = True
        elif key == ord('g'):
            game_mode = True

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])

                #labels = ['ab','afb','abfb']
                #print(label)

                roi = frame[y:y + h, x:x + w]  # roi 지정
                saveImage = roi.copy()
                if label not in labels:
                    labels.append(label)
                    images.append(saveImage)

                score = confidences[i]


                # 경계상자와 클래스 정보 이미지에 입력
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
                cv2.putText(frame, label, (x, y - 20), cv2.FONT_ITALIC, 1,(0, 0, 255), 2)


        #cv2.imshow("YOLOv3", frame)
        return frame
        #if cv2.waitKey(100) > 0:
        #    break

def detection2(_frame):
    global labels
    # 웹캠 신호 받기
    #VideoSignal = cv2.VideoCapture(0)
    # YOLO 가중치 파일과 CFG 파일 로드
    YOLO_net = cv2.dnn.readNet(r"/Users/whistle/Downloads/LanguageStudy-master/yolov2-tiny.weights",r"/Users/whistle/Downloads/LanguageStudy-master/yolov2-tiny.cfg")

    # YOLO NETWORK 재구성
    classes = []
    with open(r"/Users/whistle/Downloads/LanguageStudy-master/yolo.names", "r", encoding='utf-8') as f:
        classes = [line.strip() for line in f.readlines()]
        print(classes)
    layer_names = YOLO_net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in YOLO_net.getUnconnectedOutLayers()]

    while True:
        key = cv2.waitKey(100)
        # 웹캠 프레임
        #ret, frame = VideoSignal.read()
        frame = _frame
        h, w, c = frame.shape
        cap_flag = False
        game_mode = False

        # YOLO 입력
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
        True, crop=False)
        YOLO_net.setInput(blob)
        outs = YOLO_net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []
        labels = []

        for out in outs:

            for detection in out:

                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * w)
                    center_y = int(detection[1] * h)
                    dw = int(detection[2] * w)
                    dh = int(detection[3] * h)
                    # Rectangle coordinate
                    x = int(center_x - dw / 2)
                    y = int(center_y - dh / 2)
                    boxes.append([x, y, dw, dh])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)
        temp_img = frame.copy()
        if key == ord('c'):
            cap_flag = True
        elif key == ord('g'):
            game_mode = True

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                if label not in labels:
                    labels.append(label)

                #labels = ['ab','afb','abfb']
                #print(label)

                roi = frame[y:y + h, x:x + w]  # roi 지정
                saveImage = roi.copy()


                score = confidences[i]


                # 경계상자와 클래스 정보 이미지에 입력
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, label, (x, y - 20), cv2.FONT_ITALIC, 1,(0, 0, 255), 2)


        #cv2.imshow("YOLOv3", frame)
        return frame
        #if cv2.waitKey(100) > 0:
        #    break
