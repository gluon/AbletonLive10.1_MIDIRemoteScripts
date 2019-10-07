# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/device_parameters.py
# Compiled at: 2019-05-08 17:06:57
from __future__ import absolute_import, print_function, unicode_literals
from itertools import izip_longest
from ableton.v2.control_surface import InternalParameterBase
from ableton.v2.control_surface.components import DisplayingDeviceParameterComponent
from ableton.v2.control_surface.control import ColorSysexControl, control_list
from .util import convert_parameter_value_to_midi_value

def is_internal_parameter(parameter):
    return isinstance(parameter, InternalParameterBase)


WIDTH = 8

class DeviceParameterComponent(DisplayingDeviceParameterComponent):
    parameter_color_fields = control_list(ColorSysexControl, WIDTH)
    encoder_color_fields = control_list(ColorSysexControl, WIDTH)

    def __init__(self, *a, **k):
        self._parameter_controls = None
        super(DeviceParameterComponent, self).__init__(*a, **k)
        return

    def set_parameter_controls(self, encoders):
        super(DeviceParameterComponent, self).set_parameter_controls(encoders)
        self._parameter_controls = encoders

    def _update_parameter_values(self):
        super(DeviceParameterComponent, self)._update_parameter_values()
        for parameter, control in izip_longest(self.parameters, self._parameter_controls or []):
            if is_internal_parameter(parameter) and control:
                control.send_value(convert_parameter_value_to_midi_value(parameter))

    def _update_parameters(self):
        super(DeviceParameterComponent, self)._update_parameters()
        self._update_color_fields()

    def _update_color_fields(self):
        for color_field_index, parameter_info in izip_longest(xrange(WIDTH), self._parameter_provider.parameters[:WIDTH]):
            parameter = parameter_info.parameter if parameter_info else None
            color = 'Device.On' if parameter else 'DefaultButton.Disabled'
            self.parameter_color_fields[color_field_index].color = color
            self.encoder_color_fields[color_field_index].color = color

        return