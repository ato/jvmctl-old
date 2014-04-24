from configparser import ConfigParser, ExtendedInterpolation

def preprocess_indent(fp):
    "Indent lines within a shell-style array"
    paren_depth = 0
    legacy = True
    for line in fp:
        if line.strip() == '[jvmctl]':
            legacy = False
        if legacy:
            if paren_depth > 0 and line[0] not in [' ', '\t']:
                line = '  ' + line
            paren_depth += line.count('(') - line.count(')')
        yield line

def preprocess_add_header(fp):
    "Add a [jvmctl] header if we're missing one"
    sent_header = False
    for line in fp:
        if line.strip().startswith('['):
            sent_header = True
        if not sent_header and '=' in line:
            sent_header = True
            yield '[jvmctl]\n'
        yield line

def preprocess_env_section(fp):
    "Gather up any export lines and include them in a separate [env] section."
    env_lines = []
    for line in fp:
        if line.startswith('export '):
            env_lines.append(line[len('export '):])
        else:
            yield line
    yield '[env]'
    for line in env_lines:
        yield line

def preprocess(fp):
    """
    Proprocess legacy jettyctl style config files so
    that ConfigParser can cope with them.
    """
    return preprocess_add_header(preprocess_env_section(preprocess_indent(fp)))
 
def parse(fp):
    parser = ConfigParser(delimiters='=', interpolation=ExtendedInterpolation())
    parser.optionxform = str
    parser.read_dict({'jvmctl': {'USER': 'webapp'}})
    parser.read_file(preprocess(fp))
    return parser

def unquote(s):
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    return s

def quote(s):
    return '"%s"' % s if ' ' in s else s

def format_property_options(properties):
    return ' '.join(quote('-D%s=%s' % (k, v)) for k, v in properties.iteritems())

def format_env_block(env):
    return ' '.join(quote('%s=%s' % (k, unquote(v))) for k, v in env.iteritems())

if __name__ == '__main__':
    appname = 'jelly-amber'
    config = parse(open('/opt/jetty/conf/jelly-amber.conf'))
    properties = {'jetty.port': config['jvmctl']['PORT']}
    property_opts = format_property_options(properties)
    cmdline = 'java ' + property_opts
    import sys

