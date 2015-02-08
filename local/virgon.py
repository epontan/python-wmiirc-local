from socket import gethostname
from local import AbortModuleLoadException

if gethostname() != 'virgon':
    raise AbortModuleLoadException


import wmiirc_local
from wmiirc_local import *

from plugins import volume, ps, temperature, clock
from plugins import acpi, network


# Right bar status plugins
volume.Volume()
network.Wicd()
ps.Cpu()
ps.Memory()
temperature.Temperature()
acpi.Battery()
clock.Clock()


# vim:se sts=4 sw=4 et:
