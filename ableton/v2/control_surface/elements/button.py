# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/elements/button.py
# Compiled at: 2019-05-15 02:17:17
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ...base import BooleanContext, const, in_range, has_event, listens
from ..input_control_element import InputControlElement, MIDI_CC_TYPE
from ..skin import Skin
from .color import Color

class DummyUndoStepHandler(object):

    def begin_undo_step(self):
        pass

    def end_undo_step(self):
        pass


class ButtonElementMixin(object):
    u"""
    Mixin for sending values to button-like control-elements elements.
    """

    def set_light(self, value):
        pass


class ButtonElement(InputControlElement, ButtonElementMixin):
    u"""
    Class representing a button a the controller
    """

    class ProxiedInterface(InputControlElement.ProxiedInterface, ButtonElementMixin):
        is_momentary = const(True)
        is_pressed = const(False)

    class Colors:

        class DefaultButton:
            On = Color(127)
            Off = Color(1)
            Disabled = Color(0)

    num_delayed_messages = 2

    def __init__(self, is_momentary, msg_type, channel, identifier, is_rgb=False, skin=Skin(Colors), undo_step_handler=DummyUndoStepHandler(), send_should_depend_on_forwarding=False, *a, **k):
        super(ButtonElement, self).__init__(msg_type, channel, identifier, send_should_depend_on_forwarding=send_should_depend_on_forwarding, *a, **k)
        self.is_rgb = is_rgb
        self._is_momentary = bool(is_momentary)
        self._last_received_value = -1
        self._undo_step_handler = undo_step_handler
        self._skin = skin
        self._drawing_via_skin = BooleanContext()

    def reset(self):
        self.set_light('DefaultButton.Disabled')
        self.use_default_message()
        self.suppress_script_forwarding = False

    def is_momentary(self):
        u""" returns true if the buttons sends a message on being released """
        return self._is_momentary

    def message_map_mode(self):
        assert self.message_type() is MIDI_CC_TYPE
        return Live.MidiMap.MapMode.absolute

    def is_pressed(self):
        return self._is_momentary and int(self._last_received_value) > 0

    def set_light(self, value):
        if hasattr(value, 'draw'):
            value.draw(self)
        elif type(value) in (int, long) and in_range(value, 0, 128):
            self.send_value(value)
        elif isinstance(value, bool):
            self._set_skin_light('DefaultButton.On' if value else 'DefaultButton.Off')
        else:
            self._set_skin_light(value)

    def _set_skin_light(self, value):
        color = None
        try:
            color = self._skin[value]
            self._do_draw(color)
        finally:
            if has_event(color, 'midi_value'):
                self.__on_midi_value_changed.subject = color
            else:
                self._disconnect_color_listener()

        return

    def _do_draw(self, color):
        with self._drawing_via_skin():
            color.draw(self)

    @listens('midi_value')
    def __on_midi_value_changed(self, *a):
        self._do_draw(self.__on_midi_value_changed.subject)

    def send_value(self, value, force=False, channel=None):
        if not self._drawing_via_skin:
            self._disconnect_color_listener()
        super(ButtonElement, self).send_value(value, force, channel)

    def receive_value(self, value):
        pressed_before = self.is_pressed()
        self._last_received_value = value
        if not pressed_before and self.is_pressed():
            self._undo_step_handler.begin_undo_step()
        super(ButtonElement, self).receive_value(value)
        if pressed_before and not self.is_pressed():
            self._undo_step_handler.end_undo_step()

    def disconnect(self):
        super(ButtonElement, self).disconnect()
        self._undo_step_handler = None
        return

    def _disconnect_color_listener(self):
        self.__on_midi_value_changed.subject = None
        return