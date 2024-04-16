#include <Wire.h>
#include "ArduinoJson.h"
#include <ESP8266WiFi.h>

#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"

#include "SPI.h"

#include "Adafruit_GFX.h"
#include "Adafruit_ILI9341.h"

MPU6050 mpu;
int16_t ax, ay, az;
int16_t gx, gy, gz;
static uint32_t tmr;
uint8_t fifoBuffer[45];


int start = 0;
bool JSONend = true;

#define TFT_CS       15 
#define TFT_DC       2
#define TFT_RST      0

Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC, TFT_RST); // Use hardware SPI

#define SSID "eminA"
#define PASS "10101010"
// #define SSID "IT-Poligon"
// #define PASS "wifipassw0rd"
// #define SSID "Plushka"
// #define PASS "14203237"
WiFiServer server(80);


unsigned long long last_time = 0;
unsigned long long time_ = 0;
unsigned long long delta = 0;
float meanings[600][2];
int indexxx = 0;
String JSONMessage = "{\"ParticipantID\": 2, \"Start\": 10,  \"Finish\": 10,  \"Telemetry\": ["; // ID
String response = "responce";
unsigned long long starttime = 0;
bool start_time = true;


void setup(void) {

   Wire.begin();
  //Wire.setClock(1000000UL);   // разгоняем шину на максимум

  // инициализация DMP
  mpu.initialize();
  mpu.dmpInitialize();
  mpu.setDMPEnabled(true);


  // put your setup code here, to run once:
  // IPAddress ip(192,168,1,31);
  // IPAddress gateway(192,168,1,1);
  // IPAddress subnet(255, 255, 255, 0);
  // WiFi.config(ip, gateway, subnet);
  WiFi.begin(SSID, PASS);
  Serial.begin(115200);
  while(WiFi.status() !=  WL_CONNECTED){
    delay(500);
    Serial.println("Connecting...");
  }
  Serial.println("-----------------------------------");
  Serial.println(WiFi.localIP());
  server.begin();
  
  tft.begin();

  // read diagnostics (optional but can help debug problems)
  uint8_t x = tft.readcommand8(ILI9341_RDMODE);
  Serial.print("Display Power Mode: 0x"); Serial.println(x, HEX);
  x = tft.readcommand8(ILI9341_RDMADCTL);
  Serial.print("MADCTL Mode: 0x"); Serial.println(x, HEX);
  x = tft.readcommand8(ILI9341_RDPIXFMT);
  Serial.print("Pixel Format: 0x"); Serial.println(x, HEX);
  x = tft.readcommand8(ILI9341_RDIMGFMT);
  Serial.print("Image Format: 0x"); Serial.println(x, HEX);
  x = tft.readcommand8(ILI9341_RDSELFDIAG);
  Serial.print("Self Diagnostic: 0x"); Serial.println(x, HEX); 
  Serial.println(testText());
  delay(3000);


}

void loop() {

   WiFiClient client = server.available();
    if(client){
      String request = client.readString();
      //Serial.println(010);
      //Serial.println(request);
      Serial.println("Client!!!");
      // = 
      //   "HTTP/1.1 200 OK\r\n"
      //   "Content-Type: text/html\r\n\r\n"
      //   "TEST";
      if(request.indexOf("init") != -1){
        response = 
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n\r\n"
        "INIT_SUCCESS";
      }
      else if(request.indexOf("start") != -1){ // Принимать ID
        start = 1;
        response = 
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n\r\n"
        "START_SUCCESS";
        Serial.println(response);
        client.print(response); 
      }
      else if (request.indexOf("get_data") != -1){
        start = 0;
        if (JSONend == true){
        //JSONMessage += "[0, 0]]}";
        JSONend = false;
        }
        //Serial.println(JSONMessage);
      //   StaticJsonDocument<5000> parsed;   //Пул памяти слишком много
      //   // Десериализация документа JSON
      //   DeserializationError error = deserializeJson(parsed, JSONMessage);
      //   // Проверьте, удастся ли выполнить синтаксический анализ.
      //   if (error) {
      //     Serial.print(F("deserializeJson() failed: "));
      //     Serial.println(error.f_str());
      //     return;
      //   }
      //   else {   //Вывести если ошибок нет

      //     Serial.println("There are no errors");
      
      // }
        response = 
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n\r\n";
        response += JSONMessage;
        //Serial.println(response);
        client.print(response); 
        //client.print(JSONMessage);
    }}
    
    if (start == 1){
      if (starttime == 0 ){
        starttime = millis();
      }
      //Serial.println(111);
      time_ = millis();
      time_ = time_ - starttime;      
      delta = time_ - last_time;
      if (indexxx < 600 && (start_time == true || delta > 50)){
        last_time = time_;
        // Serial.println(JSONMessage);
        // Serial.println(start_time);
        start_time = false;
        meanings[indexxx][0] = (float)time_;
        mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
        meanings[indexxx][1] = az - gz;
        // if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) {
        //   meanings[indexxx][1] = get_degree();
        //   }

        indexxx++;
        //Serial.println(meanings[indexxx - 1][0]);
        

        //Serial.println(indexxx);
        //Serial.println("");
        
        
        
        JSONMessage += "[" + (String)meanings[indexxx - 1][0] + ", " + (String)meanings[indexxx - 1][1] + "], ";
        //Serial.print("Initial string value: ");
        //Serial.println(JSONMessage);
        }}

    }



float get_degree(){
  // переменные для расчёта (ypr можно вынести в глобал)
      Quaternion q;
      VectorFloat gravity;
      float ypr[3];

      // расчёты
      mpu.dmpGetQuaternion(&q, fifoBuffer);
      mpu.dmpGetGravity(&gravity, &q);
      mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);

      // выводим результат в радианах (-3.14, 3.14)
      float returnn = degrees(ypr[0]); // вокруг оси Z
      // для градусов можно использовать degrees()


      return (returnn);
    }

unsigned long testText() {
  tft.setRotation(1);
  tft.fillScreen(ILI9341_BLACK);
  unsigned long start = micros();
  tft.setCursor(30, 90);
  tft.setTextColor(ILI9341_GREEN);
  tft.setTextSize(2);
  tft.println("ParticipantID: 2");
  tft.setCursor(20, 120);
  tft.setTextSize(3);
  tft.println(WiFi.localIP());
  return micros() - start;
}