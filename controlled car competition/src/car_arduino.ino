
//void setup() {
//  // initialize digital pin LED_BUILTIN as an output.
//  pinMode(13, OUTPUT);
//}
//
//// the loop function runs over and over again forever
//void loop() {
//  digitalWrite(13, HIGH);   // turn the LED on (HIGH is the voltage level)
//  delay(100);                       // wait for a second
//  digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW
//  delay(100);                       // wait for a second
//}

#include <SoftwareSerial.h>
SoftwareSerial BT(10, 11); //HC06-TX Pin 10, HC06-RX to Arduino Pin 11
int LED = 13; //Use whatever pins you want
char t;


void setup() {
  BT.begin(9600); //Baudrate 9600 , Choose your own baudrate
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
}

void loop() {
  if (BT.available()) {
    t = BT.read();
    BT.println(t);
    Serial.println(t);
  }

  if (t == '1') {          //move forward(all motors rotate in forward direction)
    digitalWrite(4, HIGH);
    digitalWrite(6, HIGH);
  }

  else if (t == '2') {    //move reverse (all motors rotate in reverse direction)
    digitalWrite(5, HIGH);
    digitalWrite(7, HIGH);
  }

  else if (t == '3') {    //turn right (left side motors rotate in forward direction, right side motors doesn't rotate)
    digitalWrite(6, HIGH);
  }

  else if (t == '4') {    //turn left (right side motors rotate in forward direction, left side motors doesn't rotate)
    digitalWrite(4, HIGH);
  }



  else if (t == '0') {    //STOP (all motors stop)
    digitalWrite(4, LOW);
    digitalWrite(5, LOW);
    digitalWrite(6, LOW);
    digitalWrite(7, LOW);
  }
  delay(100);

  //  if(BT.available() > 0) //When HC06 receive something
  //  {
  //    char receive = BT.read(); //Read from Serial Communication
  //
  //    if(receive == '1') //If received data is 1, turn on the LED and send back the sensor data
  //    {
  //      BT.println("fuck");
  //      Serial.println("1");
  //      digitalWrite(13, HIGH);
  //      digitalWrite(6,HIGH);
  //      digitalWrite(7,LOW);
  //
  //
  //    }
  //    if(receive == '0')
  //    {
  //      BT.println("shit");
  //      Serial.println("0");
  //      digitalWrite(13, LOW);
  //      digitalWrite(6,LOW);
  //      digitalWrite(7,LOW);
  //
  //
  //    }
  //  }
}