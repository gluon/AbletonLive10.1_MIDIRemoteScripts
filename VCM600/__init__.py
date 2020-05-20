#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/VCM600/__init__.py
from __future__ import absolute_import, print_function, unicode_literals
from .VCM600 import VCM600

def create_instance(c_instance):
    u""" Creates and returns the ADA1 script """
    return VCM600(c_instance)
