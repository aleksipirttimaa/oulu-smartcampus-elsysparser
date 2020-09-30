#!/usr/bin/python
# -*- coding: utf-8 -*-

import signal
import sys
import time
import traceback

# user modules
from gw_message import parse_gateway_message, GatewayMessageError
from monitoring import MonLog
import mqtt
import settings


MQTT_CLIENT = mqtt.Mqtt()
MON_LOG = MonLog()
LAST_MONITORING_MESSAGE = 0


def shutdown():
    '''
    Shutdown the process gracefully.
    '''

    MQTT_CLIENT.client.loop_stop()
    settings.logger.debug("MQTT client loop stopped.")
    settings.logger.info("Client disconnecting.")
    MQTT_CLIENT.client.disconnect()

def terminate_signal_handler(_signal, _frame):
    '''
    Handler for TERM and INT signals.
    '''
    settings.logger.critical("Got termination signal from system.")
    shutdown()

def handle_message(message):
    '''
    Callback called by Mqtt for every message of the topic.
    '''
    global MON_LOG
    global LAST_MONITORING_MESSAGE
    try:
        parsed = parse_gateway_message(message)
    except GatewayMessageError as err: 
        # parser couldn't do its thing, likely malformed payload
        settings.logger.warning(str(err))
        # message type is bytes
        settings.logger.debug("Failed message: " + message.decode("utf-8"))
        traceback.print_exc(limit=4, file=sys.stdout)
        MON_LOG.n_fail += 1
    else:
        settings.logger.debug("Parsed message successfully.")
        MQTT_CLIENT.publish(parsed)
        MON_LOG.n_success += 1
        # rate limit monitoring message
        if MON_LOG.allow():
            MQTT_CLIENT.publish_monitor(MON_LOG)

if __name__ == '__main__':
    # setting handler for terminate and interrupt signals
    signal.signal(signal.SIGTERM, terminate_signal_handler)
    signal.signal(signal.SIGINT, terminate_signal_handler)

    MQTT_CLIENT.message_handler = handle_message
    MQTT_CLIENT.connect()
