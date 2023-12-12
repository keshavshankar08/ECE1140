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

      // PLC Program
    else if (incoming == 'X')
    {
      Data = "";
      char curr_device = '0';
      char set_device_stage = '0';
      while (Serial.available() > 0)
      {
              incoming = Serial.read(); // read byte
              Data += incoming;
      }
      if (Data == "SW")
      {
        curr_device = '1'; // 1 corresponds to SW 
        set_device_stage = '1';
      }
      else if (Data == "CR")
      {
        curr_device = '2'; // 2 corresponds to CR
        set_device_stage = '1';
      }
      //TRANSFER DATA BACK
      String transfer = "";
      transfer[0] = curr_device;
      transfer[1] = set_device_stage;
      transfer[2] = '\0';
      Serial.println(transfer);
    }

    // corresponds to token 0
    else if (incoming == 'Y')
    {
      while (Serial.available() > 0)
      {
              incoming = Serial.read(); // read byte
              Data += incoming;
      }
      if (Data == "READ")
      {
        char transfer = "R";
        Serial.println(transfer);
      }
      else if (Data == "COND")
      {
        char transfer = "C";
        Serial.println(transfer);
      }
      else if (Data == "OPP")
      {
        char transfer = "O";
        Serial.println(transfer);
      }
      
    }
    else if (incoming == 'Z')
    {
      while (Serial.available() > 0)
      {
              incoming = Serial.read(); // read byte
              Data += incoming;
      } 
      if (Data == "NOT")
        Serial.println("N");
      else if (Data == "NC")
        Serial.println("C");
      else if (Data == "SV")
        Serial.println("S");
      else if (Data == "AND")
        Serial.println("A");
    }

  


    /*Serial.write("Received: ");
    for (int i = 0; i < Data.length(); i++)
    {
      Serial.write(Data[i]);
    }
    Serial.write("\n");
    */
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