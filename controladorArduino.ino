
#include <SoftwareSerial.h>


#define E1 10  // Enable Pin for motor 1
#define I1 8     // Control pin 1 for motor 1
#define I2 9     // Control pin 2 for motor 1

#define E2 11  // Enable Pin for motor 1
#define I3 12    // Control pin 1 for motor 1
#define I4 13     // Control pin 2 for motor 1

double t0, countE1, countE2, v1, v2, currentE1, currentE2;
double en1, en2;
double valorLuz;

double kp[2] = {.025,.005};
double ki[2] = {.015,.015};
double kd[2] = {.1,.1};

unsigned long prevTime[2];
double lastError[2];
double outM1, outM2, setPoint1, setPoint2;
double I[2];


//conf del xbee
SoftwareSerial xbee = SoftwareSerial(65,64);
char senal = '7';

void setup() {
    xbee.begin(9600);
 
    for (int i =8 ; i<14 ; i++)                     // Inicializamos los pines
      pinMode( i, OUTPUT);
   
    pinMode(A2, INPUT);
    pinMode(A1, INPUT);
    t0 =0;
    setPoint1 = 0;
    setPoint2 = 0;
    en1= digitalRead(A2);
    I[0] = 0;
    I[1] = 0;
    
 
    analogWrite(E2, 0);     // Activamos Motor1
    digitalWrite(I3, HIGH);     // Arrancamos
    digitalWrite(I4, LOW);
    
    analogWrite(E1, 0);     // Activamos Motor2
    digitalWrite(I2, HIGH);// Arrancamos
    digitalWrite(I1, LOW);  

    
}


void loop() {

  if(t0 == 0){
    t0 = millis();
    countE1 = 0;
    countE2 = 0;
  }
  
  currentE1 = digitalRead(A2);
  double xr = (en1||currentE1)&&(!en1 || !currentE1);
  countE1 = countE1 + xr;
  en1 = currentE1;

  currentE2 = digitalRead(A1);
  xr = (en2||currentE2)&&(!en2 || !currentE2);
  countE2 = countE2 + xr;
  en2 = currentE2;
  
 
 double currentTime = millis();
  if (currentTime - t0 >= 1000){
    v1 = ((countE1/18)*1000)/(currentTime-t0);
    v2 = ((countE2/18)*1000)/(currentTime-t0);
    t0 = 0;
    
    outM1 = PID(v1, 0, setPoint1);
    outM2 = PID(v2, 1, setPoint2);
   
     double outPWM1 = min(abs(outM1), 255);
     double outPWM2 = min(abs(outM2), 255);
     analogWrite(E2, outPWM1); 
     analogWrite(E1, outPWM2);


 }


 
   //Serial.println(v1);
 
  
   
     
  // Serial.println(outM1);  

  //Recibe la senal del xbee 
  if(xbee.available()){
    senal = xbee.read();

    switch(senal) {
    case '0' :  
      setPoint1 = 5;
      setPoint2 = 5;
      break;
    case '1' : 
      setPoint1 = 5;
      setPoint2 = 0;
      break;
    case '2':
      setPoint1 =  0;
      setPoint2 = 5;
      break;
     case '3':
      setPoint1 = 0;
      setPoint2 = 0;
      break;
  }

   
  }

 


}

void lineaRecta(){
   //Serial.println("Entro");
   outM1 = PID(v1, 0, 5);
   outM2 = PID(v2, 1, 5);
   
   double outPWM1 = min(abs(outM1), 255);
   double outPWM2 = min(abs(outM2), 255);
   analogWrite(E2, outPWM1); 
   analogWrite(E1, outPWM2); 
   
}

void izquierda(){
   Serial.println("Entro");
   outM1 = PID(v1, 0, 6);
   outM2 = PID(v2, 1, 1);
   
   double outPWM1 = min(abs(outM1), 255);
   double outPWM2 = min(abs(outM2), 255);
   analogWrite(E2, outPWM1); 
   analogWrite(E1, outPWM2); 
   
}


double PID(double e , int m,  double setPoint){
    double currentTime = millis();
    double eTime = (double)(currentTime - prevTime[m]);
    double error = setPoint - e;
    
    I[m] += error * eTime;
    double d = (error-lastError[m])/eTime;
    
    double pid = kp[m]*error + kd[m]*d + ki[m]*I[m];
    
    lastError[m] = error;
    prevTime[m] = currentTime;
    
    return pid;
}
