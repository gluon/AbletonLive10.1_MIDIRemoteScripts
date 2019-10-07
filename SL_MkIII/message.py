# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/SL_MkIII/message.py
# Compiled at: 2019-04-23 14:43:03
from __future__ import absolute_import, print_function, unicode_literals
from itertools import izip
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import TextDisplayControl
NUM_MESSAGE_SEGMENTS = 2

class MessageComponent(Component):
    display = TextDisplayControl(segments=(u'', ) * NUM_MESSAGE_SEGMENTS)

    def __call__(self, *messages):
        for index, message in izip(xrange(NUM_MESSAGE_SEGMENTS), messages):
            self.display[index] = message if message else ''