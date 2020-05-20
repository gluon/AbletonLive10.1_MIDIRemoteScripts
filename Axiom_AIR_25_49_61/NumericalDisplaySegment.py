#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Axiom_AIR_25_49_61/NumericalDisplaySegment.py
from __future__ import absolute_import, print_function, unicode_literals
from _Framework.LogicalDisplaySegment import LogicalDisplaySegment

class NumericalDisplaySegment(LogicalDisplaySegment):
    u""" Special display segment that only displays numerical values """

    @staticmethod
    def adjust_string(original, length):
        characters_to_retain = {u'0': 48,
         u'1': 49,
         u'2': 50,
         u'3': 51,
         u'4': 52,
         u'5': 53,
         u'6': 54,
         u'7': 55,
         u'8': 56,
         u'9': 57}
        resulting_string = u''
        for char in original:
            if char in characters_to_retain:
                resulting_string = resulting_string + char

        if len(resulting_string) > length:
            resulting_string = resulting_string[:length]
        if len(resulting_string) < length:
            resulting_string = resulting_string.rjust(length)
        return resulting_string

    def __init__(self, width, update_callback):
        LogicalDisplaySegment.__init__(self, width, update_callback)

    def display_string(self):
        resulting_string = u' ' * self._width
        if self._data_source != None:
            resulting_string = NumericalDisplaySegment.adjust_string(self._data_source.display_string(), self._width)
        return resulting_string
