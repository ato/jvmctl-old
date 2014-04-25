from __future__ import print_function
import os, sys, argparse, subprocess, shutil, vcstools
from jvmctl.systemd import Systemd

initd = Systemd()
parser = argparse.ArgumentParser(description='Manage JVMs')
subparsers = parser.add_subparsers(metavar="<subcommand>")

class Node(object):
    pass

def node(args):
    node = Node()
    node.name = args.node
    node.config_file = os.path.join('/etc/jvmctl/nodes/', node.name + '.conf')
    return node

def command(func):
    cmd_parser = subparsers.add_parser(func.__name__, help=func.__doc__)
    cmd_parser.set_defaults(func=func)
    cmd_parser.add_argument('node', help='name of a node')
    return func

#
# Code Management
#

def fail(msg):
    raise Exception(msg)

@command
def deploy(args):
    "(re)build and deploy the application"
    build_root = '/tmp/build'
    build_dest = '/tmp/build-dest'
    os.mkdir(build_root)
    os.mkdir(build_dest)
    vcs_client = vcstools.get_vcs_client('git', build_root)
    vcs_client.checkout('source-url', version='1.2.3') or fail('source checkout failed')
    # TODO: build environment
    # TODO: build user
    if os.path.exists(os.path.join(build_root, 'nla-deploy.sh')):
        subprocess.call(['bash', 'nla-deploy.sh', build_dest, 'bogus'], cwd=build_root)
    elif os.path.exists(os.path.join(build_root, 'pom.xml')):
        subprocess.call(['mvn', 'package'], cwd=build_root)
    else:
        print('jvmctl: No build script found (add a pom.xml or nla-deploy.sh)', file=sys.stderr)
    

#
# Process Management
#

@command
def disable(args):
    "prevent the node from running on startup"
    return initd.disable(node(args))

@command
def enable(args):
    "allow the node to run on startup"
    return initd.enable(node(args))

@command
def pid(args):
    "print process ID of this node"
    print(initd.pid(node(args)))

@command
def restart(args):
    "stop and then start the node"
    return initd.restart(node(args))

@command
def start(args):
    "start the node"
    return initd.start(node(args))

@command
def status(args):
    "check whether the node is running"
    return initd.status(node(args))

@command
def stop(args):
    "temporarily stop the node"
    return initd.stop(node(args))

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

def main():
    args = parser.parse_args()
    result = args.func(args)
    if isinstance(result, (int, long)):
        sys.exit(result)

