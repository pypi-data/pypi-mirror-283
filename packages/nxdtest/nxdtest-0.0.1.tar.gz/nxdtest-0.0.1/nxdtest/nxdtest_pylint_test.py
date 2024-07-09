# -*- coding: utf-8 -*-
# Copyright (C) 2021  Nexedi SA and Contributors.
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

# verify pylint-related functionality

from nxdtest import _test_result_summary, PyLint
import pytest
from golang import b

# [] of (name, out, err, summaryok)
testv = []
def case1(name, out, err, summaryok): testv.append((name, out, err, summaryok))


case1('multiple-messages', b("""\
************* Module nxdtest
nxdtest/__init__.py:411:4: E0001: invalid syntax (<unknown>, line 411) (syntax-error)
************* Module nxdtest.nxdtest_test
nxdtest/nxdtest_test.py:27:0: E0001: Cannot import 'nxdtest' due to syntax error 'invalid syntax (<unknown>, line 411)' (syntax-error)
************* Module nxdtest.nxdtest_pylint_test
nxdtest/nxdtest_pylint_test.py:22:0: E0001: Cannot import 'nxdtest' due to syntax error 'invalid syntax (<unknown>, line 411)' (syntax-error)
************* Module nxdtest.nxdtest_unittest_test
nxdtest/nxdtest_unittest_test.py:22:0: E0001: Cannot import 'nxdtest' due to syntax error 'invalid syntax (<unknown>, line 411)' (syntax-error)
************* Module nxdtest.nxdtest_pytest_test
nxdtest/nxdtest_pytest_test.py:22:0: E0001: Cannot import 'nxdtest' due to syntax error 'invalid syntax (<unknown>, line 411)' (syntax-error)

------------------------------------------------------------------
Your code has been rated at 7.16/10 (previous run: 9.85/10, -2.69)

"""),
b(''),
'error\ttestname\t1.000s\t# 1t 5e 0f 0s')


case1('one-message', b("""\
************* Module nxdtest
nxdtest/__init__.py:89:4: E0213: Method should have "self" as first argument (no-self-argument)

------------------------------------------------------------------
Your code has been rated at 9.85/10 (previous run: 9.69/10, +0.15)
"""),
b(''),
'error\ttestname\t1.000s\t# 1t 1e 0f 0s')


case1('no-messages', b("""\

-------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 7.16/10, +2.84)

"""),
b(''),
'ok\ttestname\t1.000s\t# 1t 0e 0f 0s')


case1('invocation-error', b(''),
b('Something went really wrong'),
'?\ttestname\t1.000s\t# ?t ?e 0f 0s')


@pytest.mark.parametrize("name,out,err,summaryok", testv)
def test_pylint_summary(name, out, err, summaryok):
    kw = {'duration': 1.0}
    kw.update(PyLint.summary(out, err))
    summary = _test_result_summary('testname', kw)
    assert summary == summaryok
