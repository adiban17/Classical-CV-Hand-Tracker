# Classical CV Hand Tracker 🖐️📷

A real-time hand tracking and virtual object interaction prototype built using **pure OpenCV**. 
Designed to run efficiently on CPU without relying on heavy deep learning frameworks or pose estimation APIs (like MediaPipe or OpenPose).

> **Context:** Created for the Arvyax Machine Learning Internship Assessment.

---

## 🚀 Key Features
* **Zero-ML Tracking:** Uses HSV Color Segmentation and Contour Analysis to track hand movements.
* **High Performance:** Optimized for CPU execution, achieving **30+ FPS** on standard hardware (Target was ≥8 FPS).
* **Interactive Virtual Object:** Detects proximity to a virtual object (Puppy overlay) and triggers dynamic state changes.
* **Smart Overlay:** Uses **Alpha Blending & Bitwise Masking** to render images over the video feed, handling transparency even for JPGs.
* **3-Stage Safety Logic:**
    * 🟢 **SAFE:** Hand is at a safe distance.
    * 🟡 **WARNING:** Hand is approaching the object.
    * 🔴 **DANGER:** Hand has breached the object boundary (Visual + Text Alert).

---

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Libraries:** `OpenCV` (cv2), `NumPy`
* **Techniques:**
    * Color Space Conversion (BGR → HSV)
    * Morphological Operations (Erosion/Dilation for noise removal)
    * Contour Detection & Image Moments (Centroid Calculation)
    * Euclidean Distance Logic
    * ROI (Region of Interest) Processing

---

## 👤 Author
**Aditya Banerjee**

[LinkedIn](https://www.linkedin.com/in/aditya-banerjee-08117b310/)  
[GitHub](https://github.com/adiban17)

