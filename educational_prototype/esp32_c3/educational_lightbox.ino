#include <Wire.h>
#include <Adafruit_BME680.h>
#include <Adafruit_NeoPixel.h>

#define SDA_PIN 5
#define SCL_PIN 6
#define NEOPIXEL_PIN 4
#define PIXEL_COUNT 16

Adafruit_BME680 bme(&Wire);
Adafruit_NeoPixel ring(PIXEL_COUNT, NEOPIXEL_PIN, NEO_GRBW + NEO_KHZ800);

const int WARMUP_MS = 60000;
const int BASELINE_SAMPLES = 20;
const int SAMPLE_DELAY_MS = 2000;

float baselineTemp = 0.0;
float baselineHum = 0.0;
float baselineGas = 0.0;
bool baselineReady = false;

const int SMOOTH_N = 5;
float gasDropHist[SMOOTH_N] = {0};
float humDeltaHist[SMOOTH_N] = {0};
int histIdx = 0;
bool histFilled = false;

String lastRawState = "Fresh";
String stableState = "Fresh";
int sameStateCount = 0;
const int REQUIRED_CONFIRMATIONS = 3;

void fillRing(uint8_t r, uint8_t g, uint8_t b, uint8_t w) {
  for (int i = 0; i < PIXEL_COUNT; i++) {
    ring.setPixelColor(i, ring.Color(r, g, b, w));
  }
  ring.show();
}

bool readSensor(float &tempC, float &humPct, float &pressHpa, float &gasKOhms) {
  if (!bme.performReading()) return false;

  tempC = bme.temperature;
  humPct = bme.humidity;
  pressHpa = bme.pressure / 100.0;
  gasKOhms = bme.gas_resistance / 1000.0;
  return true;
}

void calibrateBaseline() {
  Serial.println("Calibrating baseline...");
  fillRing(0, 0, 0, 255); // blanco durante calibración

  float tSum = 0.0, hSum = 0.0, gSum = 0.0;
  int valid = 0;

  for (int i = 0; i < BASELINE_SAMPLES; i++) {
    float t, h, p, g;
    if (readSensor(t, h, p, g)) {
      tSum += t;
      hSum += h;
      gSum += g;
      valid++;
    }
    delay(SAMPLE_DELAY_MS);
  }

  if (valid > 0) {
    baselineTemp = tSum / valid;
    baselineHum = hSum / valid;
    baselineGas = gSum / valid;
    baselineReady = true;

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
    return "Very ripe";
  }
  if (gasDropPctSmoothed >= 10.0 || deltaHumPctSmoothed >= 6.0) {
    return "Ripe";
  }
  return "Fresh";
}

String stabilizeState(String rawState) {
  if (rawState == lastRawState) {
    sameStateCount++;
  } else {
    lastRawState = rawState;
    sameStateCount = 1;
  }

  if (sameStateCount >= REQUIRED_CONFIRMATIONS) {
    stableState = rawState;
  }

  return stableState;
}

void applyStateColor(String state) {
  if (state == "Fresh") {
    fillRing(0, 255, 0, 0);
  } else if (state == "Ripe") {
    fillRing(255, 180, 0, 0);
  } else {
    fillRing(255, 0, 0, 0);
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  ring.begin();
  ring.setBrightness(40);
  ring.show();

  Wire.begin(SDA_PIN, SCL_PIN);

  if (!bme.begin(0x77)) {
    Serial.println("Could not find BME680/BME688");
    fillRing(255, 0, 0, 255); // error
    while (1) delay(10);
  }

  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150);

  Serial.println("Warm-up...");
  fillRing(0, 0, 0, 255);
  delay(WARMUP_MS);

  calibrateBaseline();

  if (baselineReady) {
    fillRing(0, 255, 0, 0);
  }
}

void loop() {
  if (!baselineReady) {
    delay(5000);
    return;
  }

  float tempC, humPct, pressHpa, gasKOhms;
  if (!readSensor(tempC, humPct, pressHpa, gasKOhms)) {
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

  applyStateColor(finalState);

  Serial.print("T="); Serial.print(tempC, 2);
  Serial.print(" H="); Serial.print(humPct, 2);
  Serial.print(" Gas="); Serial.print(gasKOhms, 2);
  Serial.print(" | dHum="); Serial.print(deltaHumPctSmoothed, 2);
  Serial.print(" gasDrop="); Serial.print(gasDropPctSmoothed, 2);
  Serial.print(" | raw="); Serial.print(rawState);
  Serial.print(" stable="); Serial.println(finalState);

  delay(50000);
}