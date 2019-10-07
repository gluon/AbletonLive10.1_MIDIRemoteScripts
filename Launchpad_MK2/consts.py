# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_MK2/consts.py
# Compiled at: 2019-04-09 19:23:44
from __future__ import absolute_import, print_function, unicode_literals
PRODUCT_ID_BYTES = (0, 32, 41, 105, 0, 0, 0)
IDENTITY_REQUEST = (240, 126, 127, 6, 1, 247)
STANDARD_SYSEX_PREFIX = (240, 0, 32, 41, 2, 24)
CHALLENGE_RESPONSE_BYTE = (64, )
LAYOUT_CHANGE_BYTE = (34, )
FADER_SETUP_BYTE = (43, )
QUIT_MESSAGE = (240, 0, 32, 41, 2, 24, 64, 247)
BLINK_LED_CHANNEL = 1
PULSE_LED_CHANNEL = 2
USER_MODE_CHANNELS = (5, 6, 7, 13, 14, 15)
VOLUME_MODE_CHANNEL = 3
PAN_MODE_CHANNEL = 4
SEND_A_MODE_CHANNEL = 8
SEND_B_MODE_CHANNEL = 9
FADER_STANDARD_TYPE = 0
FADER_BIPOLAR_TYPE = 1
SESSION_WIDTH = 8