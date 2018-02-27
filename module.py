import os
import cv2
import json
import time

from detector import Detector
from sender import Sender

# Can be used to change used camera in case multiple available
CAMERA_INDEX = int(os.getenv('OPENCV_CAMERA_INDEX', 0))

# These variables are set by the IoT Edge Agent
CONNECTION_STRING = os.getenv('EdgeHubConnectionString', False)
CA_CERTIFICATE = os.getenv('EdgeModuleCACertificateFile', False)
IS_EDGE = CONNECTION_STRING and CA_CERTIFICATE or False

if IS_EDGE:
    sender = Sender(CONNECTION_STRING, CA_CERTIFICATE)
else:
    sender = False

video_capture = cv2.VideoCapture(CAMERA_INDEX)
detector = Detector()
detection_id = 0

while True:
    capture = video_capture.read()
    if capture[0]:
        array = capture[1]
        type = 'captured'
    else:
        type = 'static'
        array = cv2.imread('data/dog.jpg')

    print('Using %s %ix%i image' % (type, array.shape[0], array.shape[1]))
    result = detector.detect(array)
    print(json.dumps(result, indent=4))

    if sender:
        detection_id += 1
        msg_properties = {
            'detection_id': str(detection_id)
        }
        json_formatted = json.dumps(result)
        sender.send_event_to_output('detectionOutput', json_formatted, msg_properties, detection_id)

    # To avoid sending too frequently on hardware where detection is fast
    time.sleep(1)
