# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/RemoteSL/RemoteSLComponent.py
# Compiled at: 2019-04-09 19:23:45
from __future__ import absolute_import, print_function, unicode_literals
from .consts import *

class RemoteSLComponent:
    u"""Baseclass for a subcomponent of the RemoteSL.
    Just defines some handy shortcuts to the main scripts functions...
    for more details about the methods, see the RemoteSLs doc strings
    """

    def __init__(self, remote_sl_parent):
        self.__parent = remote_sl_parent
        self.__support_mkII = False

    def application(self):
        return self.__parent.application()

    def song(self):
        return self.__parent.song()

    def send_midi(self, midi_event_bytes):
        self.__parent.send_midi(midi_event_bytes)

    def request_rebuild_midi_map(self):
        self.__parent.request_rebuild_midi_map()

    def disconnect(self):
        pass

    def build_midi_map(self, script_handle, midi_map_handle):
        pass

    def refresh_state(self):
        pass

    def update_display(self):
        pass

    def cc_status_byte(self):
        return CC_STATUS + SL_MIDI_CHANNEL

    def support_mkII(self):
        return self.__support_mkII

    def set_support_mkII(self, support_mkII):
        self.__support_mkII = support_mkII