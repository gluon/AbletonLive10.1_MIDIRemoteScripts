#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Axiom_AIR_25_49_61/NumericalDisplayElement.py
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement
from .NumericalDisplaySegment import NumericalDisplaySegment

class NumericalDisplayElement(PhysicalDisplayElement):
    u""" Special display element that only displays numerical values """
    _ascii_translations = {u'0': 48,
     u'1': 49,
     u'2': 50,
     u'3': 51,
     u'4': 52,
     u'5': 53,
     u'6': 54,
     u'7': 55,
     u'8': 56,
     u'9': 57}

    def __init__(self, width_in_chars, num_segments):
        PhysicalDisplayElement.__init__(self, width_in_chars, num_segments)
        self._logical_segments = []
        self._translation_table = NumericalDisplayElement._ascii_translations
        width_without_delimiters = self._width - num_segments + 1
        width_per_segment = int(width_without_delimiters / num_segments)
        for index in range(num_segments):
            new_segment = NumericalDisplaySegment(width_per_segment, self.update)
            self._logical_segments.append(new_segment)

    def display_message(self, message):
        assert self._message_header != None
        assert message != None
        assert isinstance(message, str)
        if not self._block_messages:
            message = NumericalDisplaySegment.adjust_string(message, self._width)
            self.send_midi(self._message_header + tuple([ self._translate_char(c) for c in message ]) + self._message_tail)

    def _translate_char(self, char_to_translate):
        assert char_to_translate != None
        assert isinstance(char_to_translate, str) or isinstance(char_to_translate, unicode)
        assert len(char_to_translate) == 1
        if char_to_translate in self._translation_table.keys():
            result = self._translation_table[char_to_translate]
        else:
            result = self._translation_table[u'0']
        return result
