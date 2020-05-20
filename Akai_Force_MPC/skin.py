#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Akai_Force_MPC/skin.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.elements import Color
LIVE_COLOR_TABLE_INDEX_OFFSET = 8
ON_COLOR = Color(127)
OFF_COLOR = Color(0)

class ColorsBase:

    class DefaultButton:
        On = ON_COLOR
        Off = OFF_COLOR
        Disabled = OFF_COLOR

    class Mixer:
        SoloOn = Color(2)
        SoloOff = OFF_COLOR
        MuteOn = Color(1)
        MuteOff = OFF_COLOR
        ArmOff = OFF_COLOR
        CrossfadeAssignA = Color(1)
        CrossfadeAssignB = Color(3)

    class Session:
        RecordButton = ON_COLOR
        ClipTriggeredPlay = Color(3)
        ClipTriggeredRecord = Color(6)
        ClipStarted = Color(4)
        ClipRecording = Color(7)
        ClipStopped = Color(2)
        ClipSelected = Color(127)
        Scene = Color(0)
        SceneTriggered = Color(1)
        NoScene = OFF_COLOR
        StopClipTriggered = ON_COLOR
        StopClip = Color(4)
        StopClipDisabled = OFF_COLOR
        ClipEmpty = OFF_COLOR
        ClipEmptyWithStopButton = Color(1)
        SceneOff = OFF_COLOR
        SceneOn = Color(2)
        SceneDefault = Color(21)

    class Action:
        Available = OFF_COLOR
        On = Color(1)
        Off = Color(0)
        QuantizeOn = Color(5)
        QuantizeOff = Color(0)

    class Transport:
        PlayOn = ON_COLOR
        PlayOff = OFF_COLOR
        StopOn = ON_COLOR
        StopOff = OFF_COLOR
        MetronomeOn = Color(6)
        MetronomeOff = Color(0)
        TapTempo = Color(1)

    class Recording:
        On = ON_COLOR
        Off = OFF_COLOR
        Transition = ON_COLOR

    class Automation:
        On = Color(2)
        Off = OFF_COLOR

    class Navigation:
        Enabled = Color(1)

    class Background:
        On = Color(1)

    class Mode:
        On = Color(1)
        Off = OFF_COLOR


class ForceColors(ColorsBase):

    class Mixer(ColorsBase.Mixer):
        ArmOn = Color(3)


class MPCColors(ColorsBase):

    class Mixer(ColorsBase.Mixer):
        ArmOn = Color(1)
