
import cv2
import os

# Project and dataset paths
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(PROJECT_DIR, "ai", "datasets")

# Category keys and folders
folders = {
    ord("p"): ("plastic", os.path.join(DATASET_DIR, "plastic")),
    ord("a"): ("paper", os.path.join(DATASET_DIR, "paper")),
    ord("m"): ("metal", os.path.join(DATASET_DIR, "metal")),
}

# Create dataset folders
for _, folder in folders.values():
    os.makedirs(folder, exist_ok=True)


def get_next_count(folder, prefix):
    numbers = []

    for filename in os.listdir(folder):
        name, ext = os.path.splitext(filename)

        if name.startswith(prefix + "_") and ext.lower() == ".jpg":
            try:
                numbers.append(int(name[len(prefix) + 1:]))
            except ValueError:
                pass

    return max(numbers, default=0)


# Find existing image counts
counts = {
    key: get_next_count(folder, name)
    for key, (name, folder) in folders.items()
}

print("SMART AI DUSTBIN - IMAGE COLLECTION")
print("------------------------------------")
print("P = Save Plastic image")
print("A = Save Paper image")
print("M = Save Metal image")
print("Q = Quit")
print("\nDataset location:", DATASET_DIR)

# Open camera
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("ERROR: Camera could not be opened.")
    raise SystemExit

print("\nCamera ready!")
print("Click the camera window and press P, A, or M.")
print("Press Q to quit.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("ERROR: Camera frame could not be read.")
        break

    display = frame.copy()

    cv2.putText(
        display,
        "P: Plastic | A: Paper | M: Metal | Q: Quit",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    cv2.imshow("Waste Image Collection", display)
    key = cv2.waitKey(30) & 0xFF

    # Quit
    if key in (ord("q"), ord("Q")):
        break

    # Save image for selected category
    if key in folders:
        class_name, folder = folders[key]
        counts[key] += 1

        filename = os.path.join(
            folder,
            f"{class_name}_{counts[key]:04d}.jpg"
        )

        success = cv2.imwrite(filename, frame)

        if success:
            print(f"{class_name.capitalize()} saved: {filename}")
        else:
            counts[key] -= 1
            print("SAVE FAILED:", filename)

camera.release()
cv2.destroyAllWindows()

print("\nImage collection completed!")

for key, (name, folder) in folders.items():
    print(f"{name.capitalize()} images: {counts[key]}")
