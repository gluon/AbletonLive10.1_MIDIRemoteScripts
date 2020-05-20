#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Axiom_DirectLink/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
from .Axiom_DirectLink import Axiom_DirectLink

def create_instance(c_instance):
    return Axiom_DirectLink(c_instance)


from _Framework.Capabilities import *

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=1891, product_ids=[8237], model_name=u'Axiom 49'),
     PORTS_KEY: [inport(props=[NOTES_CC]),
                 inport(props=[NOTES_CC, SCRIPT]),
                 inport(props=[NOTES_CC]),
                 outport(props=[]),
                 outport(props=[SCRIPT])]}
