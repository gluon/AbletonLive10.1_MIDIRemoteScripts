# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/LV2_LX2_LC2_LD2/LV2_LX2_LC2_LD2.py
# Compiled at: 2019-04-09 19:23:44
from __future__ import absolute_import, print_function, unicode_literals
import Live
from .FaderfoxScript import FaderfoxScript
from .LV2MixerController import LV2MixerController
from .LV2DeviceController import LV2DeviceController
from .FaderfoxDeviceController import FaderfoxDeviceController
from .LV2TransportController import LV2TransportController
from .consts import *

class LV2_LX2_LC2_LD2(FaderfoxScript):
    u"""Automap script for LV2 Faderfox controllers"""
    __module__ = __name__
    __name__ = 'LV2_LX2_LC2_LD2 Remote Script'

    def __init__(self, c_instance):
        LV2_LX2_LC2_LD2.realinit(self, c_instance)

    def realinit(self, c_instance):
        self.suffix = '2'
        FaderfoxScript.realinit(self, c_instance)
        self.mixer_controller = LV2MixerController(self)
        self.device_controller = LV2DeviceController(self)
        self.transport_controller = LV2TransportController(self)
        self.components = [self.mixer_controller, self.device_controller,
         self.transport_controller]

    def suggest_map_mode(self, cc_no, channel):
        return -1