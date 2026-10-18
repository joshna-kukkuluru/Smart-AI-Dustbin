
import cv2
import numpy as np
import tensorflow as tf
import requests

MODEL_PATH = "ai/models/waste_classifier_mobilenet_v2_new.keras"
CLASS_PATH = "ai/models/class_names_mobilenet_v2_new.txt"
ESP32_URL = "http://192.168.4.1/sort"

CONFIDENCE_THRESHOLD = 80.0
SAMPLES_TO_CHECK = 5

model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_PATH, "r") as file:
    class_names = [line.strip() for line in file if line.strip()]

print("Loaded classes:", class_names)

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera open avvaledhu!")
    raise SystemExit

locked_class = None
locked_confidence = 0.0
message = "Show one item, then press S to scan"

print("\nS = Scan and lock category")
print("R = Reset after dropping the item")
print("Q = Quit")

try:
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Camera frame read avvaledhu.")
            break

        display = frame.copy()

        if locked_class is not None:
            status = (
                f"LOCKED: {locked_class.upper()} "
                f"({locked_confidence:.1f}%)"
            )
        else:
            status = message

        cv2.putText(
            display, status, (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 0.65,
            (0, 255, 0) if locked_class else (0, 200, 255), 2
        )

        cv2.imshow("Smart Dustbin - Category Lock", display)
        key = cv2.waitKey(1) & 0xFF

        if key in (ord("q"), ord("Q")):
            break

        if key in (ord("r"), ord("R")):
            locked_class = None
            locked_confidence = 0.0
            message = "Ready for next item"
            print("Category lock reset. Show the next item.")
            continue

        if key in (ord("s"), ord("S")):
            if locked_class is not None:
                print("An item is already locked. Press R first.")
                continue

            # Capture several frames and average their predictions.
            predictions = []

            for _ in range(SAMPLES_TO_CHECK):
                ret, scan_frame = camera.read()
                if not ret:
                    continue

                resized = cv2.resize(scan_frame, (160, 160))
                rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                image = np.expand_dims(rgb, axis=0).astype(np.float32)

                probs = model.predict(image, verbose=0)[0]
                predictions.append(probs)

            if len(predictions) != SAMPLES_TO_CHECK:
                message = "Could not scan. Try S again."
                print(message)
                continue

            avg_probs = np.mean(predictions, axis=0)
            best_index = int(np.argmax(avg_probs))
            best_class = class_names[best_index]
            best_confidence = float(avg_probs[best_index]) * 100

            print(
                "Scan result:",
                best_class,
                f"({best_confidence:.1f}%)"
            )

            if best_confidence < CONFIDENCE_THRESHOLD:
                message = "Low confidence - show item clearly and press S"
                print(message)
                continue

            try:
                response = requests.get(
                    ESP32_URL,
                    params={"type": best_class},
                    timeout=3
                )

                if response.status_code == 200:
                    locked_class = best_class
                    locked_confidence = best_confidence
                    message = f"Locked: {best_class.upper()}"

                    print("Category locked:", locked_class)
                    print("ESP32 response:", response.text)
                    print("Drop this item, then press R.")
                else:
                    message = "ESP32 rejected command. Try S again."
                    print("ESP32 error:", response.status_code, response.text)

            except requests.RequestException as error:
                message = "Wi-Fi error. Check ESP32 connection."
                print(message, error)

finally:
    camera.release()
    cv2.destroyAllWindows()
