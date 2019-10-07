# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Axiom_DirectLink/ShiftableMixerComponent.py
# Compiled at: 2019-04-09 19:23:44
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.MixerComponent import MixerComponent
from _Framework.ButtonElement import ButtonElement

class ShiftableMixerComponent(MixerComponent):
    u""" Special mixer class that reassigns controls based on a shift button """

    def __init__(self, num_tracks):
        self._shift_button = None
        self._selected_mute_solo_button = None
        self._strip_mute_solo_buttons = None
        self._mute_solo_flip_button = None
        MixerComponent.__init__(self, num_tracks)
        self._selected_tracks = []
        self._register_timer_callback(self._on_timer)
        return

    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        self._selected_tracks = None
        MixerComponent.disconnect(self)
        if self._shift_button != None:
            self._shift_button.remove_value_listener(self._shift_value)
            self._shift_button = None
        if self._mute_solo_flip_button != None:
            self._mute_solo_flip_button.remove_value_listener(self._mute_solo_flip_value)
            self._mute_solo_flip_button = None
        self._selected_mute_solo_button = None
        self._strip_mute_solo_buttons = None
        return

    def set_shift_button(self, shift_button):
        assert shift_button == None or shift_button.is_momentary()
        if self._shift_button != None:
            self._shift_button.remove_value_listener(self._shift_value)
        self._shift_button = shift_button
        if self._shift_button != None:
            self._shift_button.add_value_listener(self._shift_value)
        return

    def set_selected_mute_solo_button(self, button):
        assert isinstance(button, (type(None), ButtonElement))
        self._selected_mute_solo_button = button
        self.selected_strip().set_mute_button(self._selected_mute_solo_button)
        self.selected_strip().set_solo_button(None)
        return

    def set_strip_mute_solo_buttons(self, buttons, flip_button):
        assert buttons is None or isinstance(buttons, tuple) and len(buttons) == len(self._channel_strips)
        assert isinstance(flip_button, (type(None), ButtonElement))
        if self._mute_solo_flip_button != None:
            self._mute_solo_flip_button.remove_value_listener(self._mute_solo_flip_value)
        self._mute_solo_flip_button = flip_button
        if self._mute_solo_flip_button != None:
            self._mute_solo_flip_button.add_value_listener(self._mute_solo_flip_value)
        self._strip_mute_solo_buttons = buttons
        for index in range(len(self._channel_strips)):
            strip = self.channel_strip(index)
            button = None
            if self._strip_mute_solo_buttons != None:
                button = self._strip_mute_solo_buttons[index]
            strip.set_mute_button(button)
            strip.set_solo_button(None)

        return

    def tracks_to_use(self):
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    def _shift_value(self, value):
        assert self._shift_button != None
        assert value in range(128)
        if value > 0:
            self.selected_strip().set_mute_button(None)
            self.selected_strip().set_solo_button(self._selected_mute_solo_button)
        else:
            self.selected_strip().set_solo_button(None)
            self.selected_strip().set_mute_button(self._selected_mute_solo_button)
        return

    def _mute_solo_flip_value(self, value):
        assert self._mute_solo_flip_button != None
        assert value in range(128)
        if self._strip_mute_solo_buttons != None:
            for index in range(len(self._strip_mute_solo_buttons)):
                strip = self.channel_strip(index)
                if value > 0:
                    strip.set_mute_button(None)
                    strip.set_solo_button(self._strip_mute_solo_buttons[index])
                else:
                    strip.set_solo_button(None)
                    strip.set_mute_button(self._strip_mute_solo_buttons[index])

        return

    def _on_timer(self):
        sel_track = None
        while len(self._selected_tracks) > 0:
            track = self._selected_tracks[(-1)]
            if track != None and track.has_midi_input and track.can_be_armed and not track.arm:
                sel_track = track
                break
            del self._selected_tracks[-1]

        if sel_track != None:
            found_recording_clip = False
            song = self.song()
            tracks = song.tracks
            check_arrangement = song.is_playing and song.record_mode
            for track in tracks:
                if track.can_be_armed and track.arm:
                    if check_arrangement:
                        found_recording_clip = True
                        break
                    else:
                        playing_slot_index = track.playing_slot_index
                        if playing_slot_index in range(len(track.clip_slots)):
                            slot = track.clip_slots[playing_slot_index]
                            if slot.has_clip and slot.clip.is_recording:
                                found_recording_clip = True
                                break

            if not found_recording_clip:
                if song.exclusive_arm:
                    for track in tracks:
                        if track.can_be_armed and track.arm and track != sel_track:
                            track.arm = False

                sel_track.arm = True
                sel_track.view.select_instrument()
        self._selected_tracks = []
        return

    def _next_track_value(self, value):
        MixerComponent._next_track_value(self, value)
        self._selected_tracks.append(self.song().view.selected_track)

    def _prev_track_value(self, value):
        MixerComponent._prev_track_value(self, value)
        self._selected_tracks.append(self.song().view.selected_track)