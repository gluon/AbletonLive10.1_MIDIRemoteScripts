# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/actions.py
# Compiled at: 2019-05-15 02:17:17
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import forward_property, listens
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import ToggleComponent
from ableton.v2.control_surface.control import ButtonControl, ColorSysexControl, TextDisplayControl, ToggleButtonControl, control_list
from .control import BinaryControl
ACTION_NAMES = (u'Undo', u'Redo', u'Click', u'', u'', u'', u'', u'')
UNDO_DISPLAY_INDEX = 0
REDO_DISPLAY_INDEX = 1
METRONOME_DISPLAY_INDEX = 2
CAPTURE_DISPLAY_INDEX = 7

class ActionsComponent(Component):
    actions_display = TextDisplayControl(segments=ACTION_NAMES)
    actions_color_fields = control_list(ColorSysexControl, len(ACTION_NAMES))
    actions_selection_fields = control_list(BinaryControl, len(ACTION_NAMES))
    undo_button = ButtonControl(color='Action.Available')
    redo_button = ButtonControl(color='Action.Available')
    capture_midi_button = ButtonControl()
    metronome_button = ToggleButtonControl(toggled_color='Transport.MetronomeOn', untoggled_color='Transport.MetronomeOff')

    def __init__(self, *a, **k):
        super(ActionsComponent, self).__init__(*a, **k)
        self.__on_can_capture_midi_changed.subject = self.song
        self.__on_can_capture_midi_changed()
        self.actions_color_fields[METRONOME_DISPLAY_INDEX].color = 'Transport.MetronomeOn'
        self.actions_color_fields[UNDO_DISPLAY_INDEX].color = 'Action.Available'
        self.actions_color_fields[REDO_DISPLAY_INDEX].color = 'Action.Available'
        self.__on_metronome_changed.subject = self.song
        self.__on_metronome_changed()

    @property
    def capture_midi_display(self):
        return self.actions_display[CAPTURE_DISPLAY_INDEX]

    @capture_midi_display.setter
    def capture_midi_display(self, string):
        self.actions_display[CAPTURE_DISPLAY_INDEX] = string

    @property
    def capture_midi_color_field(self):
        return self.actions_color_fields[CAPTURE_DISPLAY_INDEX]

    @property
    def capture_midi_selection_field(self):
        return self.actions_selection_fields[CAPTURE_DISPLAY_INDEX]

    @undo_button.pressed
    def undo_button(self, _):
        if self.song.can_undo:
            self.song.undo()

    @redo_button.pressed
    def redo_button(self, _):
        if self.song.can_redo:
            self.song.redo()

    @capture_midi_button.pressed
    def capture_midi_button(self, _):
        try:
            self.song.capture_midi()
        except RuntimeError:
            pass

    @metronome_button.toggled
    def metronome_button(self, toggled, _):
        self.song.metronome = toggled

    @listens('can_capture_midi')
    def __on_can_capture_midi_changed(self):
        self._update_capture_midi_controls()

    @listens('metronome')
    def __on_metronome_changed(self):
        self._update_metronome_controls()

    def _update_capture_midi_controls(self):
        can_capture_midi = self.song.can_capture_midi
        self.capture_midi_button.enabled = can_capture_midi
        self.capture_midi_display = 'capture' if can_capture_midi else ''
        self.capture_midi_color_field.color = 'DefaultButton.On' if can_capture_midi else 'DefaultButton.Disabled'
        self.capture_midi_selection_field.is_on = can_capture_midi

    def _update_metronome_controls(self):
        metronome = self.song.metronome
        self.metronome_button.is_toggled = metronome
        self.actions_selection_fields[METRONOME_DISPLAY_INDEX].is_on = metronome