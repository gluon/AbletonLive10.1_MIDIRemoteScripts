# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Komplete_Kontrol/channel_strip_component.py
# Compiled at: 2019-05-08 17:06:57
from __future__ import absolute_import, print_function, unicode_literals
import re
from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from ableton.v2.control_surface.elements import DisplayDataSource
from ableton.v2.control_surface.control import SendValueControl
from .sysex import DEFAULT_TRACK_TYPE_VALUE, EMPTY_TRACK_TYPE_VALUE, MASTER_TRACK_TYPE_VALUE
volume_pattern = re.compile('-*\\d+.\\d+')

class ChannelStripComponent(ChannelStripComponentBase):
    track_type_display = SendValueControl()
    track_selection_display = SendValueControl()
    track_mute_display = SendValueControl()
    track_solo_display = SendValueControl()
    track_muted_via_solo_display = SendValueControl()

    def __init__(self, *a, **k):
        super(ChannelStripComponent, self).__init__(*a, **k)
        self._track_volume_data_source = DisplayDataSource()
        self._track_panning_data_source = DisplayDataSource()
        self.__on_selected_track_changed.subject = self.song.view

    @property
    def track_volume_data_source(self):
        return self._track_volume_data_source

    @property
    def track_panning_data_source(self):
        return self._track_panning_data_source

    def set_track(self, track):
        super(ChannelStripComponent, self).set_track(track)
        track = track if liveobj_valid(track) else None
        mixer = track.mixer_device if track else None
        self.__on_muted_via_solo_changed.subject = track
        self.__on_volume_value_changed.subject = mixer.volume if mixer else None
        self.__on_panning_value_changed.subject = mixer.panning if mixer else None
        self._update_track_volume_data_source()
        self._update_track_panning_data_source()
        self._update_track_type_display()
        self.__on_muted_via_solo_changed()
        return

    def _on_mute_changed(self):
        super(ChannelStripComponent, self)._on_mute_changed()
        self.track_mute_display.value = int(self._track.mute) if liveobj_valid(self._track) and self._track != self.song.master_track else 0

    def _on_solo_changed(self):
        super(ChannelStripComponent, self)._on_solo_changed()
        self.track_solo_display.value = int(self._track.solo) if liveobj_valid(self._track) and self._track != self.song.master_track else 0

    @listens('selected_track')
    def __on_selected_track_changed(self):
        selected_track = self.song.view.selected_track
        self.track_selection_display.value = int(self._track == selected_track) if liveobj_valid(self._track) else 0

    @listens('muted_via_solo')
    def __on_muted_via_solo_changed(self):
        self.track_muted_via_solo_display.value = int(self._track.muted_via_solo) if liveobj_valid(self._track) and self._track != self.song.master_track else 0

    @listens('value')
    def __on_volume_value_changed(self):
        self._update_track_volume_data_source()

    @listens('value')
    def __on_panning_value_changed(self):
        self._update_track_panning_data_source()

    def _update_track_volume_data_source(self):
        volume_string = ''
        if liveobj_valid(self._track):
            volume_string = str(self._track.mixer_device.volume)
            found_string = ('').join(volume_pattern.findall(volume_string))
            if found_string:
                volume_string = '%s dB' % round(float(found_string), 1)
        self._track_volume_data_source.set_display_string(volume_string)

    def _update_track_panning_data_source(self):
        pan_string = ''
        if liveobj_valid(self._track):
            pan_string = str(self._track.mixer_device.panning)
        self._track_panning_data_source.set_display_string(pan_string)

    def _update_track_type_display(self):
        value_to_send = EMPTY_TRACK_TYPE_VALUE
        if liveobj_valid(self._track):
            value_to_send = DEFAULT_TRACK_TYPE_VALUE
            if self._track == self.song.master_track:
                value_to_send = MASTER_TRACK_TYPE_VALUE
        self.track_type_display.value = value_to_send