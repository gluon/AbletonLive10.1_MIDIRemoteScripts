# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/LV1_LX1/LV1_LX1.py
# Compiled at: 2019-04-09 19:23:44
from __future__ import absolute_import, print_function, unicode_literals
from LV2_LX2_LC2_LD2.FaderfoxComponent import FaderfoxComponent
from LV2_LX2_LC2_LD2.FaderfoxScript import FaderfoxScript
from LV2_LX2_LC2_LD2.FaderfoxMixerController import FaderfoxMixerController
from LV2_LX2_LC2_LD2.FaderfoxDeviceController import FaderfoxDeviceController
from LV2_LX2_LC2_LD2.FaderfoxTransportController import FaderfoxTransportController

class LV1_LX1(FaderfoxScript):
    u"""Automap script for LV1 Faderfox controllers"""
    __module__ = __name__
    __name__ = 'LV1_LX1 Remote Script'

    def __init__(self, c_instance):
        LV1_LX1.realinit(self, c_instance)

    def realinit(self, c_instance):
        self.suffix = '1'
        FaderfoxScript.realinit(self, c_instance)
        self.is_lv1 = True
        self.log('lv1 lx1')
        self.mixer_controller = FaderfoxMixerController(self)
        self.device_controller = FaderfoxDeviceController(self)
        self.transport_controller = FaderfoxTransportController(self)
        self.components = [self.mixer_controller,
         self.device_controller,
         self.transport_controller]