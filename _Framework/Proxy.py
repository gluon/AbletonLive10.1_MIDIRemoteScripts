# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_Framework/Proxy.py
# Compiled at: 2019-04-09 19:23:45
from __future__ import absolute_import, print_function, unicode_literals
from .Util import BooleanContext

class ProxyBase(object):
    u"""
    Provides a general mechanism for building automatic proxy
    objects. The access is determined between the proxied_object, the
    proxied_interface and the proxy itself following the following rules:

    When getting an attribute:

       - If it is the proxy object, return that.
       - Else if it is in the proxied_object and in the proxied_interface,
         return that of the proxied_object.
       - Else if it is in the proxied_interface, return that.
       - Else, throw an attribute error.

    When setting an attribute, since it is more risky, the rules are stricter.

       - If the the attribute is present in the proxy_interface, but not
         in the proxy, set in the proxy_object.
       - Else if the attribute is not preent in the proxy_interface, set it
         in the proxy_object.
       - If the attribute is present in both the proxy_interface and
         the proxy_object, raise an AttributeError complaining about
         ambiguity.
    """
    _skip_wrapper_lookup = None

    def __init__(self, *a, **k):
        super(ProxyBase, self).__init__(*a, **k)
        self._skip_wrapper_lookup = BooleanContext()

    def proxy_hasattr(self, attr):
        u"""
        Returns wether the proxy, not the proxied, has an attribute.
        """
        with self._skip_wrapper_lookup():
            return hasattr(self, attr)

    def __getattr__(self, name):
        if not self._skip_wrapper_lookup:
            obj = self.proxied_object
            interface = self.proxied_interface
            if obj and hasattr(interface, name):
                return getattr(obj, name)
            return getattr(interface, name)
        raise AttributeError, 'Does not have attribute %s' % name

    def __setattr__(self, name, value):
        obj = self.proxied_object
        interface = self.proxied_interface
        if obj and hasattr(interface, name):
            if self.proxy_hasattr(name):
                raise AttributeError, 'Ambiguous set attribute: %s proxied: %s' % (name, obj)
            setattr(obj, name, value)
        elif hasattr(interface, name):
            raise AttributeError, 'Ambiguous set attribute: %s proxied: %s' % (name, obj)
        else:
            self.__dict__[name] = value

    @property
    def proxied_object(self):
        return

    @property
    def proxied_interface(self):
        obj = self.proxied_object
        return getattr(obj, 'proxied_interface', obj)


class Proxy(ProxyBase):
    proxied_object = None
    _proxied_interface = None

    @property
    def proxied_interface(self):
        return self._proxied_interface or super(Proxy, self).proxied_interface

    def __init__(self, proxied_object=None, proxied_interface=None, *a, **k):
        super(Proxy, self).__init__(*a, **k)
        self.proxied_object = proxied_object
        self._proxied_interface = proxied_interface