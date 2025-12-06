import cv2
import numpy as np

# Configurations
lower_skin = np.array([0, 54, 41])
upper_skin = np.array([19, 255, 255])

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, frame = cap.read()
    if not success: break
    
    # FLip Frame
    frame = cv2.flip(frame, 1)

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create Mask
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Clean up Mask
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask = cv2.GaussianBlur(mask, (5,5), 0)

    # Find Contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Tracking Logic
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)
        
        if area > 1000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)
                cv2.putText(frame, f"({cx}, {cy})", (cx - 20, cy - 20), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Show results
    cv2.imshow("Arvyax Phase 3: Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Cleanup
cap.release()
cv2.destroyAllWindows()