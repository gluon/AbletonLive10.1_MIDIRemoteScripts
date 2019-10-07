# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchkey/SpecialMixerComponent.py
# Compiled at: 2019-04-09 19:23:44
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.MixerComponent import MixerComponent

class SpecialMixerComponent(MixerComponent):
    u""" Special mixer class that toggles given buttons between mute and solo """

    def __init__(self, num_tracks):
        MixerComponent.__init__(self, num_tracks)
        self._strip_mute_solo_buttons = None
        self._mute_solo_flip_button = None
        self._mute_solo_is_flipped = False
        return

    def disconnect(self):
        MixerComponent.disconnect(self)
        if self._mute_solo_flip_button != None:
            self._mute_solo_flip_button.remove_value_listener(self._mute_solo_flip_value)
            self._mute_solo_flip_button = None
        self._strip_mute_solo_buttons = None
        return

    def tracks_to_use(self):
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    def set_strip_mute_solo_buttons(self, buttons, flip_button):
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

    def _mute_solo_flip_value(self, value):
        if self._strip_mute_solo_buttons != None:
            if value == 0:
                self._mute_solo_is_flipped = not self._mute_solo_is_flipped
                self._mute_solo_flip_button.turn_on() if self._mute_solo_is_flipped else self._mute_solo_flip_button.turn_off()
                for index in range(len(self._strip_mute_solo_buttons)):
                    strip = self.channel_strip(index)
                    if self._mute_solo_is_flipped:
                        strip.set_mute_button(None)
                        strip.set_solo_button(self._strip_mute_solo_buttons[index])
                    else:
                        strip.set_solo_button(None)
                        strip.set_mute_button(self._strip_mute_solo_buttons[index])

        return