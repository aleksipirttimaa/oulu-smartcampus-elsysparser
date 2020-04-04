#!/usr/bin/python

'''
Contains global variables. 🆘
'''
import logging
import logging.config  # needed for logging to work
import configparser
import os
import sys

# loading configuration file
config_file_name = 'server.conf'
config = configparser.ConfigParser()
config.read(config_file_name)

'''
# cat server.conf.example
[MqttBroker]
host: 127.0.0.1
port: 1883
user: user
passwd: pass
in_topic: cwc/elsys/downlinkMessage
out_topic: cwc/elsys/parsed
monitor_topic: cwc/elsys/parserStatus # if you want to use monitoring
certificate_path: ca.crt # if you want to use tls
# please set unique identifier for client
client_id: elsysparser_tellus

[ElsysDeployment]
appeui: 43-57-43-5f-44-45-4d-4f
'''

# setting up logger
file_name, extension = os.path.splitext(os.path.basename(sys.argv[0]))
logger = logging.getLogger(file_name)
handler = logging.handlers.RotatingFileHandler((file_name + '.log'), maxBytes=10485670, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())
logger.setLevel('INFO')
#logger.setLevel('DEBUG')

