
import os

folders = {
    "Plastic": "ai/datasets/plastic",
    "Paper": "ai/datasets/paper",
    "Metal": "ai/datasets/metal"
}

for name, folder in folders.items():
    if os.path.exists(folder):
        images = [
            f for f in os.listdir(folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png",".webp"))
        ]
        print(f"{name}: {len(images)} images")
    else:
        print(f"{name}: Folder not found")

