from socket import gethostname
from local import AbortModuleLoadException

if gethostname() != 'tauron':
    raise AbortModuleLoadException


import wmiirc_local
from wmiirc_local import *

from plugins import volume, ps, temperature, clock


# Behavior / rules
wmii.rules += (
    (ur'^Steam:', dict(tags='game')),
)


# Right bar status plugins
volume.Volume()
ps.Cpu()
ps.Memory()
temperature.Temperature()
clock.Clock()


# vim:se sts=4 sw=4 et:
