# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Alesis_V/Alesis_V.py
# Compiled at: 2019-04-09 19:23:44
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.Layer import Layer
from _Framework.EncoderElement import EncoderElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.DeviceComponent import DeviceComponent

class Alesis_V(ControlSurface):

    def __init__(self, *a, **k):
        super(Alesis_V, self).__init__(*a, **k)
        with self.component_guard():
            encoders = ButtonMatrixElement(rows=[
             [ EncoderElement(MIDI_CC_TYPE, 0, identifier + 20, Live.MidiMap.MapMode.absolute, name='Encoder_%d' % identifier) for identifier in xrange(4)
             ]])
            device = DeviceComponent(name='Device', is_enabled=False, layer=Layer(parameter_controls=encoders), device_selection_follows_track_selection=True)
            device.set_enabled(True)
            self.set_device_component(device)