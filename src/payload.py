#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
elsys-compatible payload parsing
'''
from json import dumps

def float_from_dual_bite(bite):
    '''
    Helper for a recurring pattern of 16-bit values.
    '''
    return (bite[0] * 256) + bite[1]

def temperature(bite):
    '''
    Unit is Celsius [°C].
    '''
    return { "temperature": float_from_dual_bite(bite) / 10 }

def humidity(bite):
    '''
    Unit is relative humidity [%].
    '''
    return { "humidity": bite[0] }

def light(bite):
    '''
    Unit is ???.
    '''
    return { "light": float_from_dual_bite(bite) }

def motion(bite):
    '''
    Unit depends on sensor config, as of 2020-06
    all sensors have been configured in a unified way,
    where the count is incremented by one for every 30
    second window any motion is detected.
    As a reporting interval of 15 minutes is used, the
    range is 0 - 30.
    '''
    return { "motion": bite[0] }

def co2(bite):
    '''
    Unit is ppm.
    '''
    return { "co2": float_from_dual_bite(bite) }

def battery(bite):
    '''
    Unit is volts [V].
    '''
    return { "battery": float_from_dual_bite(bite) / 1000 }

def sound(bite):
    '''
    Unit is Decibel [dB].
    '''
    return { "sound_peak": bite[0], "sound_avg": bite[1] }

def debug(bite):
    '''
    Debug frames shouldn't prevent parsing.
    '''
    return { "debug": "not implemented" }

# 'STYPE' data type id: handler, length
STYPES = {
    0x01: (temperature, 2),
    0x02: (humidity, 1),
    0x04: (light, 2),
    0x05: (motion, 1),
    0x06: (co2, 2),
    0x07: (battery, 2),
    0x15: (sound, 2),
    0x3d: (debug, 4)
}

# Setting frames are variable in length
STYPE_SETTINGS = 0x3e

STYPE_MASK = 0x3f # 0011 1111

# 'NOB' number of offset bytes
NOBS = {
    0x00: 0, # 00xx xxxx
    0x40: 1, # 01xx xxxx
    0x80: 2, # 10xx xxxx
    0xc0: 4  # 11xx xxxx
}

NOB_MASK = 0xc0 # 1100 0000

class PayloadError(Exception):
    '''
    Raised typically when the parser needs to stop, as it won't
    be able to produce a reliable output.
    '''
    pass

class Payload:
    '''
    Payload instance implements parser logic and string representation.
    '''
    def __init__(self, payload):
        self.data = {}
        self._unparsed = payload

    def __str__(self):
        return dumps(self.data)

    def _parse(self):
        while len(self._unparsed) > 0:
            byte = self._unparsed.pop(0)
            stype_b = byte & STYPE_MASK
            nob_b = byte & NOB_MASK
            nob = NOBS[nob_b]
            if stype_b in STYPES.keys():
                parser = STYPES[stype_b][0]
                length = STYPES[stype_b][1]
                bite = []
                for _ in range(length):
                    bite.append(self._unparsed.pop(0))
                value = parser(bite)
                self.data.update(value)
                offset_b = []
                for _ in range(nob):
                    offset_b.append(self._unparsed.pop(0))
                if offset_b != []:
                    raise PayloadError("Sensor payload contained offset, but that is not supported.")
            elif stype_b == 0x00:
                raise PayloadError("STYPE is null")
            elif stype_b == STYPE_SETTINGS:
                raise PayloadError("STYPE settings is not supported.")
            else:
                raise PayloadError("unknown STYPE: 0x{:02x}".format(stype_b))

    def load(self):
        self._parse()
        return self.data



def load(payload):
    return Payload(payload).load()
