#include <ArduinoJson.h>
#include <Servo.h>

// Create a servo object
Servo steeringServo;

// Define pin assignments
const int throttlePin = 6;  // Throttle (PWM pin, 0-255)
const int brakePin = 8;      // Brake (digital pin, 0 or 1)
const int steeringPin = 9;   // Steering (servo pin, 0-180 degrees)

// Define the maximum size of the JSON object
const size_t capacity = JSON_OBJECT_SIZE(3);
DynamicJsonDocument doc(capacity);

void setup() {
  Serial.begin(9600); // Opens serial port, sets data rate to 9600 bps (8N1)
  steeringServo.attach(steeringPin); // Attach the servo to pin 9
  pinMode(brakePin, OUTPUT); // Set the brake pin as an output
  digitalWrite(brakePin, LOW); // Ensure brake is off initially
}

void loop() {
  if (Serial.available()) {
    // Read data from serial
    String data = Serial.readStringUntil('\n');
    
    // Parse JSON data
    if (deserializeJson(doc, data) == DeserializationError::Ok) {
      // Extract values from JSON
      int throttleValue = doc["t"];     // Throttle value
      int brakeValue = doc["b"];         // Brake state (0 or 1)
      int steeringValue = doc["s"];      // Steering angle (0-180 degrees)

      // Process the received data
      // Write the throttle value directly to the PWM pin (0-255)
      analogWrite(throttlePin, throttleValue); // Directly use the received value

      // Set the brake state directly
      digitalWrite(brakePin, brakeValue); // Use 1 for HIGH, 0 for LOW

      // Write the steering value directly to the servo (0-180 degrees)
      steeringServo.write(steeringValue); // Directly use the received value
    } else {
      Serial.println("Failed to parse JSON data.");
    }
  }
}
