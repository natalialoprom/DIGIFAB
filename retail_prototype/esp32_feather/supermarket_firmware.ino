#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_BME680.h>

#define SDA_PIN 23
#define SCL_PIN 22

Adafruit_BME680 bme(&Wire);

// ---------- WiFi ----------
const char* ssid = "test";
const char* password = "1234";
const char* serverBase = "http://10.179.209.141:5000/update";

// ---------- Product ----------
const char* productName = "Oranges";
const char* freshPrice = "3.49 NOK";
const char* useSoonPrice = "2.79 NOK";
const char* discountPrice = "1.99 NOK";

// ---------- Sensor / baseline ----------
const int WARMUP_MS = 60000;          
const int BASELINE_SAMPLES = 20;
const int SAMPLE_DELAY_MS = 2000;

float baselineTemp = 0.0;
float baselineHum = 0.0;
float baselineGas = 0.0;
bool baselineReady = false;

// Smoothing
const int SMOOTH_N = 5;
float gasDropHist[SMOOTH_N] = {0};
float humDeltaHist[SMOOTH_N] = {0};
int histIdx = 0;
bool histFilled = false;

// Temporal confirmation
String lastRawStatus = "Fresh";
String stableStatus = "Fresh";
int sameStatusCount = 0;
const int REQUIRED_CONFIRMATIONS = 3;

// Actual data reading and processing functions
bool readSensor(float &tempC, float &humPct, float &pressHpa, float &gasKOhms) {
  if (!bme.performReading()) return false;

  tempC = bme.temperature;
  humPct = bme.humidity;
  pressHpa = bme.pressure / 100.0;
  gasKOhms = bme.gas_resistance / 1000.0;
  return true;
}

void calibrateBaseline() {
  Serial.println("Calibrating baseline in ambient air...");
  float tSum = 0.0, hSum = 0.0, gSum = 0.0;
  int valid = 0;

  for (int i = 0; i < BASELINE_SAMPLES; i++) {
    float t, h, p, g;
    if (readSensor(t, h, p, g)) {
      tSum += t;
      hSum += h;
      gSum += g;
      valid++;

      Serial.print("Baseline sample ");
      Serial.print(i + 1);
      Serial.print("/");
      Serial.print(BASELINE_SAMPLES);
      Serial.print(" | T=");
      Serial.print(t, 2);
      Serial.print("C H=");
      Serial.print(h, 2);
      Serial.print("% G=");
      Serial.print(g, 2);
      Serial.println(" kOhms");
    }
    delay(SAMPLE_DELAY_MS);
  }

  if (valid > 0) {
    baselineTemp = tSum / valid;
    baselineHum = hSum / valid;
    baselineGas = gSum / valid;
    baselineReady = true;

    Serial.println("Baseline ready:");
    Serial.print("Baseline Temp = "); Serial.println(baselineTemp, 2);
    Serial.print("Baseline Hum  = "); Serial.println(baselineHum, 2);
    Serial.print("Baseline Gas  = "); Serial.println(baselineGas, 2);
  }
}

void addToHistory(float gasDropPct, float deltaHumPct) {
  gasDropHist[histIdx] = gasDropPct;
  humDeltaHist[histIdx] = deltaHumPct;
  histIdx = (histIdx + 1) % SMOOTH_N;
  if (histIdx == 0) histFilled = true;
}

float averageArray(float* arr, int n) {
  int count = histFilled ? n : histIdx;
  if (count <= 0) return 0.0;

  float sum = 0.0;
  for (int i = 0; i < count; i++) sum += arr[i];
  return sum / count;
}

String classifyOrangeState(float gasDropPctSmoothed, float deltaHumPctSmoothed) {
  if (gasDropPctSmoothed >= 30.0 || deltaHumPctSmoothed >= 10.0) {
    return "Discount";
  }
  if (gasDropPctSmoothed >= 10.0 || deltaHumPctSmoothed >= 6.0) {
    return "Use soon";
  }
  return "Fresh";
}

String stabilizeState(String rawState) {
  if (rawState == lastRawStatus) {
    sameStatusCount++;
  } else {
    lastRawStatus = rawState;
    sameStatusCount = 1;
  }

  if (sameStatusCount >= REQUIRED_CONFIRMATIONS) {
    stableStatus = rawState;
  }

  return stableStatus;
}

String priceForStatus(String status) {
  if (status == "Fresh") return freshPrice;
  if (status == "Use soon") return useSoonPrice;
  return discountPrice;
}

void sendTagUpdate(String product, String status, String price, String temp, String hum, String gas) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected");
    return;
  }

  HTTPClient http;
  String url = String(serverBase) +
               "?product=" + product +
               "&status=" + status +
               "&price=" + price +
               "&temp=" + temp +
               "&hum=" + hum +
               "&gas=" + gas;

  url.replace(" ", "%20");

  Serial.println("Sending URL:");
  Serial.println(url);

  http.begin(url);
  int httpCode = http.GET();

  Serial.print("HTTP code: ");
  Serial.println(httpCode);

  String payload = http.getString();
  Serial.print("Response: ");
  Serial.println(payload);

  http.end();
}

void connectWifi() {
  WiFi.persistent(false);
  WiFi.mode(WIFI_OFF);
  delay(1000);
  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);
  delay(1000);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Wire.begin(SDA_PIN, SCL_PIN);

  if (!bme.begin(0x77)) {
    Serial.println("Could not find BME680/BME688");
    while (1) delay(10);
  }

  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150);

  Serial.println("Warm-up started...");
  delay(WARMUP_MS);

  calibrateBaseline();
  connectWifi();
}

void loop() {
  if (!baselineReady) {
    delay(5000);
    return;
  }

  float tempC, humPct, pressHpa, gasKOhms;
  if (!readSensor(tempC, humPct, pressHpa, gasKOhms)) {
    Serial.println("Failed reading sensor");
    delay(3000);
    return;
  }

  float deltaHumPct = humPct - baselineHum;
  float gasDropPct = 0.0;
  if (baselineGas > 0.0) {
    gasDropPct = ((baselineGas - gasKOhms) / baselineGas) * 100.0;
  }

  addToHistory(gasDropPct, deltaHumPct);

  float gasDropPctSmoothed = averageArray(gasDropHist, SMOOTH_N);
  float deltaHumPctSmoothed = averageArray(humDeltaHist, SMOOTH_N);

  String rawState = classifyOrangeState(gasDropPctSmoothed, deltaHumPctSmoothed);
  String finalState = stabilizeState(rawState);
  String finalPrice = priceForStatus(finalState);

  Serial.print("T="); Serial.print(tempC, 2);
  Serial.print(" H="); Serial.print(humPct, 2);
  Serial.print(" Gas="); Serial.print(gasKOhms, 2);
  Serial.print(" | dHum="); Serial.print(deltaHumPctSmoothed, 2);
  Serial.print(" gasDrop="); Serial.print(gasDropPctSmoothed, 2);
  Serial.print(" | raw="); Serial.print(rawState);
  Serial.print(" stable="); Serial.println(finalState);

  sendTagUpdate(
    productName,
    finalState,
    finalPrice,
    String(tempC, 1) + "C",
    String(humPct, 1),
    String(gasKOhms, 1) + "K"
  );

  delay(5000);
}