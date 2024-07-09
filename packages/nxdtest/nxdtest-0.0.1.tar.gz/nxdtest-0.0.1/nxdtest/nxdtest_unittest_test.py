# -*- coding: utf-8 -*-
# Copyright (C) 2020  Nexedi SA and Contributors.
#
# This program is free software: you can Use, Study, Modify and Redistribute
# it under the terms of the GNU General Public License version 3, or (at your
# option) any later version, as published by the Free Software Foundation.
#
# You can also Link and Combine this program with other software covered by
# the terms of any of the Free Software licenses or any of the Open Source
# Initiative approved licenses and Convey the resulting work. Corresponding
# source of such a combination shall include the source code for all other
# software used.
#
# This program is distributed WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See COPYING file for full licensing terms.
# See https://www.nexedi.com/licensing for rationale and options.

# verify unittest-related functionality

from nxdtest import _test_result_summary, UnitTest
import pytest
from golang import b

# [] of (name, out, err, summaryok)
testv = []
def case1(name, out, err, summaryok): testv.append((name, out, err, summaryok))

case1('ok', b(''), b("""\
test_1 (test.Test) ... ok
test_2 (test.Test) ... ok
test_3 (test.Test) ... ok

----------------------------------------------------------------------
Ran 3 tests in 1.761s

OK
"""),
'ok\ttestname\t1.761s\t# 3t 0e 0f 0s')


case1('ok+xfail', b(''), b("""\
test_1 (test.Test) ... ok
test_2 (test.Test) ... ok
test_3 (test.Test) ... expected failure

----------------------------------------------------------------------
Ran 3 tests in 1.098s

OK (expected failures=1)
"""),
'ok\ttestname\t1.098s\t# 3t 0e 0f 1s')


case1('fail', b(''), b("""\
test_1 (test.Test) ... ok
test_2 (test.Test) ... ok
test_3 (test.Test) ... FAIL

======================================================================
FAIL: test_3 (test.Test)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/srv/slapgrid/slappart4/srv/project/nxdtest/tmp/test.py", line 14, in test_3
    self.assertEqual(1, 2)
AssertionError: 1 != 2

----------------------------------------------------------------------
Ran 3 tests in 2.198s

FAILED (failures=1)
"""),
'fail\ttestname\t2.198s\t# 3t 0e 1f 0s')


case1('error', b(''), b("""\
test_1 (test.Test) ... ok
test_2 (test.Test) ... ok
test_3 (test.Test) ... ERROR

======================================================================
ERROR: test_3 (test.Test)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/srv/slapgrid/slappart4/srv/project/nxdtest/tmp/test.py", line 14, in test_3
    boom
NameError: name 'boom' is not defined

----------------------------------------------------------------------
Ran 3 tests in 1.684s

FAILED (errors=1)
"""),
'error\ttestname\t1.684s\t# 3t 1e 0f 0s')


case1('error-no-test', b(''), b("""\
usage: python -m unittest discover [-h] [-v] [-q] [--locals] [-f] [-c] [-b]
                                   [-k TESTNAMEPATTERNS] [-s START]
                                   [-p PATTERN] [-t TOP]
python -m unittest discover: error: unrecognized arguments: --argument-error
"""),
'?\ttestname\t1.000s\t# ?t ?e ?f ?s')


case1('error-no-output', b(''), b(''), '?\ttestname\t1.000s\t# ?t ?e ?f ?s')


case1('failed+unexpected_success', b(''), b("""\
test_1 (test.Test) ... ok
test_2 (test.Test) ... ok
test_3 (test.Test) ... unexpected success

----------------------------------------------------------------------
Ran 3 tests in 1.039s

FAILED (unexpected successes=1)
"""),
'fail\ttestname\t1.039s\t# 3t 0e 1f 0s')


case1('mixed-output', b(''), b("""\
----------------------------------------------------------------------
Ran 1 tests in 1.111s

FAILED (failures=1)


----------------------------------------------------------------------
Ran 3 tests in 2.222s

FAILED (failures=3)
"""),
'fail\ttestname\t2.222s\t# 3t 0e 3f 0s')


@pytest.mark.parametrize("name,out,err,summaryok", testv)
def test_unittest_summary(name, out, err, summaryok):
    kw = {'duration': 1.0}
    kw.update(UnitTest.summary(out, err))
    summary = _test_result_summary('testname', kw)
    assert summary == summaryok
