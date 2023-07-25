# Click & save image

# Import opencv for computer vision stuff
import cv2
# Import matplotlib so we can visualize an image
from matplotlib import pyplot as plt

def take_photo(): 
    cap = cv2.VideoCapture(2)
    ret, frame = cap.read()
    cv2.imwrite('webcamphoto.jpg', frame)
    cap.release()

take_photo()
print('Photo saved')