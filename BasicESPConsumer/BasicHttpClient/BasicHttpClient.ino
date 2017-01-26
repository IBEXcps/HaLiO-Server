#include <Arduino.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>

ESP8266WiFiMulti WiFiMulti;

String host = "ibexcps.com";
int port = 8001;

char user[] = "admin";
char password[] = "paodebatata";

void setup()
{
    Serial.begin(115200);
    WiFiMulti.addAP("Pao de Batata", "bananaamassadinha");
}


void upload_data(float value, String node)
{
    StaticJsonBuffer<300> jsonBuffer;
    JsonObject& root = jsonBuffer.createObject();
    root["node"] = node;
    root["value"] = value;
    char payload[128] = {0};
    root.printTo(payload, sizeof(payload));

    HTTPClient http;
    http.setAuthorization(user, password);

    http.begin(host,port, "/data/"); //HTTP
    http.addHeader("Content-Type", "application/json");
    int httpCode = http.POST(payload);

    if(httpCode > 0)
    {
        if(httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_CREATED)
        {
            String payload = http.getString();
            JsonObject& root = jsonBuffer.parseObject(payload);
            if (!root.success()) {
                Serial.println("parseObject() failed");
                return;
            }
            const char* node = root["node"];
            Serial.println(node);
        }
    }
    else
    {
        Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
}

void read_relay(String nodeid)
{

    HTTPClient http;
    http.setAuthorization(user, password);

    http.begin(host,port, "/nodes/"+nodeid+"/"); //HTTP
    int httpCode = http.GET();

    if(httpCode > 0)
    {
        if(httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_CREATED)
        {
            String payload = http.getString();
            StaticJsonBuffer<400> jsonBuffer;
            JsonObject& root = jsonBuffer.parseObject(payload);

            if (!root.success()) {
                Serial.println("parseObject() failed");
                return;
            }

            const char* node = root["relayState"];
            Serial.println(node);
        }
    }
    else
    {
        Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
}

void loop()
{
    // wait for WiFi connection
    if((WiFiMulti.run() == WL_CONNECTED))
    {
        upload_data(13.3, String("http://") +host+ ":" + port + "/nodes/1/"); //~50ms
        read_relay("1"); // ~ 25ms

    }
    delay(10000);
}

