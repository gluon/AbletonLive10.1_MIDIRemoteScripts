# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/components/transport.py
# Compiled at: 2019-05-15 02:17:17
from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
import Live
from ...base import in_range, clamp, listens, task
from ..component import Component
from ..control import ToggleButtonControl, ButtonControl
from .toggle import ToggleComponent
TEMPO_TOP = 200.0
TEMPO_BOTTOM = 60.0
TEMPO_FINE_RANGE = 2.56
SEEK_SPEED = 10.0

class TransportComponent(Component):
    u"""
    Class encapsulating all functions in Live's transport section.
    """
    _play_toggle = ToggleButtonControl(toggled_color='Transport.PlayOn', untoggled_color='Transport.PlayOff')
    _stop_button = ButtonControl()

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self._ffwd_button = None
        self._rwd_button = None
        self._tap_tempo_button = None
        self._tempo_control = None
        self._tempo_fine_control = None
        self._rwd_task = task.Task()
        self._ffwd_task = task.Task()
        self._fine_tempo_needs_pickup = True
        self._prior_fine_tempo_value = -1
        self._end_undo_step_task = self._tasks.add(task.sequence(task.wait(1.5), task.run(self.song.end_undo_step)))
        self._end_undo_step_task.kill()
        song = self.song
        self._loop_toggle = ToggleComponent('loop', song, parent=self)
        self._punch_in_toggle = ToggleComponent('punch_in', song, is_momentary=True, parent=self)
        self._punch_out_toggle = ToggleComponent('punch_out', song, is_momentary=True, parent=self)
        self._record_toggle = ToggleComponent('record_mode', song, parent=self)
        self._nudge_down_toggle = ToggleComponent('nudge_down', song, is_momentary=True, parent=self)
        self._nudge_up_toggle = ToggleComponent('nudge_up', song, is_momentary=True, parent=self)
        self._metronome_toggle = ToggleComponent('metronome', song, parent=self)
        self._arrangement_overdub_toggle = ToggleComponent('arrangement_overdub', song, parent=self)
        self._overdub_toggle = ToggleComponent('overdub', song, parent=self)
        self.__on_is_playing_changed.subject = song
        self.__on_is_playing_changed()
        return

    @listens('is_playing')
    def __on_is_playing_changed(self):
        self._update_button_states()

    def _update_button_states(self):
        self._play_toggle.is_toggled = self.song.is_playing
        self._update_stop_button_color()

    def _update_stop_button_color(self):
        self._stop_button.color = self._play_toggle.toggled_color if self._play_toggle.is_toggled else self._play_toggle.untoggled_color

    @_stop_button.released
    def _on_stop_button_released(self, button):
        self.song.is_playing = False

    def set_stop_button(self, button):
        self._update_stop_button_color()
        self._stop_button.set_control_element(button)

    @_play_toggle.toggled
    def _on_play_button_toggled(self, is_toggled, button):
        self.song.is_playing = is_toggled

    def set_play_button(self, button):
        self._play_toggle.set_control_element(button)

    def set_seek_buttons(self, ffwd_button, rwd_button):
        if self._ffwd_button != ffwd_button:
            self._ffwd_button = ffwd_button
            self.__ffwd_value_slot.subject = ffwd_button
            self._ffwd_task.kill()
        if self._rwd_button != rwd_button:
            self._rwd_button = rwd_button
            self.__rwd_value_slot.subject = rwd_button
            self._rwd_task.kill()

    def set_seek_forward_button(self, ffwd_button):
        if self._ffwd_button != ffwd_button:
            self._ffwd_button = ffwd_button
            self.__ffwd_value_slot.subject = ffwd_button
            self._ffwd_task.kill()

    def set_seek_backward_button(self, rwd_button):
        if self._rwd_button != rwd_button:
            self._rwd_button = rwd_button
            self.__rwd_value_slot.subject = rwd_button
            self._rwd_task.kill()

    def set_nudge_buttons(self, up_button, down_button):
        self._nudge_up_toggle.set_toggle_button(up_button)
        self._nudge_down_toggle.set_toggle_button(down_button)

    def set_nudge_up_button(self, up_button):
        self._nudge_up_toggle.set_toggle_button(up_button)

    def set_nudge_down_button(self, down_button):
        self._nudge_down_toggle.set_toggle_button(down_button)

    def set_record_button(self, button):
        self._record_toggle.set_toggle_button(button)

    def set_tap_tempo_button(self, button):
        if self._tap_tempo_button != button:
            self._tap_tempo_button = button
            self.__tap_tempo_value.subject = button
            self._update_tap_tempo_button()

    def set_loop_button(self, button):
        self._loop_toggle.set_toggle_button(button)

    def set_punch_in_button(self, in_button):
        self._punch_in_toggle.set_toggle_button(in_button)

    def set_punch_out_button(self, out_button):
        self._punch_out_toggle.set_toggle_button(out_button)

    def set_metronome_button(self, button):
        self._metronome_toggle.set_toggle_button(button)

    def set_arrangement_overdub_button(self, button):
        self._arrangement_overdub_toggle.set_toggle_button(button)

    def set_overdub_button(self, button):
        self._overdub_toggle.set_toggle_button(button)

    def set_tempo_control(self, control, fine_control=None):
        assert not control or control.message_map_mode() is Live.MidiMap.MapMode.absolute
        assert not fine_control or fine_control.message_map_mode() is Live.MidiMap.MapMode.absolute
        if self._tempo_control != control:
            self._tempo_control = control
            self.__tempo_value.subject = control
        if self._tempo_fine_control != fine_control:
            self._tempo_fine_control = fine_control
            self.__tempo_fine_value.subject = fine_control
            self._fine_tempo_needs_pickup = True
            self._prior_fine_tempo_value = -1

    def set_tempo_fine_control(self, fine_control):
        assert not fine_control or fine_control.message_map_mode() is Live.MidiMap.MapMode.absolute
        if self._tempo_fine_control != fine_control:
            self._tempo_fine_control = fine_control
            self.__tempo_fine_value.subject = fine_control
            self._fine_tempo_needs_pickup = True
            self._prior_fine_tempo_value = -1

    def update(self):
        super(TransportComponent, self).update()
        if self.is_enabled():
            self._update_tap_tempo_button()

    @listens('value')
    def __ffwd_value_slot(self, value):
        self._ffwd_value(value)

    def _ffwd_value(self, value):
        if self._ffwd_button.is_momentary():
            self._ffwd_task.kill()
            if value:
                self._ffwd_task = self._tasks.add(partial(self._move_current_song_time, SEEK_SPEED))
        elif self.is_enabled():
            self.song.current_song_time += 1

    @listens('value')
    def __rwd_value_slot(self, value):
        self._rwd_value(value)

    def _rwd_value(self, value):
        if self._rwd_button.is_momentary():
            self._rwd_task.kill()
            if value:
                self._rwd_task = self._tasks.add(partial(self._move_current_song_time, -SEEK_SPEED))
        elif self.is_enabled():
            song = self.song
            song.current_song_time = max(0.0, song.current_song_time - 1)

    def _move_current_song_time(self, speed, delta):
        song = self.song
        song.current_song_time = max(0.0, song.current_song_time + speed * delta)
        return task.RUNNING

    @listens('value')
    def __tap_tempo_value(self, value):
        if self.is_enabled():
            if value or not self._tap_tempo_button.is_momentary():
                if not self._end_undo_step_task.is_running:
                    self.song.begin_undo_step()
                self._end_undo_step_task.restart()
                self.song.tap_tempo()
            self._update_tap_tempo_button()

    def _update_tap_tempo_button(self):
        if self.is_enabled() and self._tap_tempo_button:
            self._tap_tempo_button.set_light(True)

    @listens('value')
    def __tempo_value(self, value):
        if self.is_enabled():
            fraction = (TEMPO_TOP - TEMPO_BOTTOM) / 127.0
            self.song.tempo = fraction * value + TEMPO_BOTTOM

    @listens('value')
    def __tempo_fine_value(self, value):
        if self.is_enabled():
            if self._fine_tempo_needs_pickup:
                if in_range(self._prior_fine_tempo_value, 0, 128):
                    range_max = max(value, self._prior_fine_tempo_value)
                    range_min = min(value, self._prior_fine_tempo_value)
                    if in_range(64, range_min, range_max + 1):
                        self._fine_tempo_needs_pickup = False
            else:
                assert in_range(self._prior_fine_tempo_value, 0, 128)
                difference = value - self._prior_fine_tempo_value
                ratio = 127.0 / TEMPO_FINE_RANGE
                new_tempo = clamp(self.song.tempo + difference / ratio, TEMPO_BOTTOM, TEMPO_TOP)
                self.song.tempo = new_tempo
        self._prior_fine_tempo_value = value