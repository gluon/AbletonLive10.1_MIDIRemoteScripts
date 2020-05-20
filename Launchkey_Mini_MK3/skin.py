#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchkey_Mini_MK3/skin.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import merge_skins, Skin
from novation.colors import Mono, Rgb
from novation.skin import skin as base_skin

class Colors:

    class Recording:
        On = Mono.ON
        Off = Mono.OFF

    class TrackNavigation:
        On = Mono.HALF
        Pressed = Mono.ON

    class SceneNavigation:
        On = Mono.HALF
        Pressed = Mono.ON

    class DrumGroup:
        PadSelected = Rgb.WHITE
        PadSelectedNotSoloed = Rgb.WHITE
        PadMutedSelected = Rgb.WHITE
        PadSoloedSelected = Rgb.WHITE
        Navigation = Rgb.WHITE_HALF
        NavigationPressed = Rgb.WHITE


skin = merge_skins(*(base_skin, Skin(Colors)))
