#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time
import datetime
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
    "temperature": "float",
    "humidity": "float",
    "light": "float",
    "pir": "float", # optional
    "co2": "float", # optional
    "battery": "float"
}

class ElsysParserError(Exception):
    pass

def parse_elsys_message(in_mesg_json):
    '''
    Parses a message from Elsys sensors

    Returns a json string that includes only the new values.

    Example in_mesg_json [str]
        {
            "ack":false, 
            "adr":true,
            "appeui":"43-57-43-5f-44-45-4d-4f",
            "chan":0,
            "cls":0,
            "codr":"4/5",
            "datr":"SF7BW125",
            "deveui":"a8-17-58-ff-fe-03-0f-f5",
            "freq":"868.1",
            "lsnr":"9.2",
            "mhdr":"406000000280d009",
            "modu":"LORA",
            "opts":"",
            "port":5,
            "rfch":0,
            "rssi":-97,
            "seqn":2512,
            "size":24,
            "timestamp":"2019-06-27T06:36:41.189934Z",
            "tmst":2835661339,
            "payload":[1,0,231,2,38,4,1,159,5,3,6,1,167,7,14,98],
            "eui":"a8-17-58-ff-fe-03-0f-f5",
            "_msgid":"8ff111b9.700ef"
        }
    '''
    try:
        in_mesq = json.loads(in_mesg_json)
    except ValueError as err:
        raise ElsysParserError("Message from broker is not a valid JSON") from err
    parsed = {}
    valid_appeui = settings.config.get('ElsysDeployment', 'appeui')
    if in_mesq["appeui"] == valid_appeui:
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
            
            payload = in_mesq["payload"]
            mesg_size = in_mesq["size"]
            parsed["temperature"] = ((payload[1] * 256) + payload[2]) / 10
            parsed["humidity"] = payload[4]
            parsed["light"] = (payload[6] * 256) + payload[7]
            if mesg_size == 16: # no pir, no co2
                #parsed["pir"] = 0.0
                #parsed["co2"] = 0.0
                parsed["battery"] = ((payload[9] * 256) + payload[10]) / 1000
            elif mesg_size == 20: # no pir
                parsed["pir"] = payload[9]
                #parsed["co2"] = 0.0
                parsed["battery"] = ((payload[11] * 256) + payload[12]) / 1000
            elif mesg_size == 24:
                parsed["pir"] = payload[9]
                parsed["co2"] = (payload[11] * 256) + payload[12]
                parsed["battery"] = ((payload[14] * 256) + payload[15]) / 1000
            else:
                raise ElsysParserError("Unexpected message size.")
            parsed["timestamp_parser"] = time.time()
            parsed_json = json.dumps(parsed)
            return parsed_json
        except ValueError as err:
            raise ElsysParserError("Something went wrong while parsing.") from err
    else:
        raise ElsysParserError("Unexpected appeui message not intended for this deployment")
