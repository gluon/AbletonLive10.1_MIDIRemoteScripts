# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/view_control.py
# Compiled at: 2019-04-23 14:43:03
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import EventObject, ObservablePropertyAlias, clamp, index_if, listens
from ableton.v2.control_surface.components import BasicSceneScroller, BasicTrackScroller, ScrollComponent, ViewControlComponent, all_tracks

class NotifyingTrackScroller(BasicTrackScroller, EventObject):
    __events__ = (u'scrolled', )

    def _do_scroll(self, delta):
        super(NotifyingTrackScroller, self)._do_scroll(delta)
        self.notify_scrolled()


class NotifyingTrackPager(NotifyingTrackScroller):

    def __init__(self, track_provider=None, *a, **k):
        super(NotifyingTrackPager, self).__init__(*a, **k)
        assert track_provider is not None
        self._track_provider = track_provider
        return

    def _do_scroll(self, delta):
        selected_track = self._song.view.selected_track
        tracks = all_tracks(self._song)
        selected_track_index = index_if(lambda t: t == selected_track, tracks)
        len_tracks = len(tracks)
        new_index = selected_track_index + delta * self._track_provider.num_tracks
        self._song.view.selected_track = tracks[clamp(new_index, 0, len_tracks - 1)]
        self.notify_scrolled()


class NotifyingViewControlComponent(ViewControlComponent):
    __events__ = (u'selection_scrolled', u'selection_paged')

    def __init__(self, track_provider=None, *a, **k):
        self._track_provider = track_provider
        super(NotifyingViewControlComponent, self).__init__(*a, **k)
        self._page_tracks = ScrollComponent(self._create_track_pager(), parent=self)
        self.__on_tracks_changed.subject = self._track_provider
        self.__on_selected_track_changed.subject = self.song.view
        self._page_tracks.scroll_up_button.color = 'TrackNavigation.On'
        self._page_tracks.scroll_down_button.color = 'TrackNavigation.On'
        self._scroll_tracks.scroll_up_button.color = 'TrackNavigation.On'
        self._scroll_tracks.scroll_down_button.color = 'TrackNavigation.On'
        self._scroll_scenes.scroll_up_button.color = 'SceneNavigation.On'
        self._scroll_scenes.scroll_down_button.color = 'SceneNavigation.On'

    def set_prev_track_page_button(self, button):
        self._page_tracks.set_scroll_up_button(button)

    def set_next_track_page_button(self, button):
        self._page_tracks.set_scroll_down_button(button)

    def _create_track_scroller(self):
        scroller = NotifyingTrackScroller()
        self.register_disconnectable(ObservablePropertyAlias(self, property_host=scroller, property_name='scrolled', alias_name='selection_scrolled'))
        return scroller

    def _create_scene_scroller(self):
        return BasicSceneScroller()

    def _create_track_pager(self):
        pager = NotifyingTrackPager(track_provider=self._track_provider)
        self.register_disconnectable(ObservablePropertyAlias(self, property_host=pager, property_name='scrolled', alias_name='selection_paged'))
        return pager

    @listens('tracks')
    def __on_tracks_changed(self):
        self._update_track_scrollers()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        self._update_track_scrollers()

    def _update_track_scrollers(self):
        self._scroll_tracks.update()
        self._page_tracks.update()