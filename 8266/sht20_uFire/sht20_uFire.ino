#include <Stdio.h>
#include <String.h>
#include <Wire.h>
#include "uFire_SHT20.h"

uFire_SHT20 sht20;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Wire.pins(0,2);
   Wire.begin();        // join i2c bus (address optional for master)
   sht20.begin();

}

void loop() {
  // put your main code here, to run repeatedly:
     sht20.measure_all();
     Serial.println((String)sht20.tempC + "°C");
     Serial.println((String)sht20.RH + " %RH");
     Serial.println((String)sht20.vpd() + " kPa VPD");
    Serial.println();
    delay(1000);
}
