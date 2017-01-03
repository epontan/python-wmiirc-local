from os.path import exists
from local import AbortModuleLoadException
from local.common import command_exists

if not exists('/usr/NX') and not command_exists('nxssh'):
    raise AbortModuleLoadException


from wmiirc_local import *
from plugins.nx import NXHandler


nx_handler = NXHandler()

wmii.rules += (
    (ur'^X2GoAgent:|:NX - ', dict(tags='x', floating=False)),
)

keys.bind('main', (
    "NX",
    ('%(mod)s-x', "Move to x tag and make passthrough",
        lambda k: tags.select('x') or setattr(keys, 'mode', 'nx')),
    ('%(mod)s-e', "Toggle between NX client and other",
        lambda k: nx_handler.toggle()),
    ('%(mod)s-Shift-e', "Reset mouse positions for NX toggle",
        lambda k: nx_handler.reset()),
))

keys.bind('nx', (
    "NX",
    ('%(mod)s-x', "Move out from x tag and restore passthrough",
        lambda k: tags.select(tags.LAST) or setattr(keys, 'mode', 'main')),
    ('%(mod)s-e', "Toggle between NX client and other",
        lambda k: nx_handler.toggle()),
    ('%(mod)s-Shift-e', "Reset mouse positions for NX toggle",
        lambda k: nx_handler.reset()),
    ('%(mod)s-Shift-f', "Toggle fullscreen of NX client",
        lambda k: nx_handler.toggle_fullscreen()),
))

events.bind({
    'ClientFocus': lambda c: nx_handler.check_client(c),
    'AreaFocus': lambda a: nx_handler.check_area(a),
})


# vim:se sts=4 sw=4 et:
