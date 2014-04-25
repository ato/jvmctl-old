import sys, dbus, subprocess

NS = 'org.freedesktop.systemd1'
MANAGER_IFACE = 'org.freedesktop.systemd1.Manager'
SERVICE_IFACE = 'org.freedesktop.systemd1.Service'

def unit_name(node):
    return node.name + '.service'

class Systemd:
    def __init__(self):
        self.bus = dbus.SystemBus()
        systemd = self.bus.get_object(NS,'/org/freedesktop/systemd1')
        self.manager = dbus.Interface(systemd, MANAGER_IFACE)

    def generate_unit(self, node):
        out = ConfigParser()
        out.optionxform = str
        out.add_section('Node')
        out['Node']['StartExec'] = node.cmdline
        out['Node']['User'] = node.user
        out['Node']['Environment'] = format_env_block(node.env)
        out.write(sys.stdout, space_around_delimiters=False)

    def start(self, node):
        self.manager.StartUnit(unit_name(node), 'replace')

    def stop(self, node):
        self.manager.StopUnit(unit_name(node), 'replace')

    def restart(self, node):
        self.manager.RestartUnit(unit_name(node), 'replace')

    def status(self, node):
        return subprocess.call(['systemctl', 'status', unit_name(node)])

    def pid(self, node):
        unit_path = self.manager.GetUnit(unit_name(node))
        unit = self.bus.get_object(NS, unit_path)
        return unit.Get(NODE_IFACE, 'MainPID', dbus_interface=dbus.PROPERTIES_IFACE)
    
    
