#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Axiom_DirectLink/ShiftableSessionComponent.py
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.SessionComponent import SessionComponent
from _Framework.ButtonElement import ButtonElement

class ShiftableSessionComponent(SessionComponent):
    u""" Special session class that reassigns controls based on a shift button """

    def __init__(self, num_tracks, num_scenes):
        self._shift_button = None
        self._clip_slot_buttons = None
        SessionComponent.__init__(self, num_tracks, num_scenes)

    def disconnect(self):
        SessionComponent.disconnect(self)
        if self._shift_button != None:
            self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = None
        self._clip_slot_buttons = None

    def set_shift_button(self, shift_button):
        assert shift_button == None or shift_button.is_momentary()
        if self._shift_button != None:
            self._shift_button.remove_value_listener(self._shift_value)
        self._shift_button = shift_button
        if self._shift_button != None:
            self._shift_button.add_value_listener(self._shift_value)

    def set_clip_slot_buttons(self, buttons):
        assert buttons == None or isinstance(buttons, tuple) and len(buttons) == self._num_tracks
        self._clip_slot_buttons = buttons
        self._shift_value(0)

    def on_selected_track_changed(self):
        SessionComponent.on_selected_track_changed(self)
        selected_track = self.song().view.selected_track
        tracks = self.tracks_to_use()
        if selected_track in tracks:
            track_index = list(tracks).index(selected_track)
            new_offset = track_index - track_index % self._num_tracks
            assert new_offset / self._num_tracks == int(new_offset / self._num_tracks)
            self.set_offsets(new_offset, self.scene_offset())

    def _shift_value(self, value):
        assert self._shift_button != None
        assert value in range(128)
        for index in range(self._num_tracks):
            slot = self.selected_scene().clip_slot(index)
            if value == 0 or self._clip_slot_buttons == None:
                slot.set_launch_button(None)
            else:
                slot.set_launch_button(self._clip_slot_buttons[index])

    def _bank_right_value(self, value):
        assert value in range(128)
        assert self._bank_right_button != None
        if self.is_enabled():
            if value is not 0 or not self._bank_right_button.is_momentary():
                self.set_offsets(self._track_offset + self._num_tracks, self.scene_offset())

    def _bank_left_value(self, value):
        assert isinstance(value, int)
        assert self._bank_left_button != None
        if self.is_enabled():
            if value is not 0 or not self._bank_left_button.is_momentary():
                self.set_offsets(max(0, self._track_offset - self._num_tracks), self.scene_offset())
