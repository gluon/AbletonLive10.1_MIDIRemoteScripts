# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/BLOCKS/target_track_provider.py
# Compiled at: 2019-04-09 19:23:44
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens, listens_group
from ableton.v2.control_surface import Component

class TargetTrackProvider(Component):
    __events__ = (u'target_track', u'armed_tracks')

    def __init__(self, *a, **k):
        super(TargetTrackProvider, self).__init__(*a, **k)
        self._target_track = None
        self._armed_tracks = []
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_tracks_changed.subject = self.song
        self.__on_tracks_changed()
        return

    @property
    def target_track(self):
        return self._target_track

    @listens('selected_track')
    def __on_selected_track_changed(self):
        if not self._armed_tracks:
            self._update_target_track()

    @listens('tracks')
    def __on_tracks_changed(self):
        tracks = filter(lambda t: t.can_be_armed and t.has_midi_input, self.song.tracks)
        self.__on_arm_changed.replace_subjects(tracks)
        self.__on_frozen_state_changed.replace_subjects(tracks)
        self._update_tracks(tracks)

    @listens_group('arm')
    def __on_arm_changed(self, track):
        if track in self._armed_tracks:
            self._armed_tracks.remove(track)
        if track.arm:
            self._armed_tracks.append(track)
            self._set_target_track(track)
        else:
            self._update_target_track()
        self.notify_armed_tracks()

    @listens_group('is_frozen')
    def __on_frozen_state_changed(self, track):
        if track in self._armed_tracks:
            self._armed_tracks.remove(track)
        self._update_target_track()

    def _update_tracks(self, all_tracks):
        for track in self._armed_tracks:
            if track not in all_tracks:
                self._armed_tracks.remove(track)

        for track in all_tracks:
            if track.arm and track not in self._armed_tracks:
                self._armed_tracks.append(track)

        self._update_target_track()

    def _update_target_track(self):
        target_track = None
        selected_track = self.song.view.selected_track
        if self._armed_tracks:
            target_track = self._armed_tracks[(-1)]
        elif not selected_track.is_frozen:
            target_track = selected_track
        self._set_target_track(target_track)
        return

    def _set_target_track(self, track):
        if self._target_track != track:
            self._target_track = track
            self.notify_target_track()