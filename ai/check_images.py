
import os
from PIL import Image

folders = {
    "Plastic": "ai/datasets/plastic",
    "Paper": "ai/datasets/paper",
    "Metal": "ai/datasets/metal"
}

for name, folder in folders.items():
    valid = 0
    invalid = []

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)

        try:
            with Image.open(path) as img:
                img.verify()
            valid += 1
        except Exception:
            invalid.append(filename)

    print(f"\n{name}")
    print("Readable images:", valid)
    print("Unreadable images:", len(invalid))

    if invalid:
        print("Files to inspect:", invalid)
