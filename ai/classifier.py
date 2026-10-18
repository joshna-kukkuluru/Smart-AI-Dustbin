from ultralytics import YOLO
import cv2

# Pre-trained YOLO model
model = YOLO("yolo11n.pt")

# Laptop camera
camera = cv2.VideoCapture(0)

while True:

    ret, frame = camera.read()

    if not ret:
        print("Camera not detected")
        break

    # AI detection
    results = model(frame)

    # Draw detections
    annotated_frame = results[0].plot()

    cv2.imshow("Smart Dustbin AI", annotated_frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()