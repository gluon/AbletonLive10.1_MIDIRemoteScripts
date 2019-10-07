# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_MxDCore/MxDUtils.py
# Compiled at: 2019-05-08 17:06:57
from __future__ import absolute_import, print_function, unicode_literals
import logging
logger = logging.getLogger(__name__)

class TupleWrapper(object):
    u""" Wrapper class for the access to volatile lists and tuples in the Python API """
    _tuple_wrapper_registry = {}

    def forget_tuple_wrapper_instances():
        TupleWrapper._tuple_wrapper_registry = {}

    forget_tuple_wrapper_instances = staticmethod(forget_tuple_wrapper_instances)

    def get_tuple_wrapper(parent, attribute, element_filter=None):
        if (parent, attribute) not in TupleWrapper._tuple_wrapper_registry:
            TupleWrapper._tuple_wrapper_registry[(parent, attribute)] = TupleWrapper(parent, attribute, element_filter)
        return TupleWrapper._tuple_wrapper_registry[(parent, attribute)]

    get_tuple_wrapper = staticmethod(get_tuple_wrapper)

    def __init__(self, parent, attribute, element_filter=None):
        assert isinstance(attribute, (str, unicode))
        self._parent = parent
        self._attribute = attribute
        self._element_filter = element_filter

    def get_list(self):
        result = ()
        parent = self._parent
        if parent == None:
            parent = __builtins__
        if isinstance(parent, dict):
            if self._attribute in parent.keys():
                result = parent[self._attribute]
        elif hasattr(parent, self._attribute):
            result = getattr(parent, self._attribute)
        if self._element_filter:
            return [ e if self._element_filter(e) else None for e in result ]
        else:
            return result


STATE_NEUTRAL = 'neutral'
STATE_QUOTED_STR = 'quoted'
STATE_UNQUOTED_STR = 'unquoted'
STATE_PENDING_NR = 'number'
STATE_PENDING_FLOAT = 'float'
QUOTE_ENTITY = '&quot;'
QUOTE_SIMPLE = '"'

class StringHandler(object):
    u""" Class that can parse incoming strings and format outgoing strings """

    def prepare_incoming(string):
        assert isinstance(string, (str, unicode))
        return string.replace(QUOTE_ENTITY, QUOTE_SIMPLE)

    prepare_incoming = staticmethod(prepare_incoming)

    def prepare_outgoing(string):
        assert isinstance(string, (str, unicode))
        result = string.replace(QUOTE_SIMPLE, QUOTE_ENTITY)
        if result.find(' ') >= 0:
            result = QUOTE_SIMPLE + result + QUOTE_SIMPLE
        return result

    prepare_outgoing = staticmethod(prepare_outgoing)

    def parse(string, id_callback):
        assert isinstance(string, (str, unicode))
        return StringHandler(id_callback).parse_string(string)

    parse = staticmethod(parse)

    def __init__(self, id_callback):
        self._state = STATE_NEUTRAL
        self._sub_string = ''
        self._open_quote_index = -1
        self._id_callback = id_callback

    def parse_string(self, string):
        self._arguments = []
        self._sub_string = ''
        self._state = STATE_NEUTRAL
        self._open_quote_index = -1
        for index in range(len(string)):
            char = string[index]
            handle_selector = '_' + str(self._state) + '_handle_char'
            if hasattr(self, handle_selector):
                getattr(self, handle_selector)(char, index)
            else:
                logger.info('Unknown state ' + str(self._state))
                assert False

        finalize_selector = '_finalize_' + str(self._state)
        if len(self._sub_string) > 0 and hasattr(self, finalize_selector):
            getattr(self, finalize_selector)()
        return self._arguments

    def _neutral_handle_char(self, char, index):
        if char == '"':
            self._open_quote_index = index
            self._state = STATE_QUOTED_STR
        elif char != ' ':
            self._sub_string += char
            if unicode(char).isdigit():
                self._state = STATE_PENDING_NR
            else:
                self._state = STATE_UNQUOTED_STR

    def _number_handle_char(self, char, index):
        if char == ' ':
            if len(self._sub_string) > 0:
                self._finalize_number()
            else:
                self._state = STATE_NEUTRAL
        else:
            if char == '.':
                self._state = STATE_PENDING_FLOAT
            elif not unicode(char).isdigit():
                self._state = STATE_UNQUOTED_STR
            self._sub_string += char

    def _float_handle_char(self, char, index):
        if char == ' ':
            self._add_argument(float(self._sub_string))
        else:
            if char in (u'.', u'e', u'E'):
                if char in self._sub_string:
                    self._state = STATE_UNQUOTED_STR
            elif not unicode(char).isdigit():
                self._state = STATE_UNQUOTED_STR
            self._sub_string += char

    def _unquoted_handle_char(self, char, index):
        if char == ' ':
            self._add_argument(self._sub_string)
        elif unicode(char).isdigit():
            if self._sub_string == '-':
                self._state = STATE_PENDING_NR
            elif self._sub_string in (u'.', u'-.'):
                self._state = STATE_PENDING_FLOAT
        else:
            self._sub_string += char

    def _quoted_handle_char(self, char, index):
        if char == '"':
            self._open_quote_index = -1
            self._add_argument(self._sub_string)
        else:
            self._sub_string += char

    def _finalize_quoted(self):
        raise RuntimeError('no match for quote at index %d found' % self._open_quote_index)

    def _finalize_unquoted(self):
        self._add_argument(self._sub_string)

    def _finalize_float(self):
        self._add_argument(float(self._sub_string))

    def _finalize_number(self):
        argument = int(self._sub_string)
        if cmp(unicode(self._arguments[(-1)]), 'id') == 0:
            self._arguments.pop()
            try:
                argument = self._id_callback(argument)
            except KeyError:
                raise RuntimeError('Invalid id')

        self._add_argument(argument)

    def _add_argument(self, argument):
        if isinstance(argument, (str, unicode)):
            argument = StringHandler.prepare_incoming(argument)
        self._arguments.append(argument)
        self._sub_string = ''
        self._state = STATE_NEUTRAL