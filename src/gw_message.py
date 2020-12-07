#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
This module parses the json message from the gateway, and invokes
payload.py for parsing the sensor paylaod.
'''

import json
import time
import datetime

from payload import load, PayloadError
import settings

# in_mesg_json is an str directly from the MQTT broker
schema_in_mesg = {
    "_msqid": "str", # _msqid is passed trough for reference
    "ack": "bool",
    "adr": "str",
    "appeui": "str",
    "chan": "int",
    "cls": "int",
    "codr": "str",
    "datr": "str",
    "deveui": "str",
    "eui": "str",
    "freq": "str",
    "lsnr": "str",
    "mhdr": "str",
    "modu": "str",
    "opts": "str", # optional
    "port": "int",
    "rfch": "int",
    "rssi": "int",
    "seqn": "int",
    "size": "int",
    "time": "int",
    "tmst": "int",
    "fcnt": "int",
    "gweui": "str",
    "stat": "int",
    "payload": "list[int]"
}

# parsed is returned by parse_elsys_message()
schema_parsed = {
    "_msqid": "str",
    "deveui": "str",
    "timestamp_node": "float",
    "timestamp_parser": "float",
    "temperature": "float", # optional
    "humidity": "float", # optional
    "light": "float", # optional
    "pir": "float", # optional
    "co2": "float", # optional
    "battery": "float", # optional
    "sound_avg": "float", # optional
    "sound_peak": "float" # optional
}

class GatewayMessageError(Exception):
    pass

class GatewayMessageIgnored(RuntimeWarning):
    pass

def parse_gateway_message(in_mesg_json):
    '''
    Parses a message from the gateway and calls payload for parsing the elsys-compatible payload

    Returns a json string that includes only the new values.

    Please refer to the README for reference of the input and output.
    '''
    try:
        in_mesq = json.loads(in_mesg_json)
    except ValueError as err:
        raise GatewayMessageError("Message from broker is not a valid JSON") from err

    parsed = {}

    valid_appeui = settings.config.get("ElsysDeployment", "appeui")
    if in_mesq["appeui"] != valid_appeui:
        raise GatewayMessageIgnored("Unexpected appeui {}: message not intended for this deployment.".format(in_mesq["appeui"]))

    valid_ports = settings.config.get("ElsysDeployment", "ports").split(",")
    print(valid_ports, type(valid_ports))
    if str(in_mesq["port"]) not in valid_ports:
        raise GatewayMessageIgnored("Unexpected port {}: message not intended for this deployment.".format(in_mesq["port"]))

    try:
        parsed["_msgid"] = in_mesq["_msgid"] # _msqid is passed trough for reference
        parsed["deveui"] = in_mesq["deveui"]
        # assume upstream generates timestamps in UTC timezone
        try:
            timestr = in_mesq["time"]
        except KeyError:
            pass
        else:
            node_datetime = datetime.datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%S.%fZ")
            parsed["timestamp_node"] = node_datetime.replace(tzinfo=datetime.timezone.utc).timestamp()

        try:
            parsed.update(load(in_mesq["payload"]))
        except PayloadError as err:
            raise GatewayMessageError("Payload parser encountered an error.") from err

        for key, value in parsed.items():
            parsed[key] = value

        parsed["timestamp_parser"] = time.time()
        parsed_json = json.dumps(parsed)
        return parsed_json
    except ValueError as err:
        raise GatewayMessageError("Something went wrong while parsing.") from err