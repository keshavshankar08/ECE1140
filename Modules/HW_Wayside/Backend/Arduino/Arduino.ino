#include <LiquidCrystal_I2C.h> // Library for LCD

char incomingByte; 
String Data = "";
char BlockType;
char TrackFault, Maintenance;
char SwitchDirection, TrafficLight;
char Crossing;
int Writer = 0;


LiquidCrystal_I2C lcd(0x20, 16, 4); // I2C address 0x27, 16 column and 2 rows

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  LCD_setup();

  lcd.print("Getting Set up...");
  delay(1);
  LCD_setup();
  }

void loop() {

  // READ PLC PROGRAM - convert to string
  if (Serial.available() > 0) {
    // read data
    display();

/*
    while (Serial.available() > 0)
    {
      incomingByte = Serial.read(); // read byte
      digitalWrite(LED_BUILTIN, HIGH);

      lcd.print(incomingByte); 
      Data += incomingByte;
    }
*/
    // PERFORM LOGIC WITH PLC PROGRAM
    //
    //
    //
    //
    //

    Serial.write("Received Display");
    /*
    for (int i = 0; i < Data.length(); i++)
    {
      Serial.write(Data[i]);
    }
    */
    Serial.write("\n");
    }
  }

void LCD_setup(){
  lcd.init(); //initialize the lcd
  lcd.backlight(); //open the backlight 
  lcd.clear();
  Writer = 0;
  lcd.setCursor(0, Writer);
}

void display(){
  LCD_setup();
  char incoming = "";
  while (Serial.available() > 0)
    {
      incoming = Serial.read(); // read byte
      digitalWrite(LED_BUILTIN, HIGH);

      if (incoming == '.')
      {
        lcd.setCursor(0, Writer += 1);
        Data += incoming;
      }
      else
      {
      lcd.print(incoming); 
      Data += incoming;
      }
    }

}