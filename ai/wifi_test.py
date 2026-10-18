
import requests

ESP32_URL = "http://192.168.4.1/sort"

while True:
    waste = input(
        "Enter plastic, paper, metal or q to quit: "
    ).strip().lower()

    if waste == "q":
        break

    if waste not in ["plastic", "paper", "metal"]:
        print("Please enter a valid waste type.")
        continue

    try:
        response = requests.get(
            ESP32_URL,
            params={"type": waste},
            timeout=5
        )
        print("ESP32 response:", response.text)

    except requests.RequestException as error:
        print("Connection error:", error)
