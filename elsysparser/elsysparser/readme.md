# Mqtt client
The client saves the messages from a mqtt broker to a mysql-database.
Based on https://github.com/xmyzincx/Elsys_MQTT_Client

## Folder structure
settings.py: global variables available to other modules
utils.py: logic for parsing an incoming payload
mqtt.py: mqtt-client callbacks and init functions
db.py: context manager to init and close db-connection

## Instructions to run

1. ```pip install -r requirements.txt```
2. Add server.conf-file. An example of the format can be found below.
3. Add a certificate (if needed) and a path to a certificate if using tsl. Instructions here: https://www.cloudmqtt.com/docs/faq.html#TLS_SSL
4. ```python main.py```


```
[Database]
host: localhost
user: user
passwd: password
port: 3306
database: db_name
table: table_name

[MqttBroker]
host: host
port: 24551
user: username
passwd: password
topic: example/subexample
certificate_path: path/to/certificate/certf.crt

```