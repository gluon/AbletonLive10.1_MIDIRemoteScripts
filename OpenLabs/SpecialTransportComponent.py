# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/OpenLabs/SpecialTransportComponent.py
# Compiled at: 2019-04-09 19:23:44
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.TransportComponent import TransportComponent
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement

class SpecialTransportComponent(TransportComponent):
    u""" Transport component that takes buttons for Undo and Redo """

    def __init__(self):
        TransportComponent.__init__(self)
        self._undo_button = None
        self._redo_button = None
        self._bts_button = None
        return

    def disconnect(self):
        TransportComponent.disconnect(self)
        if self._undo_button != None:
            self._undo_button.remove_value_listener(self._undo_value)
            self._undo_button = None
        if self._redo_button != None:
            self._redo_button.remove_value_listener(self._redo_value)
            self._redo_button = None
        if self._bts_button != None:
            self._bts_button.remove_value_listener(self._bts_value)
            self._bts_button = None
        return

    def set_undo_button(self, undo_button):
        assert isinstance(undo_button, (ButtonElement, type(None)))
        if undo_button != self._undo_button:
            if self._undo_button != None:
                self._undo_button.remove_value_listener(self._undo_value)
            self._undo_button = undo_button
            if self._undo_button != None:
                self._undo_button.add_value_listener(self._undo_value)
            self.update()
        return

    def set_redo_button(self, redo_button):
        assert isinstance(redo_button, (ButtonElement, type(None)))
        if redo_button != self._redo_button:
            if self._redo_button != None:
                self._redo_button.remove_value_listener(self._redo_value)
            self._redo_button = redo_button
            if self._redo_button != None:
                self._redo_button.add_value_listener(self._redo_value)
            self.update()
        return

    def set_bts_button(self, bts_button):
        assert isinstance(bts_button, (ButtonElement, type(None)))
        if bts_button != self._bts_button:
            if self._bts_button != None:
                self._bts_button.remove_value_listener(self._bts_value)
            self._bts_button = bts_button
            if self._bts_button != None:
                self._bts_button.add_value_listener(self._bts_value)
            self.update()
        return

    def _undo_value(self, value):
        if not self._undo_button != None:
            raise AssertionError
            assert value in range(128)
            if self.is_enabled() and (value != 0 or not self._undo_button.is_momentary()):
                if self.song().can_undo:
                    self.song().undo()
        return

    def _redo_value(self, value):
        if not self._redo_button != None:
            raise AssertionError
            assert value in range(128)
            if self.is_enabled() and (value != 0 or not self._redo_button.is_momentary()):
                if self.song().can_redo:
                    self.song().redo()
        return

    def _bts_value(self, value):
        if not self._bts_button != None:
            raise AssertionError
            assert value in range(128)
            if self.is_enabled() and (value != 0 or not self._bts_button.is_momentary()):
                self.song().current_song_time = 0.0
        return