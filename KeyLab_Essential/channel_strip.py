# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/KeyLab_Essential/channel_strip.py
# Compiled at: 2019-04-09 19:23:44
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from .ringed_mapped_encoder_control import RingedMappedEncoderControl

class ChannelStripComponent(ChannelStripComponentBase):
    pan_control = RingedMappedEncoderControl()

    def set_pan_control(self, control):
        self.pan_control.set_control_element(control)
        self.update()

    def _connect_parameters(self):
        super(ChannelStripComponent, self)._connect_parameters()
        self.pan_control.mapped_parameter = self.track.mixer_device.panning

    def _disconnect_parameters(self):
        self.pan_control.mapped_parameter = None
        super(ChannelStripComponent, self)._disconnect_parameters()
        return