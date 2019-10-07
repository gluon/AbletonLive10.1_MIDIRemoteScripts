# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/device_navigation.py
# Compiled at: 2019-05-08 17:06:57
from __future__ import absolute_import, print_function, unicode_literals
from itertools import izip_longest
from ableton.v2.base import listens, listens_group
from ableton.v2.control_surface import Layer
from ableton.v2.control_surface.components import DeviceNavigationComponent
from ableton.v2.control_surface.control import ColorSysexControl, TextDisplayControl, control_list
from .control import BinaryControl
NUM_VISIBLE_ITEMS = 16
NUM_DISPLAY_SEGMENTS = NUM_VISIBLE_ITEMS / 2

class DisplayingDeviceNavigationComponent(DeviceNavigationComponent):
    device_name_display_1 = TextDisplayControl(segments=(u'', ) * NUM_DISPLAY_SEGMENTS)
    device_name_display_2 = TextDisplayControl(segments=(u'', ) * NUM_DISPLAY_SEGMENTS)
    device_bank_name_display_1 = TextDisplayControl(segments=(u'', ) * NUM_DISPLAY_SEGMENTS)
    device_bank_name_display_2 = TextDisplayControl(segments=(u'', ) * NUM_DISPLAY_SEGMENTS)
    selected_device_name_display = TextDisplayControl(segments=(u'', ))
    selected_device_bank_name_display = TextDisplayControl(segments=(u'', ))
    device_color_fields = control_list(ColorSysexControl, NUM_VISIBLE_ITEMS)
    device_selection_fields = control_list(BinaryControl, NUM_VISIBLE_ITEMS)

    def __init__(self, banking_info=None, device_bank_registry=None, *a, **k):
        super(DisplayingDeviceNavigationComponent, self).__init__(*a, **k)
        self.select_buttons.control_count = NUM_VISIBLE_ITEMS
        assert banking_info is not None
        assert device_bank_registry is not None
        self._banking_info = banking_info
        self._device_bank_registry = device_bank_registry
        self.__on_items_changed.subject = self
        self.__on_items_changed()
        self.__on_selection_changed.subject = self._item_provider
        self.__on_selection_changed()
        self.__on_device_bank_changed.subject = self._device_bank_registry
        return

    @listens('items')
    def __on_items_changed(self):
        for index, control in enumerate(self.select_buttons):
            control.enabled = index < len(self.items)

        self._update_button_colors()
        self._update_device_color_fields()
        self._update_device_names()
        self._update_device_bank_names()
        self._update_selection_display()
        self._scroll_overlay.update_scroll_buttons()
        self.__on_item_names_changed.replace_subjects(self.items)

    @listens('selected_item')
    def __on_selection_changed(self):
        self._update_button_colors()
        self._update_selection_display()
        self._update_selected_device_name_display()
        self._update_selected_device_bank_name_display()
        self.__on_selected_item_name_changed.subject = self._item_provider.selected_item

    @listens_group('name')
    def __on_item_names_changed(self, something):
        self._update_device_names()

    @listens('device_bank')
    def __on_device_bank_changed(self, *a):
        self._update_device_bank_names()
        self._update_selected_device_bank_name_display()

    @listens('name')
    def __on_selected_item_name_changed(self):
        self._update_selected_device_name_display()

    def _update_device_color_fields(self):
        for color_field, item in izip_longest(self.device_color_fields, self.items):
            color_field.color = 'Device.On' if item else 'DefaultButton.Disabled'

    def _update_selection_display(self):
        selected_item = self._item_provider.selected_item
        for selection_field, item in izip_longest(self.device_selection_fields, self.items):
            selection_field.is_on = bool(item) and self._items_equal(item, selected_item)

    def _update_device_names(self):
        for index, item in izip_longest(xrange(NUM_VISIBLE_ITEMS), self.items):
            display = getattr(self, ('device_name_display_{}').format(index / NUM_DISPLAY_SEGMENTS + 1))
            display[index % NUM_DISPLAY_SEGMENTS] = item.item.name if item else ''

    def _update_device_bank_names(self):
        for index, item in izip_longest(xrange(NUM_VISIBLE_ITEMS), self.items):
            display = getattr(self, ('device_bank_name_display_{}').format(index / NUM_DISPLAY_SEGMENTS + 1))
            display[index % NUM_DISPLAY_SEGMENTS] = self._bank_name_for_item(item.item if item else None)

        return

    def _update_selected_device_name_display(self):
        item = self._item_provider.selected_item
        self.selected_device_name_display[0] = item.name if item else 'No Device'

    def _update_selected_device_bank_name_display(self):
        self.selected_device_bank_name_display[0] = self._bank_name_for_item(self._item_provider.selected_item)

    def _bank_name_for_item(self, item):
        bank_name = ''
        if item:
            item_bank_names = self._banking_info.device_bank_names(item)
            if item_bank_names:
                bank = self._device_bank_registry.get_device_bank(item)
                bank_name = item_bank_names[bank]
        return bank_name