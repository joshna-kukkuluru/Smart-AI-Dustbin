# Smart AI Dustbin

An AI-powered smart waste segregation system that classifies waste into Plastic, Paper, and Metal using a webcam and MobileNetV2, then controls an ESP32-based servo mechanism to direct waste into the corresponding compartment.

## Project Overview

The Smart AI Dustbin combines computer vision, machine learning, and embedded systems to help segregate waste into three categories.

A laptop webcam captures the waste item. The trained AI model predicts its category, and Python sends the selected category to the ESP32 over Wi-Fi. The ESP32 controls a servo-driven sorting flap to direct the waste into the appropriate compartment.

## Features

- AI-based classification of Plastic, Paper, and Metal
- Custom-trained MobileNetV2 model
- Webcam-based waste recognition
- ESP32 Wi-Fi communication
- Servo-controlled waste sorting
- Ultrasonic sensor-based lid opening and closing
- Category lock to keep the selected waste category fixed while the item is moved
- Three separate waste compartments

## Technologies Used

- Python
- TensorFlow / Keras
- OpenCV
- NumPy
- Requests
- ESP32
- Arduino IDE
- HC-SR04 Ultrasonic Sensor
- Servo Motors

## Hardware Components

- ESP32 development board
- HC-SR04 ultrasonic sensor
- Two servo motors
- Regulated 5V power supply for servos
- Jumper wires and breadboard
- Cardboard enclosure with three waste compartments

## Waste Categories

| Category | Sorting position |
|---|---|
| Plastic | Left — 40° |
| Paper | Center — 90° |
| Metal | Right — 140° |

Servo angles may need adjustment depending on the physical sorting mechanism.

## Project Structure

```text
Smart_Ai_Dustbin/
├── ai/
│   ├── datasets/
│   │   ├── plastic/
│   │   ├── paper/
│   │   └── metal/
│   ├── models/
│   ├── test_webcam.py
│   ├── train_mobilenet.py
│   └── wifi_test.py
├── esp32/
│   └── smart_dustbin.ino
├── .gitignore
└── README.md
```

## Setup and Execution

### 1. Create and activate a Python environment

Use Python 3.12 and install the required packages in your environment.

```bash
pip install tensorflow opencv-python numpy requests
```

### 2. Prepare the AI model

Ensure the trained model and class names files are available in `ai/models/`.

### 3. Configure the ESP32

Open `esp32/smart_dustbin.ino` in Arduino IDE, verify the pin connections and Wi-Fi configuration, and upload the sketch to the ESP32.

### 4. Connect to the ESP32 Wi-Fi

Connect the laptop to the Wi-Fi network configured in the ESP32 sketch.

### 5. Run the AI application

From the project root directory, run:

```bash
python ai/test_webcam.py
```

### 6. Use category locking

- Press `S` to scan and lock the current waste category.
- Place the item into the dustbin.
- Press `R` to reset the category for the next item.
- Press `Q` to close the application.

## Model Performance

The latest training run achieved:

- Training accuracy: 91.28%
- Validation accuracy: 83.72%

Actual performance may vary with lighting, object orientation, background, and the type of waste item.

## Current Limitations

- Category reset currently requires the user to press `R`.
- Classification is limited to Plastic, Paper, and Metal.
- Servo angles and mechanical alignment depend on the physical enclosure.

## Future Enhancements

- Automatic category reset after waste insertion
- Improved classification with more diverse training images
- Better mechanical enclosure and sorting flap
- Waste sorting statistics and monitoring dashboard

## Safety Notes

- Use a regulated power supply suitable for the servo motors.
- Connect the external servo supply ground to ESP32 ground.
- Connect the HC-SR04 Echo output to the ESP32 through a suitable voltage divider.
- Keep wires away from moving servo arms and hinges.

## Author
Joshna KUKKULURU 
https://github.com/joshna-kukkuluru
## License

Choose and add an appropriate open-source license before publishing the repository.
