
#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>

// Wi-Fi access point
const char* ssid = "SmartDustbin";
const char* password = "YOUR_WIFI_PASSWORD";

WebServer server(80);

// Servo pins
const int lidServoPin = 13;
const int sortServoPin = 14;

// Ultrasonic pins
const int trigPin = 5;
const int echoPin = 18;

Servo lidServo;
Servo sortServo;

// Adjust these after testing your cardboard mechanism
const int LID_CLOSED = 0;
const int LID_OPEN = 60;

const int PLASTIC_ANGLE = 40;
const int PAPER_ANGLE = 90;
const int METAL_ANGLE = 140;

const float DETECT_DISTANCE_CM = 20.0;
const unsigned long CLOSE_DELAY_MS = 2000;

bool lidIsOpen = false;
unsigned long lastObjectSeen = 0;

float getDistanceCM() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(3);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  unsigned long duration = pulseIn(echoPin, HIGH, 30000);

  if (duration == 0) {
    return -1.0;
  }

  return duration * 0.0343 / 2.0;
}

void handleSort() {
  if (!server.hasArg("type")) {
    server.send(400, "text/plain", "Missing waste type");
    return;
  }

  String waste = server.arg("type");
  waste.toLowerCase();
  waste.trim();

  if (waste == "plastic") {
    sortServo.write(PLASTIC_ANGLE);
  } else if (waste == "paper") {
    sortServo.write(PAPER_ANGLE);
  } else if (waste == "metal") {
    sortServo.write(METAL_ANGLE);
  } else {
    server.send(400, "text/plain", "Invalid waste type");
    return;
  }

  Serial.print("Waste type received: ");
  Serial.println(waste);

  server.send(200, "text/plain", "Sorting position set: " + waste);
}

void setup() {
  Serial.begin(115200);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  lidServo.setPeriodHertz(50);
  sortServo.setPeriodHertz(50);

  lidServo.attach(lidServoPin, 500, 2400);
  sortServo.attach(sortServoPin, 500, 2400);

  lidServo.write(LID_CLOSED);
  sortServo.write(PAPER_ANGLE);

  WiFi.mode(WIFI_AP);

  if (WiFi.softAP(ssid, password)) {
    Serial.println("Smart Dustbin Wi-Fi started");
    Serial.print("IP address: ");
    Serial.println(WiFi.softAPIP());
  } else {
    Serial.println("Wi-Fi start failed");
  }

  server.on("/sort", HTTP_GET, handleSort);
  server.begin();

  Serial.println("Smart Dustbin ready");
}

void loop() {
  // Keep accepting AI sorting requests
  server.handleClient();

  float distance = getDistanceCM();
  unsigned long now = millis();

  if (distance > 0 && distance <= DETECT_DISTANCE_CM) {
    lastObjectSeen = now;

    if (!lidIsOpen) {
      lidServo.write(LID_OPEN);
      lidIsOpen = true;
      Serial.println("Object detected - lid OPEN");
    }
  }

  if (lidIsOpen && now - lastObjectSeen >= CLOSE_DELAY_MS) {
    lidServo.write(LID_CLOSED);
    lidIsOpen = false;
    Serial.println("Object absent - lid CLOSED");
  }

  delay(50);
}
