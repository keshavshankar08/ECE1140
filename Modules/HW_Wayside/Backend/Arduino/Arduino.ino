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

    // read display
    char incoming = Serial.read();
    if (incoming == 'D')
      display();
    else if (incoming == 'P')
    {
      while (Serial.available() > 0)
      {
        lcd.print(incoming); 
        Data += incoming;
      }

    }

    //ReadPLC();


    Serial.write("Received: ");
    for (int i = 0; i < Data.length(); i++)
    {
      Serial.write(Data[i]);
    }
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
  Data = "";
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

void ReadPLC(){
  while (Serial.available() > 0){
    Data = "";
    incomingByte = Serial.read(); // read byte
    digitalWrite(LED_BUILTIN, HIGH);

    if (incomingByte != '\t')
      Data += incomingByte;
  }

  String line = "";
  for (int i = 0; i < Data.length(); i++)
  {
    if (Data[i] != '\n')
      if (line == "SW")
        // SW information
        return;
        
      else if (line == "COND")
        // Condition info
        return;
      else if (line == "READ")
        // save information on variables
        return;
      else if (line == "CR")
        return;
      else if (line == "OPP")
        return;
      line += Data;
    if (Data[i] == '\n')
      return;


  }
  
}