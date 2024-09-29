#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "SHIVANSH";          // Replace with your Wi-Fi network name
const char* password = "shivansh";      // Replace with your Wi-Fi password
const char* apiUrl = "http://192.168.27.62:5001/message"; // Replace with the actual server's IP

WiFiClient client;

void setup() {
  delay(1000);  // Delay for stability
  Serial.begin(115200);   // Start serial communication
  WiFi.begin(ssid, password); // Connect to the Wi-Fi network

  // Connect to Wi-Fi
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(client, apiUrl);  // Specify the URL

    int httpCode = http.GET(); // Make the GET request

    if (httpCode > 0) {
      String payload = http.getString();  // Get the response payload
      Serial.println(payload);            // Print the received message from API
    } else {
      Serial.println(" ");
    }

    http.end();  // End the HTTP connection

  } else {
    Serial.println("Wi-Fi not connected");
  }

  delay(5000);  // Wait for 5 seconds before making the next request
}
