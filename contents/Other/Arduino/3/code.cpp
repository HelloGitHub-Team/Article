#include <Arduino.h>
#include "DHT.h"

// DHT11 DATA 引脚连接的数字引脚编号
#define DHT_DATA_PIN 8
#define UPDATE_INTERVAL 10*1000
DHT dht11(DHT_DATA_PIN, DHT11, 1);
float t, h;
unsigned long start;

String get_data()
{
  char c[100];

  h = dht11.readHumidity();
  t = dht11.readTemperature();
    // sprintf 在 Arduino 中无法转换浮点数
  dtostrf(t, 2, 2, c); 
  dtostrf(h, 2, 2, c+5);
  return String(c);
}

boolean at_exec(char *data, char *keyword, unsigned long time_out)
{
  Serial.println(data);
  Serial.flush();
  delay(100); // 等待响应
  unsigned long start = millis();

  while (Serial.available() < strlen(keyword))
  {
    if (millis() - start > time_out)
      return false;
  }
  if (Serial.find(keyword))
    return true;
  else
    return false;

  while (Serial.available())
    Serial.read(); //清空串口缓存
}
void setup()
{
  Serial.begin(115200);
  dht11.begin();
  pinMode(LED_BUILTIN, OUTPUT);
  while (!at_exec("AT+RST", "OK", 1000));
  while (!at_exec("AT+CWMODE=1", "OK", 1000));
  while (!at_exec("AT+CWQAP", "OK", 1000));
  while (!at_exec("AT+CWJAP=\"HelloGithub\",\"PassWord\"", "WIFI CONNECTED", 2000));
  while (!at_exec("AT+CIPSTART=\"TCP\",\"183.230.40.40\",1811", "CONNECT", 1000));
  while (!at_exec("AT+CIPMODE=1", "OK", 500));
  while (!at_exec("AT+CIPSEND", "OK", 500));
  Serial.println("*产品ID#ILoveHelloGitHub#HG*");
  start = millis();
}

// 根据从串口收到的 字符串 执行相应的指令
bool command_parse(String command){
  command.trim();
  command.toLowerCase();
  if (command == "open")
  {
    digitalWrite(LED_BUILTIN, HIGH);
  }else if (command == "close")
  {
    digitalWrite(LED_BUILTIN, LOW);
  }
  else if (command == "received");
}

void loop()
{
    // 定时上报消息
  if (millis() - start > UPDATE_INTERVAL)
  {
    String data = get_data();
    Serial.println(data);
    start = millis();
  }
    // 收到消息进行解析
  if (Serial.available()){
    delay(10); // 等待全部数据接收完毕
    command_parse(Serial.readString());
    while (Serial.available())
      Serial.read(); //清空串口缓存
  }
  
}