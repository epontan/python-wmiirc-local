from pygmi import call


def command_exists(command):
    null = open('/dev/null', 'w')
    p = call('which', command, stdout=null, stderr=null, background=True)
    return p.wait() == 0


# Synchronize clipboard and X selection buffer using autocutsel
if command_exists('autocutsel'):
    call('pkill', '-x', 'autocutsel') # Terminate any previous instances
    call('autocutsel', '-fork', background=True)
    call('autocutsel', '-selection', 'PRIMARY', '-fork', background=True)

# Automounting functionality and ability to mount as user
if command_exists('udiskie'):
    call('pkill', '-x', 'udiskie') # Terminate any previous instances
    call('udiskie', '-2', '-a', '-N', '-T', background=True)

# Disable touchpad tapping
if command_exists('synclient'):
    call('synclient', 'MaxTapTime=0')


# vim:se sts=4 sw=4 et:
