# Basic imports
import cv2
import numpy as np
import os

# Configurations
lower_skin = np.array([0, 54, 41])
upper_skin = np.array([19, 255, 255])

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


# Image Overlay Setup
image_path = 'image_4.png' 

if not os.path.exists(image_path):
    print(f"ERROR: {image_path} not found.")
    exit()

# Load image
overlay_raw = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# Resizing the Overlay Image
target_size = (150, 150)
overlay_resized = cv2.resize(overlay_raw, target_size)

# Preparing Masks
bgr_overlay = overlay_resized[:, :, :3] 
alpha_mask = overlay_resized[:, :, 3]   
inv_alpha_mask = cv2.bitwise_not(alpha_mask)

# Image Position
obj_center = (560, 400)
h, w = target_size
tl_x = obj_center[0] - w // 2
tl_y = obj_center[1] - h // 2
br_x = tl_x + w
br_y = tl_y + h

# Thresholds
dist_danger = w // 2 
dist_warning = 250

# Load image with Alpha Channel 
overlay_raw = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# Define Object Position and Size
obj_center = (560, 400) 
target_size = (150, 150) 

# Resize the overlay image
overlay_resized = cv2.resize(overlay_raw, target_size)

# Preparing masks for transparency
bgr_overlay = overlay_resized[:, :, :3] 
alpha_mask = overlay_resized[:, :, 3]   

inv_alpha_mask = cv2.bitwise_not(alpha_mask)

# Calculating placement coordinates based on center and size
h, w = target_size
tl_x = obj_center[0] - w // 2 # Top-Left X
tl_y = obj_center[1] - h // 2 # Top-Left Y
br_x = tl_x + w               # Bottom-Right X
br_y = tl_y + h               # Bottom-Right Y

# Distance threshold for collison 
dist_danger = w // 2 
dist_warning = 250

print("System Ready with Image Overlay. Press 'q' to exit.")

while True:
    success, frame = cap.read()
    if not success: break
    frame = cv2.flip(frame, 1)

    # Hand Detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask = cv2.GaussianBlur(mask, (5,5), 0)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    current_state = "SAFE"
    ui_color = (0, 255, 0) # Green 
    
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > 1000:
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                distance = np.sqrt((cx - obj_center[0])**2 + (cy - obj_center[1])**2)
                
                if distance < dist_danger:
                    current_state = "DANGER"
                    ui_color = (0, 0, 255) # Red
                elif distance < dist_warning:
                    current_state = "WARNING"
                    ui_color = (0, 255, 255) # Yellow
                
                # Drawing the line and dot on the hand
                cv2.line(frame, (cx, cy), obj_center, ui_color, 2)
                cv2.circle(frame, (cx, cy), 10, ui_color, -1)

    # Defining Region of Interest
    roi = frame[tl_y:br_y, tl_x:br_x]
    roi_bg = cv2.bitwise_and(roi, roi, mask=inv_alpha_mask)
    overlay_fg = cv2.bitwise_and(bgr_overlay, bgr_overlay, mask=alpha_mask)
    dst = cv2.add(roi_bg, overlay_fg)
    frame[tl_y:br_y, tl_x:br_x] = dst

    # DANGER Feedback
    if current_state == "DANGER":
         cv2.rectangle(frame, (tl_x, tl_y), (br_x, br_y), (0, 0, 255), 4)
         
         # Danger Text overlay
         text = "DANGER DANGER"
         font = cv2.FONT_HERSHEY_SIMPLEX
         text_size = cv2.getTextSize(text, font, 1.5, 4)[0]
         text_x = (640 - text_size[0]) // 2
         cv2.putText(frame, text, (text_x, 250), font, 1.5, (0, 0, 255), 4)

    # Status Text
    cv2.putText(frame, f"STATUS: {current_state}", (20, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, ui_color, 3)

    cv2.imshow("Camera Output", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()