from socket import gethostname
from local import AbortModuleLoadException

if not gethostname().startswith('elx'):
    raise AbortModuleLoadException

import shlex

import wmiirc
import wmiirc_local
from wmiirc_local import *

from plugins import notice
from plugins import volume, ps, temperature, clock
from plugins import upower, network
from plugins import mail, track


# Behavior / rules
wmiirc.terminal = 'wmiir', 'setsid', 'uxterm'

wmii.rules += (
    (ur'Wfica', dict(tags='win')),
    (ur'^pdfpc:', dict(tags='pres')),
    (ur'^mirror:Mirror:', dict(tags=r'/./', fullscreen=True)),
)


# Right bar status plugins
mail.Mail()
volume.Volume(device='pulse')
network.Wicd()
ps.Cpu()
ps.Memory()
temperature.Temperature()
upower.Battery()
work = track.Work()
clock.Clock()


# Override lock function
_super_lock = wmiirc_local.lock
def _lock(*arg):
    work.locked(_super_lock(*arg))
wmiirc_local.lock = _lock

# Override system_ctl function
_super_system_ctl = wmiirc_local.system_ctl
def _system_ctl(action):
    work.track(action.upper())
    _super_system_ctl(action)
wmiirc_local.system_ctl = _system_ctl


# Actions
class Actions(wmiirc_local.Actions):
    def xrandr_laptop(self, args=''):
        cmd = shlex.split('xrandr --output eDP1 --crtc 0 --auto --primary --output DP1-1 --off --output DP1-2 --off --output DP1-3 --off --output DP1 --off --output HDMI1 --off')
        call(*cmd)
        setbackground()
    def xrandr_work(self, args=''):
        cmd = shlex.split('xrandr --output eDP1 --crtc 0 --off --output DP1-1 --crtc 1 --auto --primary --output DP1-3 --crtc 2 --auto --left-of DP1-1')
        call(*cmd)
        setbackground()
    def xrandr_pres(self, args=''):
        output = Menu(choices=lambda: ['mDP/VGA', 'HDMI'], prompt='Display output: ')()
        if output == 'HDMI': output = 'HDMI1'
        else: output = 'DP1'
        cmd = shlex.split('xrandr --output %s --auto --above eDP1' % output)
        call(*cmd)
        setbackground()
wmiirc.actions = Actions()


# Screen brightness control
def adjust_brightness(adjustment):
    call("xbacklight", "-time", "0", "-steps", "1", "-inc", str(adjustment))
    percentage = round(float(call("xbacklight")))
    notice.write("Brightness %d%%" % percentage)


# Key bindings
keys.bind('main', (
    "Screen brightness",
    ('XF86MonBrightnessUp', "Increase the screen brightness",
        lambda k: adjust_brightness(25)),
    ('XF86MonBrightnessDown', "Decrease the screen brightness",
        lambda k: adjust_brightness(-25)),

    "NX",
    ('%(mod)s-e', "Toggle between NX client and other",
        lambda k: nx_handler.toggle()),
    ('%(mod)s-Shift-e', "Reset mouse positions for NX toggle",
        lambda k: nx_handler.reset()),
))

keys.bind('nx', (
    "NX",
    ('%(mod)s-e', "Toggle between NX client and other",
        lambda k: nx_handler.toggle()),
    ('%(mod)s-Shift-e', "Reset mouse positions for NX toggle",
        lambda k: nx_handler.reset()),
    ('%(mod)s-Shift-f', "Toggle fullscreen of NX client",
        lambda k: nx_handler.toggle_fullscreen()),
))


# Events
events.bind({
    'ClientFocus': lambda c: nx_handler.check_client(c),
    'AreaFocus': lambda a: nx_handler.check_area(a),
})


# Lower mouse sensitity (default: 2/1 4)
call('xset', 'm', '5/3', '4')

# Disable DPMS (kernel panics sometimes when trying to recover)
call('xset', '-dpms')


# vim:se sts=4 sw=4 et:
