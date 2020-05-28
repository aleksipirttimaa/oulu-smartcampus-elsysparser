# elsysparser

Elsysparser is an MQTT client that implements elsys-compatible sensor data parsing. It listens to a configurable topic that represents the payload from the LoRA gateway and after extracting the values, publishes them under a different topic as JSON.

## This repository

`server.conf.example`: an example configuration, you'll need to have a look at this before running.
`requirements.txt`: pardon simple dependency management, the only dependency is the paho-mqtt library.

### `src/`:

`utils.py`: implements parsing logic
`monitoring.py`: monitoring object
`mqtt.py`: mqtt-client callbacks and init functions
`settings.py`: configuration available to other modules


## Running

1. ```pip install -r requirements.txt```
2. ```cp server.conf.example server.conf```
3. If you're using TLS add your CA to `certificates/`
  - remember to point to the certificate in server.conf
4. ```python main.py```

You can build this as a container with:

```docker build -t elsysparser:latest```
