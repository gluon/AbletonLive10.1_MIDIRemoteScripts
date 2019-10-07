# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_MxDCore/__init__.py
# Compiled at: 2019-04-09 19:23:45
from __future__ import absolute_import, print_function, unicode_literals
from .MxDCore import MxDCore as _MxDCore
import sys, warnings

def set_manager(manager):
    assert manager != None
    assert _MxDCore.instance == None
    _MxDCore.instance = _MxDCore()
    _MxDCore.instance.set_manager(manager)
    return


def disconnect():
    _MxDCore.instance.disconnect()
    del _MxDCore.instance


def execute_command(device_id, object_id, command, arguments):
    assert _MxDCore.instance != None
    assert isinstance(arguments, (str, unicode))
    if hasattr(_MxDCore.instance, command):
        try:
            with warnings.catch_warnings(record=True) as (caught_warnings):
                _MxDCore.instance.update_device_context(device_id, object_id)
                function = getattr(_MxDCore.instance, command)
                function(device_id, object_id, arguments)
                for warning in caught_warnings:
                    _MxDCore.instance._warn(device_id, object_id, str(warning.message))

        except:
            if sys.exc_info()[0].__name__ == 'RuntimeError':
                assert_reason = str(sys.exc_info()[1])
            else:
                assert_reason = 'Invalid syntax'
            _MxDCore.instance._raise(device_id, object_id, assert_reason)

    else:
        _MxDCore.instance._raise(device_id, object_id, 'Unknown command: ' + command)
    return