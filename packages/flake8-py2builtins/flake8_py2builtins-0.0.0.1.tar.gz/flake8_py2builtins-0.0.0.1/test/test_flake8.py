from sys import version_info
from pytest import mark
from ast import parse
from flake8_py2builtins.checker import Py2BuiltinsChecker, FLAKE8_PREFIX

def test_positive():
    tree = parse('''
True
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 0

def test_StandardError():
    tree = parse('''
try:
    pass
except StandardError as e:
    pass
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_apply():
    tree = parse('''
apply(int, ['12'])
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_define_apply():
    tree = parse('''
def apply(function, args=None, kwargs={}):
    if args is None: args = []
    if kwargs is None: kwargs = {}
    return function(*args, **kwargs)
apply(int, ['12'])
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 0

def test_basestring():
    tree = parse('''
isinstance('', basestring)
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_buffer():
    tree = parse('''
buffer('')
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_cmp():
    tree = parse('''
cmp(1,2)
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_define_cmp():
    tree = parse('''
def cmp(a, b):
    return (a > b) - (a < b)
cmp(1,2)
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 0

def test_coerce():
    tree = parse('''
coerce(2, 0.3)
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_execfile():
    tree = parse('''
execfile('/dev/null')
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_file():
    tree = parse('''
with open('/dev/null') as f:
    isinstance(f, file)
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_intern():
    tree = parse('''
s = intern('s')
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_import_intern():
    tree = parse('''
from six.moves import intern
s = intern('s')
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 0

def test_long():
    tree = parse('''
long('1')
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_assign_long():
    tree = parse('''
long = int
long('1')
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 0

def test_raw_input():
    tree = parse('''
raw_input()
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_import_raw_input():
    tree = parse('''
from six.moves import input as raw_input
raw_input()
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 0

def test_reduce():
    tree = parse('''
reduce(lambda x,y: x*y, [2,3])
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_import_reduce():
    tree = parse('''
from six.moves import reduce
reduce(lambda x,y: x*y, [2,3])
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 0

def test_reload():
    tree = parse('''
import os
reload(os)
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_import_reload():
    tree = parse('''
from six.moves import reload_module as reload
import os
reload(os)
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 0

def test_unichr():
    tree = parse('''
unichr(1)
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_import_unichr():
    tree = parse('''
from six import unichr
unichr(1)
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 0

def test_unicode():
    tree = parse('''
unicode('a')
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_xrange():
    tree = parse('''
for i in xrange(1): i
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 1
    assert violations[0][2].startswith(FLAKE8_PREFIX)

def test_import_xrange():
    tree = parse('''
from six.moves import range as xrange
for i in xrange(1): i
''')
    violations = list(Py2BuiltinsChecker(tree).run())
    assert len(violations) == 0
