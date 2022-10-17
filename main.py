import cv2
import imutils
from tracker import *

tracker = EuclideanDestTracker()

cap = cv2.VideoCapture('highway.mp4')

object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50)

while True:
    ret, frame = cap.read()
    # frame = imutils.resize(frame, width=600)

    if ret is False:
        break

    # extract region of interest
    # roi = frame[145:373, 129:203]
    # roi = frame[276:434, 598:799]
    roi = frame[229:435, 616:780]



    # 1. object detection

    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detections = []

    for cnt in contours:
        # calculate area
        area = cv2.contourArea(cnt)

        if area > 100:
            # cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)

            x, y, w, h = cv2.boundingRect(cnt)

            detections.append([x, y, w, h])

    print('detections: ', detections)

    # 2. Object tracking

    boxes_ids= tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y-10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)



    cv2.imshow('Frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('roi', roi)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()