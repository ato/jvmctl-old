from nose.tools import *
from StringIO import StringIO
import jvmctl
import jvmctl.config

BASIC_CONFIG = """
[jvmctl]
PORT=10240
REPO=svn://example.org/apps/example/trunk
#NLA_ENVIRON=production
NLA_ENVIRON=preprod
ROOT_URL_PREFIX=/example
"""

def test_basic():
    config = jvmctl.config.parse(StringIO(BASIC_CONFIG))
    assert_equal(config['jvmctl']['PORT'], '10240')
    assert_equal(config['jvmctl']['NLA_ENVIRON'], 'preprod')

LEGACY_CONFIG = """
PORT=10240
REPO=svn://example.org/apps/example/trunk
#NLA_ENVIRON=production
NLA_ENVIRON=preprod
ROOT_URL_PREFIX=/example
export SOMEVAR=foo
JAVA_OPTS=(
  # experimental workaround for segfaults in net_read
  # see: http://bugs.sun.com/view_bug.do?bug_id=6346701
  -XX:StackShadowPages=20

  -Dconfig=/apps/$NODE/ROOT/WEB-INF/
-Djava.rmi.server.hostname=$(hostname)
)
"""

def test_legacy():
    config = jvmctl.config.parse(StringIO(LEGACY_CONFIG))
    assert_equal(config['env']['SOMEVAR'], 'foo')
