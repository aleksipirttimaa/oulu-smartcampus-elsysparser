#!/bin/bash

#  this was a workaround
docker build -t elsysparser:latest ${BASH_SOURCE%/*}
