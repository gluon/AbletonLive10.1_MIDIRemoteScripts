# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/delay_decoration.py
# Compiled at: 2019-05-08 17:06:57
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import EventObject, listens, liveobj_valid
from ableton.v2.control_surface import LiveObjectDecorator, NotifyingList, get_parameter_by_name
from .internal_parameter import EnumWrappingParameter

class ChannelType(int):
    pass


ChannelType.left_right = ChannelType(0)
ChannelType.left = ChannelType(1)
ChannelType.right = ChannelType(2)

class LinkedState(int):
    pass


LinkedState.unlinked = LinkedState(0)
LinkedState.linked = LinkedState(1)

class DelayDeviceDecorator(LiveObjectDecorator, EventObject):
    sync_modes = (u'Time', u'Sync')
    link_modes = (u'Linked', u'Unlinked')

    def __init__(self, *a, **k):
        super(DelayDeviceDecorator, self).__init__(*a, **k)
        self._channel_type_provider = NotifyingList(available_values=[
         'L+R', 'Left', 'Right'], default_value=ChannelType.left_right)
        self._additional_parameters = self._create_parameters()
        self.register_disconnectables(self._additional_parameters)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    def _create_parameters(self):
        self._channel_switch = EnumWrappingParameter(name='Channel', parent=self, values_host=self._channel_type_provider, index_property_host=self._channel_type_provider, values_property='available_values', index_property='index', value_type=ChannelType)
        self._delay_line_link_parameter = get_parameter_by_name(self, 'Link')
        self.__on_channel_switch_changed.subject = self._channel_switch
        self.__on_linked_changed.subject = self._delay_line_link_parameter
        self.__on_linked_changed()
        return (
         self._channel_switch,
         EnumWrappingParameter(name='L Sync Enum', parent=self, values_host=self, values_property='sync_modes', index_property_host=get_parameter_by_name(self, 'L Sync'), index_property='value', to_index_conversion=lambda index: int(index), from_index_conversion=lambda index: int(index)),
         EnumWrappingParameter(name='R Sync Enum', parent=self, values_host=self, values_property='sync_modes', index_property_host=get_parameter_by_name(self, 'R Sync'), index_property='value', to_index_conversion=lambda index: int(index), from_index_conversion=lambda index: int(index)),
         EnumWrappingParameter(name='Link Switch', parent=self, values_host=self, values_property='link_modes', index_property_host=self._delay_line_link_parameter, index_property='value', to_index_conversion=lambda index: int(not index), from_index_conversion=lambda index: int(not index)))

    def _linked_state_needs_updating(self):
        if liveobj_valid(self._delay_line_link_parameter):
            is_delay_line_linked = self._delay_line_link_parameter.value == LinkedState.linked
            is_channel_switch_linked = self._channel_switch.value == ChannelType.left_right
            return is_delay_line_linked != is_channel_switch_linked

    @listens('value')
    def __on_channel_switch_changed(self):
        if self._linked_state_needs_updating():
            self._delay_line_link_parameter.value = LinkedState.linked if self._channel_switch.value == ChannelType.left_right else LinkedState.unlinked

    @listens('value')
    def __on_linked_changed(self):
        if self._linked_state_needs_updating():
            self._channel_switch.value = ChannelType.left_right if self._delay_line_link_parameter.value == LinkedState.linked else ChannelType.left