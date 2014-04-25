import os, sys, argparse, subprocess, shutil
from jvmctl.systemd import Systemd

systemd = Systemd()
parser = argparse.ArgumentParser(description='Manage JVMs')
subparsers = parser.add_subparsers(metavar="<subcommand>")

class Node(object):
    pass

def node(args):
    node = Node()
    node.name = args.node
    node.config_file = os.path.join('/etc/jvmctl', node.name + '.conf')
    return node

def command(func):
    cmd_parser = subparsers.add_parser(func.__name__, help=func.__doc__)
    cmd_parser.set_defaults(func=func)
    cmd_parser.add_argument('node', help='name of a node')
    return func

#
# Code Management
#

@command
def deploy(args):
    "(re)build and deploy the application"
    pass

#
# Process Management
#

@command
def disable(args):
    "prevent the node from running on startup"
    return systemd.disable(node(args))

@command
def enable(args):
    "allow the node to run on startup"
    return systemd.enable(node(args))

@command
def pid(args):
    "print process ID of this node"
    print systemd.pid(node(args))

@command
def restart(args):
    "stop and then start the node"
    return systemd.restart(node(args))

@command
def start(args):
    "start the node"
    return systemd.start(node(args))

@command
def status(args):
    "check whether the node is running"
    return systemd.status(node(args))

@command
def stop(args):
    "temporarily stop the node"
    return systemd.stop(node(args))

#
# Configuration
#

@command
def config(args):
    "open $EDITOR on the node config file"
    editor = os.environ.get('EDITOR', 'vi')
    sys.exit(subprocess.call([editor, node(args).config_file]))

@command
def delete(args):
    "delete the node configuration and deployed code"
    pass

@command
def list(args):
    "list all configured nodes"
    pass

@command
def show(args):
    "show node configuration"
    with open(node(args).config_file, 'r') as f:
        shutil.copyfileobj(f, sys.stdout)

#Process management:
#  deploy    - (re)build and reploy the application
#  disable   - stop the node and prevent it from running on startup
#  pid       - print process ID of this node
#  restart   - stop and then start the jetty node
#  start     - start the jetty node
#  status    - check whether the jetty node is running
#  stop      - temporarily stop the jetty node
#
#Configuration:
#  config    - open $EDITOR on the node config file
#  configlog - show configuration history
#  delete    - delete the node
#  list      - list all configured Jetty nodes
#  modify    - automatically modify the node config based on arguments
#  new       - create a new node config file
#  register  - register a new node with the OS
#  show      - show node config
#
#Debugging:
#  gcutil    - show garbage collection status using jstat
#  jdb       - force attach debugger (limited functionality)
#  lsof      - list open files
#  log       - follow the end of the jetty log with less
#  sqltrace  - trace JDBC SQL statements
#  stack     - print thread dump like Ctrl-\
#  truncate  - truncate the current log file
#  truss     - trace system calls

def main():
    args = parser.parse_args()
    result = args.func(args)
    if isinstance(result, (int, long)):
        sys.exit(result)

