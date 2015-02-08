import os
import dbus
from pygmi import fs, _

import wmiirc
from wmiirc import *

from plugins import dbus_instance
from plugins import notice
from plugins import spotify
from plugins import nx


# Theme
wmiirc.background = '#333333'
wmiirc.floatbackground='#222222'

wmii['font'] = '-*-terminus-medium-*-*-*-12-*-*-*-*-*-*-*'
wmii['normcolors'] = '#dddddd', '#474747', '#727272'
wmii['focuscolors'] = '#a7d8fe', '#232323', '#474747'
wmii.cache['urgentcolors'] = '#dddddd', '#bb6050', '#dd8070'
wmii['border'] = 1
tags.focuscol = '#a7d8fe', '#232323', '#232323'
tags.reset()


# Behavior / rules
keys.defs['mod'] = 'Mod1'
wmiirc.terminal = 'wmiir', 'setsid', 'urxvt'
wmii['grabmod'] = keys.defs['mod']
wmii['colmode'] = 'default'

wmii.colrules = (
    (ur'gimp', '17+83+41'),
    (ur'comm', '20+80'),
    (ur'dev', '40+60'),
    (ur'vpn', '40+60'),
    (ur'.*', '50+50'),
)

wmii.rules = (
    (ur':MPlayer:', dict(floating=True)),
    (ur'^Pidgin:', dict(tags='comm')),
    (ur':Firefox:', dict(tags='www')),
    (ur':Thunderbird:', dict(tags='mail')),
    (ur'^libreoffice:', dict(tags='docs', group=0)),
    (ur'^spotify:', dict(tags='music', floating=False)),
    (ur'^X2GoAgent:|:NX - ', dict(tags='x', floating=False)),
)


# Initialize plugins
nx_handler = nx.NXHandler()


# Right bar status plugins
fs.indexed_bar.add('right') # Make them stay in the order they are created
notice.Notice()


# Misc functions
def setbackground(color='black'):
    bg_file = '%s/background' % os.path.dirname(__file__)
    if os.path.isfile(bg_file):
        call('feh', '--no-fehbg', '--bg-fill', bg_file)
    else:
        call('xsetroot', '-solid', color)
wmiirc.setbackground = setbackground

def lock(blank=False):
    cmd = ['securezone']
    if blank:
        cmd.append('-b')
    return call(*cmd, background=True)

def system_ctl(action):
    logind = dbus_instance.get_system_bus().get_object('org.freedesktop.login1',
            '/org/freedesktop/login1')
    manager = dbus.Interface(logind, 'org.freedesktop.login1.Manager')
    getattr(manager, action)(True)


# Actions
class Actions(wmiirc.Actions):
    def __init__(self):
        super(Actions, self).__init__(show_scripts=False)
    def lock(self, args=''):
        lock()
    def suspend(self, args=''):
        lock()
        system_ctl('Suspend')
    def reboot(self, args=''):
        system_ctl('Reboot')
        self.quit()
    def poweroff(self, args=''):
        system_ctl('PowerOff')
        self.quit()
wmiirc.actions = Actions()


# Key bindings
keys.unbind([
    '%(mod)s-y',
    '%(mod)s-i', '%(mod)s-Shift-i',
    '%(mod)s-o', '%(mod)s-Shift-o',
    '%(mod)s-b', '%(mod)s-Shift-b',
    '%(mod)s-n', '%(mod)s-Shift-n',
])

keys.bind('main', (
    "Security",
    ('Control-%(mod)s-l', "Lock screens",
        lambda k: lock(True)),

    "Tag actions",
    ('%(mod)s-b', "Create a temporary tag for selected client",
        lambda k: wmiirc.temp_tag()),

    ('%(mod)s-i', "Move to the last tag",
        lambda k: tags.select(tags.LAST)),
    ('%(mod)s-Shift-i', "Move to the last tag, take along current client",
        lambda k: tags.select(tags.LAST, take_client=Client('sel'))),

    ('%(mod)s-q', "Move to the view to the left",
        lambda k: tags.select(tags.next(True))),
    ('%(mod)s-w', "Move to the view to the right",
        lambda k: tags.select(tags.next())),
    ('%(mod)s-Shift-q', "Move to the view to the left, take along current client",
        lambda k: tags.select(tags.next(True), take_client=Client('sel'))),
    ('%(mod)s-Shift-w', "Move to the view to the right, take along current client",
        lambda k: tags.select(tags.next(), take_client=Client('sel'))),

    "Spotify control",
    ('%(mod)s-Up', "Show song meta information",
        lambda k: spotify.toggle_meta_info()),
    ('%(mod)s-Down', "Toggle play/pause",
        lambda k: spotify.play_pause()),
    ('%(mod)s-Left', "Play previous song",
        lambda k: spotify.prev()),
    ('%(mod)s-Right', "Play next song",
        lambda k: spotify.next()),
    ('XF86AudioStop', "Quit spotify",
        lambda k: spotify.quit()),

    "NX",
    ('%(mod)s-x', "Move to x tag and make passthrough",
        lambda k: tags.select('x') or setattr(keys, 'mode', 'nx')),
))

keys.bind('nx', (
    "NX",
    ('%(mod)s-x', "Move out from x tag and restore passthrough",
        lambda k: tags.select(tags.LAST) or setattr(keys, 'mode', 'main')),
))


# Events
events.unbind([
    'AreaFocus',
    Match('LeftBarMouseDown', 3),
    Match('ClientClick', _, 4),
    Match('ClientClick', _, 5),
])


# Load any local adaptations
import local


# Run custom hook script if any
custom_hook = find_script('hook')
if custom_hook:
    call(custom_hook, background=True)


# vim:se sts=4 sw=4 et:
