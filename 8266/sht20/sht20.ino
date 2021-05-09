#include <Wire.h>
 
#define SHT2x 0b1000000
#define CMD_TEMP 0b11100011
#define CMD_RH 0b11100101
void setup()
{
  
  Wire.begin(0,2);        // join i2c bus (address optional for master)
  Serial.begin(115200);  // start serial for output
}
 
void loop()
{
  Serial.print(getRH());         // print the character
  Serial.println("%");
  delay(500);
  Serial.print(getTempC());
  Serial.println("C");
  delay(1000);
}
double getRH()
{
  Wire.beginTransmission(SHT2x);
  Wire.write(CMD_RH);
  Wire.endTransmission();
   
  Serial.println("endTransmission");
   
  Wire.requestFrom(SHT2x, 0x40);    // request 6 bytes from slave device #2
  unsigned long data=0;
  for(int i=0;i<2&&Wire.available();++i)    // slave may send less than requested
  { 
    unsigned char c = Wire.read(); // receive a byte as character
    data+=(unsigned long)c<<((1-i)*8);
  }
  double RH;
  RH=125.0*(double)data/65536-6.0;
  return RH;
}
double getTempC()
{
  Wire.beginTransmission(SHT2x);
  Wire.write(CMD_TEMP);
  Wire.endTransmission();
   
  Serial.println("endTransmission");
   
  Wire.requestFrom(SHT2x, 0x40);    // request 6 bytes from slave device #2
  unsigned long data=0;
  for(int i=0;i<2&&Wire.available();++i)    // slave may send less than requested
  { 
    unsigned char c = Wire.read(); // receive a byte as character
    data+=(unsigned long)c<<((1-i)*8);
  }
  double tempC;
  tempC=175.72*(double)data/65536-46.85;
  return tempC;
}
