# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/_MxDCore/MxDControlSurfaceAPI.py
# Compiled at: 2019-04-09 19:23:45
from __future__ import absolute_import, print_function, unicode_literals
from collections import namedtuple
from _MxDCore.LomTypes import is_control_surface, get_control_surfaces
RECEIVE_MIDI_TIMEOUT = 0.2

def midi_byte_to_int(byte):
    if isinstance(byte, (str, unicode)):
        return int(byte, 0)
    return byte


def midi_bytes_are_sysex(bytes):
    return len(bytes) > 3 and bytes[0] == 240 and bytes[(-1)] == 247


def check_attribute(lom_object, actual_name, shown_name):
    if not hasattr(lom_object, actual_name):
        raise AttributeError(("object '{}' has no attribute '{}'").format(type(lom_object).__name__, shown_name))


class MxDControlSurfaceAPI(object):

    def __init__(self, mxdcore, *a, **k):
        super(MxDControlSurfaceAPI, self).__init__(*a, **k)
        self._mxdcore = mxdcore
        self._grabbed_controls_per_cs = {}

    class MxDMidiOwner(namedtuple('Owner', 'device_id object_id mxdcore')):

        def send_reply(self, selector, message):
            message_str = self.mxdcore.str_representation_for_object(message)
            selector_str = {'send_receive': 'send_receive_sysex', 
               'grab': 'grab_midi', 
               'release': 'release_midi', 
               'received': 'received_midi'}.get(selector, str(selector))
            try:
                self.mxdcore.manager.send_message(self.device_id, self.object_id, 'obj_output', '"' + selector_str + '"  ' + message_str)
            except:
                pass

        def report_error(self, message):
            self.mxdcore._raise(self.device_id, self.object_id, message)

        def is_expected_reply(self, message):
            return midi_bytes_are_sysex(message)

    def object_send_midi(self, device_id, object_id, lom_object, parameters):
        check_attribute(lom_object, 'mxd_midi_scheduler', 'send_midi')
        midi_message = tuple(map(midi_byte_to_int, parameters[1:]))
        lom_object.mxd_midi_scheduler.send(self.MxDMidiOwner(device_id, object_id, self._mxdcore), midi_message)

    def object_send_receive_sysex(self, device_id, object_id, lom_object, parameters):
        check_attribute(lom_object, 'mxd_midi_scheduler', 'send_receive_sysex')
        owner = self.MxDMidiOwner(device_id, object_id, self._mxdcore)
        has_timeout = len(parameters) > 2 and parameters[(-2)] == 'timeout'
        timeout = parameters[(-1)] if has_timeout else RECEIVE_MIDI_TIMEOUT
        midi_parameters = parameters[1:-2] if has_timeout else parameters[1:]
        midi_message = tuple(map(midi_byte_to_int, midi_parameters))
        if midi_bytes_are_sysex(midi_message):
            lom_object.mxd_midi_scheduler.send_receive(owner, midi_message, timeout)
        else:
            self._mxdcore._raise(device_id, object_id, 'non-sysex passed to send_receive_sysex')

    def object_grab_midi(self, device_id, object_id, lom_object, parameters):
        check_attribute(lom_object, 'mxd_midi_scheduler', 'grab_midi')
        lom_object.mxd_midi_scheduler.grab(self.MxDMidiOwner(device_id, object_id, self._mxdcore))

    def object_release_midi(self, device_id, object_id, lom_object, parameters):
        check_attribute(lom_object, 'mxd_midi_scheduler', 'release_midi')
        lom_object.mxd_midi_scheduler.release(self.MxDMidiOwner(device_id, object_id, self._mxdcore))

    def release_control_surface_midi(self, device_id, object_id):
        for control_surface in get_control_surfaces():
            if hasattr(control_surface, 'mxd_midi_scheduler'):
                control_surface.mxd_midi_scheduler.disconnect(self.MxDMidiOwner(device_id, object_id, self._mxdcore))

    def object_get_control_names(self, device_id, object_id, lom_object, parameters):
        if not is_control_surface(lom_object):
            raise AttributeError(("object '{}' has no attribute get_control_names").format(type(lom_object).__name__))
        control_names = self._get_cs_control_names(lom_object)
        result = 'control_names %d\n' % len(control_names) + ('').join([ ('control {}\n').format(name) for name in control_names ]) + 'done'
        self._mxdcore.manager.send_message(device_id, object_id, 'obj_call_result', result)

    def _get_cs_control_names(self, cs):
        return [ control.name for control in cs.controls if hasattr(control, 'name') and control.name ]

    def object_get_control(self, device_id, object_id, lom_object, parameters):
        if not is_control_surface(lom_object):
            raise AttributeError(("object '{}' has no attribute get_control").format(type(lom_object).__name__))
        cs = lom_object
        name = parameters[1]
        control = self._get_cs_control(cs, name)
        result_str = self._mxdcore.str_representation_for_object(control)
        self._mxdcore.manager.send_message(device_id, object_id, 'obj_call_result', result_str)

    def _get_cs_control(self, cs, name):
        for control in cs.controls:
            if hasattr(control, 'name') and control.name == name:
                return control

        return

    def set_control_element(self, control, grabbed):
        u"""called back from control.resource.grab/release"""
        if hasattr(control, 'release_parameter'):
            control.release_parameter()
        control.reset()

    def _get_control_or_raise(self, cs, control_or_name, command):
        if not is_control_surface(cs):
            raise AttributeError(("object '{}' has no attribute {}").format(type(cs).__name__, command))
        if not control_or_name:
            raise AttributeError(('control id or name required for {}').format(command))
        if isinstance(control_or_name, (str, unicode)):
            control = self._get_cs_control(cs, control_or_name)
            if not control:
                raise AttributeError(("{} is not a control of '{}'").format(control_or_name, type(cs).__name__))
        else:
            control = control_or_name
            if control not in cs.controls:
                id_str = self._mxdcore.str_representation_for_object(control)
                raise AttributeError(("'{}' ({}) is not a control of '{}'").format(type(control).__name__, id_str, type(cs).__name__))
        return control

    def object_grab_control(self, device_id, object_id, lom_object, parameters):
        cs = lom_object
        control_or_name = parameters[1]
        control = self._get_control_or_raise(cs, control_or_name, 'grab_control')
        if cs not in self._grabbed_controls_per_cs:
            self._grabbed_controls_per_cs[cs] = []
            cs.add_disconnect_listener(self._disconnect_control_surface)
        grabbed_controls = self._grabbed_controls_per_cs[cs]
        if control not in grabbed_controls:
            with cs.component_guard():
                priority = cs.mxd_grab_control_priority() if hasattr(cs, 'mxd_grab_control_priority') else 1
                control.resource.grab(self, priority=priority)
                if hasattr(control, 'suppress_script_forwarding'):
                    control.suppress_script_forwarding = False
                grabbed_controls.append(control)

    def object_release_control(self, device_id, object_id, lom_object, parameters):
        cs = lom_object
        control_or_name = parameters[1]
        control = self._get_control_or_raise(cs, control_or_name, 'release_control')
        grabbed_controls = self._grabbed_controls_per_cs.setdefault(cs, [])
        if control in grabbed_controls:
            with cs.component_guard():
                grabbed_controls.remove(control)
                control.resource.release(self)

    def _disconnect_control_surface(self, cs):
        try:
            for control in self._grabbed_controls_per_cs[cs]:
                with cs.component_guard():
                    control.resource.release(self)

            del self._grabbed_controls_per_cs[cs]
        except KeyError:
            pass