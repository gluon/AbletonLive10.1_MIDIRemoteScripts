# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/pushbase/internal_parameter.py
# Compiled at: 2019-04-23 14:43:03
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import clamp, listenable_property, liveobj_valid, nop, EventError, EventObject, forward_property, Proxy, Slot
from ableton.v2.control_surface import EnumWrappingParameter, InternalParameter, InternalParameterBase, RelativeInternalParameter, WrappingParameter, to_percentage_display

class ConstantParameter(InternalParameterBase):
    forward_from_original = forward_property('_original_parameter')

    def __init__(self, original_parameter=None, *a, **k):
        assert original_parameter is not None
        super(InternalParameterBase, self).__init__(*a, **k)
        self._original_parameter = original_parameter
        return

    add_value_listener = forward_from_original('add_value_listener')
    remove_value_listener = forward_from_original('remove_value_listener')
    value_has_listener = forward_from_original('value_has_listener')
    canonical_parent = forward_from_original('canonical_parent')
    min = forward_from_original('min')
    max = forward_from_original('max')
    name = forward_from_original('name')
    original_name = forward_from_original('original_name')
    default_value = forward_from_original('default_value')
    automation_state = forward_from_original('automation_state')
    state = forward_from_original('state')
    _live_ptr = forward_from_original('_live_ptr')

    @property
    def display_value(self):
        return str(self._original_parameter)

    def _get_value(self):
        return self._original_parameter.value

    def _set_value(self, _):
        pass

    value = property(_get_value, _set_value)
    linear_value = property(_get_value, _set_value)

    def __str__(self):
        return self.display_value


class ProxyParameter(Proxy):
    u"""
    Behaves like Proxy, but with inverted logic of getting arguments from the passed
    interface / proxied object. It means the proxied interface can override
    proxied object's attributes.
    """

    def __getattr__(self, name):
        if not self._skip_wrapper_lookup:
            obj = self.proxied_object
            return getattr(self.proxied_interface, name, getattr(obj, name))
        raise AttributeError('Does not have attribute %s' % name)

    def __unicode__(self):
        return unicode(self.proxied_object)

    def __eq__(self, other):
        if isinstance(other, ProxyParameter):
            return self.proxied_object == other.proxied_object and self.proxied_interface == other.proxied_interface
        return self.proxied_object == other

    def __ne__(self, other):
        if isinstance(other, ProxyParameter):
            return self.proxied_object != other.proxied_object or self.proxied_interface != other.proxied_interface
        return self.proxied_object != other