import numpy as np 
import cv2

cap = cv2.VideoCapture(0)

while True:
    r, frame = cap.read()
    cv2.imshow("my face", frame)
    if cv2.waitKey(1) == ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()
