# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/Launchpad_MK2/__init__.py
# Compiled at: 2019-04-09 19:23:44
from __future__ import absolute_import, print_function, unicode_literals
from .Launchpad_MK2 import Launchpad_MK2
from _Framework.Capabilities import controller_id, inport, outport, CONTROLLER_ID_KEY, PORTS_KEY, NOTES_CC, SCRIPT, SYNC, REMOTE

def get_capabilities():
    return {CONTROLLER_ID_KEY: controller_id(vendor_id=5042, product_ids=[
                         105, 106, 107, 108,
                         109, 110, 111, 112,
                         113, 114, 115, 116,
                         117, 118, 119, 120], model_name=[
                         'Launchpad MK2', 'Launchpad MK2 2',
                         'Launchpad MK2 3', 'Launchpad MK2 4',
                         'Launchpad MK2 5', 'Launchpad MK2 6',
                         'Launchpad MK2 7', 'Launchpad MK2 8',
                         'Launchpad MK2 9', 'Launchpad MK2 10',
                         'Launchpad MK2 11', 'Launchpad MK2 12',
                         'Launchpad MK2 13', 'Launchpad MK2 14',
                         'Launchpad MK2 15', 'Launchpad MK2 16']), 
       PORTS_KEY: [
                 inport(props=[NOTES_CC, SCRIPT, REMOTE]),
                 outport(props=[NOTES_CC, SCRIPT, SYNC, REMOTE])]}


def create_instance(c_instance):
    return Launchpad_MK2(c_instance)