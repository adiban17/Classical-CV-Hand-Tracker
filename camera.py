# Basic Imports
import cv2
import time

# Camera Initilization
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

# Resolution Configuration
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) 

# FPS Calc Variables
prev_time = 0
new_time = 0

print("Camera initialized. Press 'q' to exit.")

# Main Loop
while True:
    
    # Reading Frames
    success, frame = cap.read()
    
    if not success:
        print("Error: Failed to read frame.")
        break

    frame = cv2.flip(frame, 1)

    # FPS Calculation
    new_time = time.time()
    fps = 1 / (new_time - prev_time)
    prev_time = new_time

    # FPS Display
    fps_text = f"FPS: {int(fps)}"
    cv2.putText(frame, fps_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                1, (0, 255, 0), 2)
    cv2.imshow("Camera Test", frame)

    # Exit Condition Check
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()