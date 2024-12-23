#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_MPU6050.h>
#include <math.h>

Adafruit_MPU6050 mpu;

const int flexsensor0 = A0;
const int flexsensor1 = A1;
const int flexsensor2 = A2;
const int flexsensor3 = A3;
const int flexsensor4 = A6;

int val0, val1, val2, val3, val4;

float angle_x_acc, angle_y_acc, angle_z_gyro;
float gyro_offset_z = 0.0;

const float rAD_TO_DEG = 180.0 / PI;
const float DT = 0.01;

void setup() {
  Serial.begin(9600);

  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) delay(10);
  }

  Serial.println("MPU6050 Initialized");

  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  delay(100);

  // Calibrate gyroscope offset for Z-axis
  for (int i = 0; i < 100; ++i) {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    gyro_offset_z += g.gyro.z;
    delay(10);
  }
  gyro_offset_z /= 100.0;
}

void loop() {
  // Read flex sensor values
  val0 = analogRead(flexsensor0);
  val1 = analogRead(flexsensor1);
  val2 = analogRead(flexsensor2);
  val3 = analogRead(flexsensor3);
  val4 = analogRead(flexsensor4);

  // Get MPU6050 data
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Calculate angles from accelerometer
  angle_x_acc = atan2(a.acceleration.y, sqrt(a.acceleration.x * a.acceleration.x + a.acceleration.z * a.acceleration.z)) * rAD_TO_DEG;
  angle_y_acc = atan2(-a.acceleration.x, sqrt(a.acceleration.y * a.acceleration.y + a.acceleration.z * a.acceleration.z)) * rAD_TO_DEG;

  // Normalize accelerometer angles
  angle_x_acc = fmod(angle_x_acc, 360.0);
  if (angle_x_acc < 0) angle_x_acc += 360.0;

  angle_y_acc = fmod(angle_y_acc, 360.0);
  if (angle_y_acc < 0) angle_y_acc += 360.0;

  // Calculate gyroscope angle for Z-axis
  angle_z_gyro = (g.gyro.z - gyro_offset_z) * DT;

  // Normalize gyroscope angle
  angle_z_gyro = fmod(angle_z_gyro, 360.0);
  if (angle_z_gyro < 0) angle_z_gyro += 360.0;

  // Print data in CSV format
  Serial.print(val0);
  Serial.print(",");
  Serial.print(val1);
  Serial.print(",");
  Serial.print(val2);
  Serial.print(",");
  Serial.print(val3);
  Serial.print(",");
  Serial.print(val4);
  Serial.print(",");
  Serial.print(angle_x_acc);
  Serial.print(",");
  Serial.print(angle_y_acc);
  Serial.print(",");
  Serial.print(angle_z_gyro);
  Serial.println(",A");

  delay(100);
}
