#include <Adafruit_MCP4725.h>
Adafruit_MCP4725 dac;

void setup() {
  
  Serial.begin(9600);
  dac.begin(0x60); // The I2C Address: Run the I2C Scanner if you're not sure 

  
  delay(1000);
  dac.setVoltage(4095, false);
  delay(1500);
  dac.setVoltage(0, false);
  
  pinMode(8, INPUT);
  pinMode(9, INPUT);
  //digitalWrite(8, LOW);
   
}

//int throttleMax = 4096;
int throttleCurrent = 0;

void loop() {
  if (Serial.available())
  {
    /*
    char turn = Serial.read();
    if(turn == 'f'){
      pinMode(8, OUTPUT);
      Serial.println("done");
    }else{
      pinMode(8, INPUT);
    }
    */
    
    // throttle
    
    int ch = Serial.parseInt();
    if(ch > 10 || ch == 0){
      throttleCurrent = (ch * 4000)/100;
      if(throttleCurrent == 4000){
        throttleCurrent = 4095;
      }
      Serial.println(throttleCurrent);
      dac.setVoltage(throttleCurrent, false);
    }else{
      if(ch == 1){
        pinMode(8, OUTPUT);
        Serial.println("left");
      }else if(ch == 2){
        digitalWrite(8, LOW);
        pinMode(8, INPUT);
        Serial.println("stable");
      }if(ch == 4){
        pinMode(9, OUTPUT);
        Serial.println("back");
      }else if(ch == 5){
        pinMode(9, INPUT);
        Serial.println("stable");
      }
    }
    
    

    
    //measure current at A0
    //test
    /*
    delay(1000); 
    int sensorValue = analogRead(A0);
    float voltage= sensorValue * (3.3 / 1023.0);
    Serial.println(voltage);
    */
    
  }

   
  
  
  


}
