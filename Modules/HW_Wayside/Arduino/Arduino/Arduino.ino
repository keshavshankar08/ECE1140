#include <LiquidCrystal_I2C.h> // Library for LCD

String incomingByte ; 
bool TDEFA, TJUNC, TCROS, TSTAT;
int i = 0;
bool value;
char valueA;
String L1,L2,L3,L4;
LiquidCrystal_I2C lcd(0x20, 16, 4); // I2C address 0x27, 16 column and 2 rows

void setup() {
  Serial.begin(9600);
  //pinMode(LED_BUILTIN, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);

  
  lcd.init(); //initialize the lcd
  lcd.backlight(); //open the backlight 
  lcd.clear();
  }

void loop() {

  if (Serial.available() > 0) {
    delay(10);

    incomingByte = Serial.read(); // read byte of data
      //Serial.write("I recieved: ");
      //Serial.write(incomingByte[0]);
      //Serial.write("\n");
    if (incomingByte == "48")
    {
      value = 0;
      valueA = '0';
    }
    else if (incomingByte == "49")
    {
      value = 1;
      valueA = '1';
    }
    else
      exit(-1);
    
    if (i == 0)
    {
      TDEFA = value;
      Serial.write("\nTDEFA: ");
      Serial.write(valueA);
      lcd.setCursor(0, 0);

      if (value)
      {
        digitalWrite(7, HIGH);
        lcd.print("TDEFA: 1");
      }
      else
      {
        digitalWrite(7, LOW);
        lcd.print("TDEFA: 0");        
      }

    }

    if (i == 1)
    {
      TJUNC = value;
      Serial.write("\nTJUNC: ");
      Serial.write(valueA);
      lcd.setCursor(0, 1);
      //lcd.print("TJUNC = " + valueA);
      if (value)
      {
        digitalWrite(6, HIGH);
        lcd.print("TJUNC: 1");
      }
      else
      {
        digitalWrite(6, LOW);
        lcd.print("TJUNC: 0");
      }

    }

    if (i == 2)
    {
      TCROS = value;
      Serial.write("\nTCROS: ");
      Serial.write(valueA);
      lcd.setCursor(0, 2);
      if (value)
      {
        digitalWrite(5, HIGH);
        lcd.print("TCROS: 1");
      }
      else
      {
        digitalWrite(5, LOW);
        lcd.print("TCROS: 0");
      }
        
    }

    if (i == 3)
    {
      TSTAT = value;
      Serial.write("\nTSTAT: ");
      Serial.write(valueA);
      lcd.setCursor(0, 3);
      //lcd.print("TSTAT = " + valueA);

      if (value)
      {
        digitalWrite(4, HIGH);
        lcd.print("TSTAT: 1");
      }
      else
      {
        digitalWrite(4, LOW);
        lcd.print("TSTAT: 0");
      }
    }
    
    i++;
    if (i == 4) // reset counter to 0
      i = 0;

      //Serial.write("I recieved: ");
      //Serial.write(incomingByte[0]);
      //Serial.write("\n");
    delay(10); // delay 1 second before next reading

    }
  }
