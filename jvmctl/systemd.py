import sys
import dbus

class Systemd:
    def __init__(self):
        self.bus = dbus.SystemBus()
        systemd = bus.get_object('org.freedesktop.systemd1','/org/freedesktop/systemd1')
        self.manager = dbus.Interface(systemd, 'org.freedesktop.systemd1.Manager')

    def generate_unit(self):
        out = ConfigParser()
        out.optionxform = str
        out.add_section('Service')
        out['Service']['StartExec'] = cmdline
        out['Service']['User'] = config['jvmctl']['USER']
        out['Service']['Environment'] = format_env_block(config['env'])
        out.write(sys.stdout, space_around_delimiters=False)

