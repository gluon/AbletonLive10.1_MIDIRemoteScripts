# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchkey_MK2/consts.py
# Compiled at: 2019-04-09 19:23:44
from __future__ import absolute_import, print_function, unicode_literals
PRODUCT_ID_BYTE_PREFIX = (0, 32, 41)
LAUNCHKEY_25_ID_BYTE = 123
LAUNCHKEY_49_ID_BYTE = 124
LAUNCHKEY_61_ID_BYTE = 125
PRODUCT_ID_BYTES = (
 LAUNCHKEY_25_ID_BYTE,
 LAUNCHKEY_49_ID_BYTE,
 LAUNCHKEY_61_ID_BYTE)
IDENTITY_REQUEST = (240, 126, 127, 6, 1, 247)
IN_CONTROL_QUERY = (159, 11, 0)
DRUM_IN_CONTROL_ON_MESSAGE = (159, 15, 127)
DRUM_IN_CONTROL_OFF_MESSAGE = (159, 15, 0)
STANDARD_CHANNEL = 15
PULSE_LED_CHANNEL = 2
BLINK_LED_CHANNEL = 1
MAX_SENDS = 6