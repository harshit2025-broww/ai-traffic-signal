#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Button & LEDs
#define BUTTON_PIN 12
#define LED_WIFI 13
#define LED_GREEN 14
#define LED_RED 15

// 7-Segment Display via 74HC595
#define DATA_PIN 16   // DS
#define LATCH_PIN 17  // ST_CP
#define CLOCK_PIN 18  // SH_CP

const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
String serverUrl = "https://your-app-name.onrender.com/traffic";

// Camera pins for AI Thinker ESP32-CAM
#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27
#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22

// 7-segment digits map (common cathode)
const byte digits[10] = {
  B00111111, // 0
  B00000110, // 1
  B01011011, // 2
  B01001111, // 3
  B01100110, // 4
  B01101101, // 5
  B01111101, // 6
  B00000111, // 7
  B01111111, // 8
  B01101111  // 9
};

void setup() {
  Serial.begin(115200);

  // Button & LEDs
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_WIFI, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_RED, LOW);

  // 7-segment pins
  pinMode(DATA_PIN, OUTPUT);
  pinMode(LATCH_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);

  // WiFi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("\nWiFi connected!");
  digitalWrite(LED_WIFI, HIGH);

  // Camera config
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_QVGA;
  config.jpeg_quality = 12;
  config.fb_count = 1;

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Camera init failed!");
    return;
  }

  Serial.println("Camera ready. Press the button to capture.");
}

void displayNumber(int number) {
  int tens = number / 10;
  int units = number % 10;

  // Display tens
  digitalWrite(LATCH_PIN, LOW);
  shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, digits[tens]);
  digitalWrite(LATCH_PIN, HIGH);
  delay(5);

  // Display units
  digitalWrite(LATCH_PIN, LOW);
  shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, digits[units]);
  digitalWrite(LATCH_PIN, HIGH);
  delay(5);
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW) {
    delay(100); // debounce
    Serial.println("Capturing image...");

    camera_fb_t* fb = esp_camera_fb_get();
    if (!fb) {
      Serial.println("Camera capture failed!");
      return;
    }

    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "image/jpeg");

    int httpResponseCode = http.POST(fb->buf, fb->len);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Server Response:");
      Serial.println(response);

      StaticJsonDocument<200> doc;
      DeserializationError error = deserializeJson(doc, response);
      if (!error) {
        int timer = doc["timer"];
        const char* signal = doc["signal"];

        // Traffic LED control
        if (strcmp(signal, "GREEN") == 0) {
          digitalWrite(LED_GREEN, HIGH);
          digitalWrite(LED_RED, LOW);
        } else {
          digitalWrite(LED_GREEN, LOW);
          digitalWrite(LED_RED, HIGH);
        }

        Serial.print("Timer: ");
        Serial.println(timer);

        // Countdown on 7-segment
        for (int i = timer; i >= 0; i--) {
          displayNumber(i);
          delay(1000);
        }

        digitalWrite(LED_GREEN, LOW);
        digitalWrite(LED_RED, LOW);
      }
    } else {
      Serial.printf("Error sending image: %d\n", httpResponseCode);
    }

    http.end();
    esp_camera_fb_return(fb);
    delay(2000);
  }
}
