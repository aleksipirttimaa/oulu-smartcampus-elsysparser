#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Please read ../server.conf.example

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
