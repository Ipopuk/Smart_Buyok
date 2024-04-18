// подключите один мотор к клемме: M1+ и M1-
// а второй к клемме: M2+ и M2-
// Motor shield использует четыре контакта 4, 5, 6, 7 для управления моторами 
// 4 и 7 — для направления, 5 и 6 — для скорости
 
#include <SoftwareSerial.h>
#include <Servo.h>
#include "Parser.h"

#define HC_TRIG 10
#define HC_ECHO 11

#define SPEED_1      5 
#define DIR_1        4
 
#define SPEED_2      6
#define DIR_2        7

#include "AsyncStream.h"  // асинхронное чтение сериал
AsyncStream<50> serial(&Serial, ';');   // указываем обработчик и стоп символ

Servo myservo;

int id = 1;
int last_min = 0;
void setup() {
  Serial.begin(9600);

  pinMode(HC_TRIG, OUTPUT); // trig выход
  pinMode(HC_ECHO, INPUT);  // echo вход ultrasonic
  // // настраиваем выводы платы 4, 5, 6, 7 на вывод сигналов 
  for (int i = 4; i < 8; i++) {     
    pinMode(i, OUTPUT);
  }
    myservo.attach(9);

} 
 
void loop() {
  Serial.println("-");
  parsing();
}

//   int timeMins = (millis() / 1000ul % 3600ul) / 60ul;
//   if ((timeMins - last_min) >= 15){
//     last_min = (millis() / 1000ul % 3600ul) / 60ul;

//     float depth = getDist();  
//     float mpu = get_degree();
//     char ll[] = "55.637656, 37.493700"
//     String OUTPUT[] += id + ll + (String)depth + (String)mpu; // СБОР ДАННЫХ
//}




void parsing() {
 if (serial.available()) {
    Parser data(serial.buf, ',');  // отдаём парсеру
    int ints[10];           // массив для численных данных
    data.parseInts(ints);   // парсим в него

    switch (ints[0]) {
      case 0:
        digitalWrite(DIR_1, LOW); // grid
        analogWrite(SPEED_1, 255);
        delay(1000 * ints[1] / 100); // TIME - время для полного сворачивания сетки, X.X передаваемый коэф.
        analogWrite(SPEED_1, 0);
        break;
      case 1: 
        digitalWrite(DIR_2, LOW);
        analogWrite(SPEED_2, 255);
        break;
      case 2:
        analogWrite(SPEED_2, 0);
        break;
      case 3:
         myservo.write(ints[1]);
        break;
    }
  }
}
// float getDist() {
//   // импульс 10 мкс
//   digitalWrite(HC_TRIG, HIGH);
//   delayMicroseconds(10);
//   digitalWrite(HC_TRIG, LOW);
//   // измеряем время ответного импульса
//   uint32_t us = pulseIn(HC_ECHO, HIGH);
//   // считаем расстояние и возвращаем
//   return (us / 58.2);
//}

// float get_degree(){
//   // переменные для расчёта (ypr можно вынести в глобал)
//       Quaternion q;
//       VectorFloat gravity;
//       float ypr[3];

//       // расчёты
//       mpu.dmpGetQuaternion(&q, fifoBuffer);
//       mpu.dmpGetGravity(&gravity, &q);
//       mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);

//       // выводим результат в радианах (-3.14, 3.14)
//       float returnn = degrees(ypr[0]); // вокруг оси Z
//       // для градусов можно использовать degrees()


//       return (returnn);
//     }