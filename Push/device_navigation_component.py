# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Push/device_navigation_component.py
# Compiled at: 2019-04-09 19:23:44
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from contextlib import contextmanager
import Live.DrumPad
from ableton.v2.base import BooleanContext, const, depends, disconnectable, inject, in_range, listens, liveobj_valid, NamedTuple
from ableton.v2.control_surface import Component
from pushbase import consts
from pushbase.device_chain_utils import is_first_device_on_pad
from pushbase.message_box_component import MessageBoxComponent
from pushbase.scrollable_list_component import ScrollableListWithTogglesComponent
from .navigation_node import make_navigation_node

class DeviceNavigationComponent(Component):
    u"""
    Component that displays an overview of the devices in the current
    track and navigates in its hierarchy.
    """

    def __init__(self, device_bank_registry=None, banking_info=None, info_layer=None, delete_handler=None, session_ring=None, *a, **k):
        super(DeviceNavigationComponent, self).__init__(*a, **k)
        self._make_navigation_node = partial(make_navigation_node, session_ring=session_ring, device_bank_registry=device_bank_registry, banking_info=banking_info)
        self._delete_handler = delete_handler
        self._updating_children = BooleanContext()
        self._device_list = ScrollableListWithTogglesComponent(parent=self)
        self._on_selection_clicked_in_controller.subject = self._device_list
        self._on_selection_changed_in_controller.subject = self._device_list
        self._on_state_changed_in_controller.subject = self._device_list
        self._current_node = None
        self._message_box = MessageBoxComponent(parent=self, layer=info_layer, is_enabled=False)
        self._message_box.text = consts.MessageBoxText.EMPTY_DEVICE_CHAIN
        self._selected_track = None
        self._on_selected_track_changed.subject = self.song.view
        with inject(selection=const(NamedTuple(selected_device=None))).everywhere():
            self._on_selected_track_changed()
        self._on_device_parameters_changed.subject = self._selected_track.view.selected_device
        return

    @property
    def current_node(self):
        return self._current_node

    def set_select_buttons(self, select_buttons):
        self._device_list.set_select_buttons(select_buttons)

    def set_state_buttons(self, state_buttons):
        self._device_list.set_state_buttons(state_buttons)

    def set_exit_button(self, exit_button):
        assert not exit_button or exit_button.is_momentary()
        self._on_exit_value.subject = exit_button
        self._update_exit_button()

    def set_enter_button(self, enter_button):
        assert not enter_button or enter_button.is_momentary()
        self._on_enter_value.subject = enter_button
        self._update_enter_button()

    def set_display_line(self, line):
        self._device_list.set_display_line(line)

    def set_blank_display_line(self, line):
        if line:
            line.reset()

    @property
    def selected_object(self):
        selected = None
        if self._current_node:
            children = self._current_node.children
            option = self._device_list.selected_option
            if children and in_range(option, 0, len(children)):
                _, selected = children[option]
        return selected

    def back_to_top(self):
        if consts.PROTO_SONG_IS_ROOT:
            self._set_current_node(self._make_navigation_node(self.song))
        else:
            self._set_current_node(self._make_navigation_node(self._selected_track))

    @listens('selected_track')
    def _on_selected_track_changed(self):
        self._selected_track = self.song.view.selected_track
        self._on_selected_device_changed.subject = self._selected_track.view
        self.back_to_top()

    @listens('selected_device')
    def _on_selected_device_changed(self):
        selected_device = self._selected_track.view.selected_device
        if selected_device == None:
            self._set_current_node(self._make_exit_node())
            return
        else:
            is_just_default_child_selection = False
            if self._current_node and self._current_node.children:
                selected = self.selected_object
                if isinstance(selected, Live.DrumPad.DrumPad) and is_first_device_on_pad(selected_device, selected):
                    is_just_default_child_selection = True
                if isinstance(selected, Live.Chain.Chain) and selected_device and selected_device.canonical_parent == selected and selected.devices[0] == selected_device:
                    is_just_default_child_selection = True
            if not is_just_default_child_selection:
                target = selected_device and selected_device.canonical_parent
                if not self._current_node or self._current_node.object != target:
                    node = self._make_navigation_node(target, is_entering=False)
                    self._set_current_node(node)
            self._on_device_parameters_changed.subject = selected_device
            return

    @listens('parameters')
    def _on_device_parameters_changed(self):
        self._update_enter_button()
        self._update_exit_button()

    def _set_current_node(self, node):
        if node is None:
            return
        else:
            self.disconnect_disconnectable(self._current_node)
            self._current_node = node
            self.register_disconnectable(node)
            self._on_children_changed_in_node.subject = node
            self._on_selected_child_changed_in_node.subject = node
            self._on_state_changed_in_node.subject = node
            self._on_children_changed_in_node()
            for index, value in enumerate(node.state):
                self._on_state_changed_in_node(index, value)

            node.preselect()
            return

    @depends(selection=lambda : NamedTuple(selected_device=None))
    def _update_info(self, selection=None):
        if liveobj_valid(self._selected_track) and len(self._selected_track.devices) == 0 and selection.selected_device == None:
            self._message_box.set_enabled(True)
        else:
            self._message_box.set_enabled(False)
        return

    def update(self):
        super(DeviceNavigationComponent, self).update()
        if self.is_enabled():
            self._update_enter_button()
            self._update_exit_button()
            self._update_info()

    @contextmanager
    def _deactivated_option_listener(self):
        old_subject = self._on_state_changed_in_controller.subject
        self._on_state_changed_in_controller.subject = None
        yield
        self._on_state_changed_in_controller.subject = old_subject
        return

    @listens('state')
    def _on_state_changed_in_node(self, index, value):
        with self._deactivated_option_listener():
            self._device_list.set_option_state(index, value)

    @listens('children')
    def _on_children_changed_in_node(self):
        if self._updating_children:
            return
        with self._updating_children():
            if not self._current_node.children:
                self.back_to_top()
            names = map(lambda x: x[0], self._current_node.children)
            self._device_list.option_names = names
            self._device_list.selected_option = self._current_node.selected_child
            self._update_enter_button()
            self._update_exit_button()

    @listens('selected_child')
    def _on_selected_child_changed_in_node(self, index):
        self._device_list.selected_option = index
        self._update_enter_button()
        self._update_exit_button()
        self._update_info()

    @property
    def _is_deleting(self):
        return self._delete_handler and self._delete_handler.is_deleting

    @listens('toggle_option')
    def _on_state_changed_in_controller(self, index, value):
        if self._current_node:
            if self._is_deleting:
                _, child = self._current_node.children[index]
                if child != None and isinstance(child, Live.Device.Device):
                    self._delete_handler.delete_clip_envelope(child.parameters[0])
            else:
                self._current_node.set_state(index, value)
            if self._current_node.state[index] != value:
                with self._deactivated_option_listener():
                    self._device_list.set_option_state(index, self._current_node.state[index])
        return

    @listens('change_option')
    def _on_selection_changed_in_controller(self, value):
        self._current_node.selected_child = value
        self._update_hotswap_target()
        self._update_enter_button()
        self._update_exit_button()

    @listens('press_option', in_front=True)
    def _on_selection_clicked_in_controller(self, index):
        if self._is_deleting:
            if self._current_node:
                self._current_node.delete_child(index)
            return True
        if consts.PROTO_FAST_DEVICE_NAVIGATION:
            if self._device_list.selected_option == index:
                self._set_current_node(self._make_enter_node())
                return True
            if not in_range(index, 0, len(self._device_list.option_names)):
                self._set_current_node(self._make_exit_node())
                return True
        return index == None

    @listens('value')
    def _on_enter_value(self, value):
        if self.is_enabled():
            self._update_enter_button()
            if value:
                self._set_current_node(self._make_enter_node())
                self._update_hotswap_target()

    @listens('value')
    def _on_exit_value(self, value):
        if self.is_enabled():
            self._update_exit_button()
            if value:
                self._set_current_node(self._make_exit_node())
                self._update_hotswap_target()

    def _update_hotswap_target(self):
        try:
            browser = self.application.browser
            if liveobj_valid(self.selected_object) and liveobj_valid(browser.hotswap_target):
                browser.hotswap_target = self.selected_object
        except RuntimeError:
            pass

    def _make_enter_node(self):
        if self._device_list.selected_option >= 0 and self._device_list.selected_option < len(self._current_node.children):
            child = self._current_node.children[self._device_list.selected_option][1]
            return self._make_navigation_node(child, is_entering=True)

    def _make_exit_node(self):
        return self._make_navigation_node(self._current_node and self._current_node.parent, is_entering=False)

    def _update_enter_button(self):
        button = self._on_enter_value.subject
        if self.is_enabled() and button:
            with disconnectable(self._make_enter_node()) as (node):
                button.set_light('DefaultButton.On' if node else 'DefaultButton.Disabled')

    def _update_exit_button(self):
        button = self._on_exit_value.subject
        if self.is_enabled() and button:
            with disconnectable(self._make_exit_node()) as (node):
                button.set_light('DefaultButton.On' if node else 'DefaultButton.Disabled')