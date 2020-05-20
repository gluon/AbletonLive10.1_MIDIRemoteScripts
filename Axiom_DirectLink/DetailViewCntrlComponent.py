#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Axiom_DirectLink/DetailViewCntrlComponent.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement

class DetailViewCntrlComponent(ControlSurfaceComponent):
    u""" Component that can navigate the selection of devices """

    def __init__(self):
        ControlSurfaceComponent.__init__(self)
        self._left_button = None
        self._right_button = None

    def disconnect(self):
        if self._left_button != None:
            self._left_button.remove_value_listener(self._nav_value)
            self._left_button = None
        if self._right_button != None:
            self._right_button.remove_value_listener(self._nav_value)
            self._right_button = None

    def set_device_nav_buttons(self, left_button, right_button):
        assert left_button == None or isinstance(left_button, ButtonElement)
        assert right_button == None or isinstance(right_button, ButtonElement)
        identify_sender = True
        if self._left_button != None:
            self._left_button.remove_value_listener(self._nav_value)
        self._left_button = left_button
        if self._left_button != None:
            self._left_button.add_value_listener(self._nav_value, identify_sender)
        if self._right_button != None:
            self._right_button.remove_value_listener(self._nav_value)
        self._right_button = right_button
        if self._right_button != None:
            self._right_button.add_value_listener(self._nav_value, identify_sender)
        self.update()

    def on_enabled_changed(self):
        self.update()

    def update(self):
        super(DetailViewCntrlComponent, self).update()
        if self.is_enabled():
            if self._left_button != None:
                self._left_button.turn_off()
            if self._right_button != None:
                self._right_button.turn_off()

    def _nav_value(self, value, sender):
        assert sender != None and sender in (self._left_button, self._right_button)
        if self.is_enabled():
            if not sender.is_momentary() or value != 0:
                modifier_pressed = True
                if not self.application().view.is_view_visible(u'Detail') or not self.application().view.is_view_visible(u'Detail/DeviceChain'):
                    self.application().view.show_view(u'Detail')
                    self.application().view.show_view(u'Detail/DeviceChain')
                else:
                    direction = Live.Application.Application.View.NavDirection.left
                    if sender == self._right_button:
                        direction = Live.Application.Application.View.NavDirection.right
                    self.application().view.scroll_view(direction, u'Detail/DeviceChain', not modifier_pressed)
