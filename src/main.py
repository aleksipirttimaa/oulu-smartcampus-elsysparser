#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import signal

# user modules
from utils import parse_elsys_message, ElsysParserError
from monitoring import MonLog
import mqtt
import settings


MQTT_CLIENT = mqtt.Mqtt()
MON_LOG = MonLog()
LAST_MONITORING_MESSAGE = 0


def shutdown():
    '''
    Function to shut_down the process gracefully.
    '''

    MQTT_CLIENT.client.loop_stop()
    settings.logger.debug("MQTT client loop stopped.")
    settings.logger.info("Client disconnecting.")
    MQTT_CLIENT.client.disconnect()
    


def terminate_signal_handler(_signal, _frame):
    '''
    Hander for TERM and INT signals.
    '''
    settings.logger.critical("Got termination signal from system.")
    shutdown()


def handle_message(message):
    '''
    Callback called by Mqtt for when theres a message.
    '''
    global MON_LOG
    global LAST_MONITORING_MESSAGE
    try:
        parsed = parse_elsys_message(message)
    except ElsysParserError as err: 
        # parser couldn't do its thing, likely malformed payload
        settings.logger.warning(str(err))
        settings.logger.debug("Failed message: " + message)
        MON_LOG.n_fail += 1
    else:
        settings.logger.debug("Parsed message successfully.")
        MQTT_CLIENT.publish(parsed)
        MON_LOG.n_success += 1
        if LAST_MONITORING_MESSAGE + 10 < time.time():
            LAST_MONITORING_MESSAGE = time.time()
            MQTT_CLIENT.publish_monitor(MON_LOG)


if __name__ == '__main__':
    # setting handler for terminate and interrupt signals
    signal.signal(signal.SIGTERM, terminate_signal_handler)
    signal.signal(signal.SIGINT, terminate_signal_handler)

    MQTT_CLIENT.message_handler = handle_message
    MQTT_CLIENT.connect()
