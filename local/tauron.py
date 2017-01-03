from pygmi import call
from socket import gethostname
from local import AbortModuleLoadException

if gethostname() != 'tauron':
    raise AbortModuleLoadException


import wmiirc_local
from wmiirc_local import *

from plugins import volume, ps, temperature, clock


# Behavior / rules
wmii.rules += (
    (ur'^qemu-system', dict(floating=True)),
    (ur'^Steam:', dict(tags='game')),
)


# Right bar status plugins
volume.Volume()
ps.Cpu()
ps.Memory()
temperature.Temperature()
clock.Clock()

keys.bind('main', (
    "Misc",
    ('%(mod)s-z', "Counting windows app",
        lambda k: call('cwin', background=True)),
))


# Ensure "maximum performance" is enabled
call('nvidia-settings', '-a', '[gpu:0]/GpuPowerMizerMode=1')

# Adjust the color temperature of the screen(s) to be easy on the eye
call('pkill', '-x', 'redshift') # Terminate any previous instances
call('redshift', '-l57.70:11.94', background=True)

# Enable transparency and nice transitions
call('pkill', '-x', 'compton') # Terminate any previous instances
# call('compton', background=True)


# vim:se sts=4 sw=4 et:
