# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/MPD232/MPD232.py
# Compiled at: 2019-04-09 19:23:44
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _MPDMkIIBase.MPDMkIIBase import MPDMkIIBase
from _MPDMkIIBase.ControlElementUtils import make_button, make_encoder, make_slider
PAD_CHANNEL = 1
PAD_IDS = [
 [
  81, 83, 84, 86],
 [
  74, 76, 77, 79],
 [
  67, 69, 71, 72],
 [
  60, 62, 64, 65]]

class MPD232(MPDMkIIBase):

    def __init__(self, *a, **k):
        super(MPD232, self).__init__(PAD_IDS, PAD_CHANNEL, *a, **k)
        with self.component_guard():
            self._create_device()
            self._create_transport()
            self._create_mixer()

    def _create_controls(self):
        self._create_pads()
        self._encoders = ButtonMatrixElement(rows=[
         [ make_encoder(identifier, 0, 'Encoder_%d' % index) for index, identifier in enumerate(xrange(22, 30))
         ]])
        self._sliders = ButtonMatrixElement(rows=[
         [ make_slider(identifier, 0, 'Slider_%d' % index) for index, identifier in enumerate(xrange(12, 20))
         ]])
        self._control_buttons = ButtonMatrixElement(rows=[
         [ make_button(identifier, 0, 'Control_Button_%d' % index) for index, identifier in enumerate(xrange(32, 40))
         ]])
        self._play_button = make_button(118, 0, 'Play_Button')
        self._stop_button = make_button(117, 0, 'Stop_Button')
        self._record_button = make_button(119, 0, 'Record_Button')