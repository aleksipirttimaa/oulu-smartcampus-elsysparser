#!/usr/bin/python

from configparser import NoOptionError
import os
import paho.mqtt.client as mqtt
import settings


class Mqtt():
    def __init__(self):
        self.publish_topic = settings.config.get('MqttBroker', 'out_topic')
        self.monitor_topic = settings.config.get('MqttBroker', 'monitor_topic') or ""

        # please use unique identifier for client
        # the previous client with the same name will be kicked out
        client_id = settings.config.get('MqttBroker', 'client_id')
        self.client = mqtt.Client(client_id, clean_session=True)

        # credentials also from config
        broker_user = settings.config.get('MqttBroker', 'user')
        broker_pass = settings.config.get('MqttBroker', 'passwd')
        certificate_path = ""
        try:
            certificate_path = settings.config.get('MqttBroker', 'certificate_path')
        except NoOptionError as err:
            settings.logger.warning("No tls cert set, tls won't be used.")

        self.parsed_topic = settings.config.get('MqttBroker', 'out_topic')

        self.client.username_pw_set(broker_user, password=broker_pass)

        # certificate path required for tls operation, but optional
        if certificate_path:
            # use the certificate if the file exists
            if os.path.isfile(certificate_path):
                self.client.tls_set(certificate_path)  # needed for tls encryption
            else:
                settings.logger.critical("No certificate could be found.")
        
        self.message_handler = self.none_callback

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect


    def none_callback(self, *_):
        raise NotImplementedError("Uninitialised callback invoked")


    def on_connect(self, client, userdata, _flags, rc):
        try:
            subscribe_topic = settings.config.get('MqttBroker', 'in_topic')
            if rc == 0:
                settings.logger.info("Connected to the broker with code: " + str(rc))
                client.subscribe(subscribe_topic)  # QoS-0 by default
            else:
                settings.logger.critical("Error occured while connecting to the broker. Error code: " + str(rc))
        except Exception as err: # paho-mqtt.client loop inhibits all exceptions, I'm trying my best
            settings.logger.critical("Connection handler encountered an unexpected error: " + str(err))
            quit()


    def on_message(self, _client, _userdata, mesg):
        try:
            self.message_handler(mesg.payload) # not to be confused w/ elsys payload
        except Exception as err: # paho-mqtt.client lo...
            settings.logger.critical("Message handler encountered an unexpected error: " + str(err))
            quit()


    def on_disconnect(_self, _client, _userdata, _rc):
        settings.logger.critical("Client disconnected.")


    def connect(self):
        broker_host = settings.config.get('MqttBroker', 'host')
        broker_port = settings.config.get('MqttBroker', 'port')

        settings.logger.info("Connecting to broker.")
        rc = self.client.connect(broker_host, int(broker_port), keepalive=60)

        if rc == 0:
            settings.logger.debug("MQTT client loop started")
            self.client.loop_forever()
        else:
            print("Connection to the broker failed. Return code: " + str(rc))
            settings.logger.critical("Connection to the broker failed. Return code: " + str(rc))


    def publish(self, message, topic=""):
        if topic == "": # publish as result if no other topic specified
            topic = self.parsed_topic
        msg_info = self.client.publish(topic, payload=message) # QoS-0 by default
        
    def publish_monitor(self, status):
        if self.monitor_topic != "":
            self.publish(str(status), topic=self.monitor_topic)
