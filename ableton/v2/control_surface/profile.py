# uncompyle6 version 3.4.1
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.16 (v2.7.16:413a49145e, Mar  2 2019, 14:32:10) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/versonator/Jenkins/live/output/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ableton/v2/control_surface/profile.py
# Compiled at: 2019-04-09 19:23:45
u"""
Provides facilities to ease the profiling of Control Surfaces.
"""
from __future__ import absolute_import, print_function, unicode_literals
from functools import wraps, partial
ENABLE_PROFILING = False
if ENABLE_PROFILING:
    import cProfile
    PROFILER = cProfile.Profile()

def profile(fn):
    u"""
    Decorator to mark a function to be profiled.
    """
    if ENABLE_PROFILING:

        @wraps(fn)
        def wrapper(self, *a, **k):
            if PROFILER:
                return PROFILER.runcall(partial(fn, self, *a, **k))
            else:
                print('Can not profile (%s), it is probably reloaded' % fn.__name__)
                return fn(*a, **k)

        return wrapper
    else:
        return fn


def dump(name='default'):
    u"""
    Dumps profiling data to the working directory with the given `name`. Three files
    are created:

    1. [name].profile contains the profile data in pstats format.
    2. [name].profile.time.txt contains the data in human readable form, sorted
       by *total time* - i.e. how much time has been expent in each function itself,
       without counting the time spent in sub-functions.
    3. [name].profile.cumulative.txt contains the data sorted by cumulative time - i.e.
       how much time is spent in a function and its sub-calls.
    """
    assert ENABLE_PROFILING
    import pstats
    fname = name + '.profile'
    PROFILER.dump_stats(fname)

    def save_human_data(sort):
        s = pstats.Stats(fname, stream=open('%s.%s.txt' % (fname, sort), 'w'))
        s.sort_stats(sort)
        s.print_stats()

    save_human_data('time')
    save_human_data('cumulative')