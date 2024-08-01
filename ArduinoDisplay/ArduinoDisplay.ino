//run this code on the arduino in order to listen to

#include "Wire.h" 
#include "LiquidCrystal_I2C.h" 


LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 16, 2); 
String currLine;

void setup() {
  // Initiate the LCD:
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
}

void loop() {
  //start listening to the to the serial monitor and wait for new input
  currLine = Serial.readString();
  int SepSpot = currLine.indexOf('-');
  String title = currLine.substring(0,SepSpot);
  String artist = currLine.substring(SepSpot + 1,currLine.length());
  lcd.setCursor(0, 0); 
  lcd.print(title); 
  lcd.setCursor(0, 1); 
  lcd.print(artist);
}