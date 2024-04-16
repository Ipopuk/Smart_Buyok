// пины
#define HC_TRIG 12
#define HC_ECHO 11
void setup() {
  Serial.begin(9600);       // для связи
  pinMode(HC_TRIG, OUTPUT); // trig выход
  pinMode(HC_ECHO, INPUT);  // echo вход
}
void loop() {
  float dist = getDist();   // получаем расстояние
  Serial.println(dist);     // выводим
  delay(50);
}
// сделаем функцию для удобства
float getDist() {
  // импульс 10 мкс
  digitalWrite(HC_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(HC_TRIG, LOW);
  // измеряем время ответного импульса
  uint32_t us = pulseIn(HC_ECHO, HIGH);
  // считаем расстояние и возвращаем
  return (us / 58.2);
}