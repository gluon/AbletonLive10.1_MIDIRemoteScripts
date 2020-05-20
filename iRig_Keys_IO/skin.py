#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/iRig_Keys_IO/skin.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin
from ableton.v2.control_surface.elements import Color

class Colors:

    class DefaultButton:
        On = Color(0)
        Off = Color(0)
        Disabled = Color(0)

    class Transport:
        PlayOn = Color(0)
        PlayOff = Color(0)

    class Recording:
        On = Color(0)
        Off = Color(0)

    class Mixer:
        MuteOff = Color(127)
        MuteOn = Color(0)
        SoloOn = Color(127)
        SoloOff = Color(0)


skin = Skin(Colors)
