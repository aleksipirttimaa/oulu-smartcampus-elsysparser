# elsysparser

Elsysparser is an MQTT client that implements elsys-compatible sensor data parsing. It listens to a configurable topic that represents the payload from the LoRA gateway and after extracting the values, publishes them under a different topic as JSON.

Based on earlier work available here: https://github.com/xmyzincx/Elsys_MQTT_Client

## This repository

- `server.conf.example`: an example configuration, you'll need to have a look at this before running
- `requirements.txt`: pardon simple dependency management, the only dependency is the paho-mqtt library.

### `src/`:

- `utils.py`: implements parsing logic
- `monitoring.py`: monitoring object
- `mqtt.py`: mqtt protocol object
- `settings.py`: configuration available to other modules


## Running

1. ```pip install -r requirements.txt```
2. ```cp server.conf.example server.conf```
3. If you're using TLS add your CA to `certificates/`
> remember to point to the certificate in server.conf
4. ```python main.py```

You can build this as a container with:

```docker build -t elsysparser:latest```


# Types

You can find the parser logic in `src/utils.py`.

What is the incoming payload from the LoRA GW like?
```json
{
  "ack": false,
  "adr": false,
  "appeui": "43-57-43-5f-44-45-4d-4f",
  "chan": 5,
  "cls": 0,
  "codr": "4/5",
  "datr": "SF7BW125",
  "deveui": "a8-17-58-ff-fe-03-10-12",
  "freq": 868.3,
  "lsnr": 9.8,
  "mhdr": "40f600000280a785",
  "modu": "LORA",
  "opts": "",
  "port": 7,
  "rfch": 0,
  "rssi": -85,
  "seqn": 34215,
  "size": 16,
  "time": "2020-06-05T16:11:37.171964Z",
  "tmst": 2919482228,
  "fcnt": 22,
  "gweui": "00-80-00-00-a0-00-48-b7",
  "stat": 1,
  "payload": [
    1,
    0,
    220,
    2,
    29,
    4,
    1,
    236,
    5,
    0,
    6,
    1,
    228,
    7,
    14,
    88
  ],
  "eui": "a8-17-58-ff-fe-03-10-12",
  "_msgid": "54d03042.ab2fd"
}
```

What is the output like?
```json
{
  "_msgid": "54d03042.ab2fd",
  "deveui": "a8-17-58-ff-fe-03-10-12",
  "timestamp_node": 1590648980,
  "temperature": 22,
  "humidity": 29,
  "light": 492,
  "pir": 0,
  "co2": 484,
  "battery": 3.672,
  "timestamp_parser": 1590649973
}
```

# License

Copyright 2020 aleksipirttimaa provided under the MIT license.
