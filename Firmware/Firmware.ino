#include <Wire.h>
#include "Wire.h"
#include "MPU6050_bdt.h"

MPU6050 mpu;

void setup() {
  Serial.begin(115200);


  Serial.println("Initialize MPU6050");
  while (!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G, MPU6050_NORMAL, WIRE_400kHz))
  {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  
  // If you want, you can set accelerometer offsets
  // mpu.setAccelOffsetX();
  // mpu.setAccelOffsetY();
  // mpu.setAccelOffsetZ();

  //mpu.setDHPFMode(MPU6050_DHPF_HOLD);
  //mpu.setDHPFMode(MPU6050_DHPF_0_63HZ);
  //mpu.setDHPFMode(MPU6050_DHPF_1_25HZ);
  //mpu.setDHPFMode(MPU6050_DHPF_2_5HZ);
  //mpu.setDHPFMode(MPU6050_DHPF_5HZ);
  //mpu.setDHPFMode(MPU6050_DHPF_RESET);

  //mpu.setDLPFMode(MPU6050_DLPF_6);
  //mpu.setDLPFMode(MPU6050_DLPF_5);
  //mpu.setDLPFMode(MPU6050_DLPF_4);
  //mpu.setDLPFMode(MPU6050_DLPF_3);
  //mpu.setDLPFMode(MPU6050_DLPF_2);
  //mpu.setDLPFMode(MPU6050_DLPF_1);
  mpu.setDLPFMode(MPU6050_DLPF_0);
}

int c = 0;
void loop() {

  c = 0;
  if (Serial.available()) {
    while (c == 0) {

      long unsigned int t = millis();
      mpu.readNormalizeGyro();
      mpu.readScaledAccel();

      Serial.print(mpu.sax); Serial.print(",");
      Serial.print(mpu.say); Serial.print(",");
      Serial.print(mpu.saz); Serial.print(",");


      Serial.print(mpu.ngx); Serial.print(",");
      Serial.print(mpu.ngy); Serial.print(",");
      Serial.print(mpu.ngz); Serial.print(",");

      Serial.print(t); Serial.print(",");
      Serial.print(0);
      Serial.println();

      byte s = Serial.read();
      if (Serial.available()) {
        Serial.read();
        c = 1;
      }
    }
  }
}
