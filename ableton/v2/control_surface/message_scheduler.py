# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/message_scheduler.py
# Compiled at: 2019-04-09 19:23:45
from __future__ import absolute_import, print_function, unicode_literals
from collections import namedtuple

class MessageScheduler(object):
    u"""
    Schedules outgoing messages (sysex and other MIDI) sent to a
    MIDI port shared between multiple owners and synchronizes them
    with incoming messages (sysex only).
    For request/response message pairs this ensures that responses are
    sent back to where the requests came from (the owner).
    Also, it allows for a temporary routing of unexpected messages
    to an owner grabbing the device.
    """

    def __init__(self, send_message_callback, timer):
        self._send_message_callback = send_message_callback
        self._timer = timer
        self._state = 'idle'
        self._owner = None
        self._request_type = namedtuple('Request', 'action owner message timeout')
        self._request_queue = []
        return

    @property
    def is_idling(self):
        return self._state == 'idle' and self._owner == None and len(self._request_queue) == 0

    def __repr__(self):
        return ('MessageScheduler(state={}, owner={})').format(self._state, self._owner)

    def _process_request(self, request):
        assert self._owner == None or self._owner == request.owner
        if request.action == 'send':
            if self._state == 'idle' or self._state == 'grabbed' and self._owner == request.owner:
                self._send_message_callback(request.message)
                return True
            else:
                return False

        elif request.action == 'grab':
            if self._state == 'idle':
                self._state = 'grabbed'
                self._owner = request.owner
                self._owner.send_reply('grab', '1')
                return True
            else:
                if self._state == 'grabbed':
                    request.owner.report_error('unexpected grab')
                    return True
                return False

        elif request.action == 'release':
            if self._state == 'idle':
                request.owner.report_error('unexpected release')
                return True
            else:
                if self._state == 'grabbed':
                    assert self._owner == request.owner
                    self._owner.send_reply('release', '1')
                    self._state = 'idle'
                    self._owner = None
                    return True
                return False

        elif request.action == 'send_receive':
            if self._state == 'idle':
                self._send_message_callback(request.message)
                self._state = 'wait'
                self._owner = request.owner
                self._timer.start(request.timeout, self.handle_timeout)
                return True
            else:
                if self._state == 'grabbed' and self._owner == request.owner:
                    self._send_message_callback(request.message)
                    self._state = 'grabbed_wait'
                    self._timer.start(request.timeout, self.handle_timeout)
                    return True
                return False

        return

    def _queue(self, request):
        if request.owner is not None:
            self._request_queue.append(request)
        return

    def _process_single_request(self):
        for i, request in enumerate(self._request_queue):
            if self._owner in (None, request.owner):
                if self._process_request(request):
                    del self._request_queue[i]
                    return True
                else:
                    return False

        return False

    def _process_queue(self):
        while self._process_single_request():
            pass

    def send(self, owner, message):
        request = self._request_type('send', owner, message, 0)
        self._queue(request)
        self._process_queue()

    def grab(self, owner):
        request = self._request_type('grab', owner, None, 0)
        self._queue(request)
        self._process_queue()
        return

    def release(self, owner):
        request = self._request_type('release', owner, None, 0)
        self._queue(request)
        self._process_queue()
        return

    def send_receive(self, owner, message, timeout):
        request = self._request_type('send_receive', owner, message, timeout)
        self._queue(request)
        self._process_queue()

    def handle_message(self, message):
        if self._state == 'idle':
            pass
        elif self._state == 'wait':
            if self._owner.is_expected_reply(message):
                self._owner.send_reply('send_receive', message)
                self._state = 'idle'
                self._owner = None
                self._timer.cancel()
                self._process_queue()
        elif self._state == 'grabbed':
            self._owner.send_reply('received', message)
        elif self._state == 'grabbed_wait':
            if self._owner.is_expected_reply(message):
                self._owner.send_reply('send_receive', message)
                self._state = 'grabbed'
                self._timer.cancel()
                self._process_queue()
            else:
                self._owner.send_reply('received', message)
        return

    def handle_timeout(self):
        if self._state == 'wait':
            self._owner.send_reply('send_receive', 'timeout')
            self._state = 'idle'
            self._owner = None
            self._process_queue()
        elif self._state == 'grabbed_wait':
            self._owner.send_reply('send_receive', 'timeout')
            self._state = 'grabbed'
            self._process_queue()
        return

    def disconnect(self, owner):
        if self._state != 'idle':
            self._request_queue = [ r for r in self._request_queue if r.owner != owner ]
            if self._owner == owner:
                self._owner = None
                self._state = 'idle'
                self._timer.cancel()
            self._process_queue()
        return