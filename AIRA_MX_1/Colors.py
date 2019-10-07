# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/AIRA_MX_1/Colors.py
# Compiled at: 2019-05-15 02:17:38
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonElement import Color
BLINK_LED_CHANNEL = 14

class Blink(Color):

    def draw(self, interface):
        interface.send_value(self.midi_value)
        interface.send_value(0, channel=BLINK_LED_CHANNEL)


class Rgb:
    BLACK = Color(0)
    RED = Color(5)
    RED_BLINK = Blink(5)
    GREEN_HALF = Color(20)
    GREEN = Color(21)
    GREEN_BLINK = Blink(21)
    BLUE_HALF = Color(44)
    BLUE = Color(45)
    BLUE_BLINK = Blink(45)