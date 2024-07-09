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

# verify pytest-related functionality

from nxdtest import _test_result_summary, PyTest
import pytest
from golang import b

# [] of (name, out, err, summaryok)
testv = []
def case1(name, out, err, summaryok): testv.append((name, out, err, summaryok))

case1('ok', b("""\
============================== test session starts ===============================
platform linux -- Python 3.7.7, pytest-4.6.11, py-1.9.0, pluggy-0.13.1
rootdir: /srv/slapgrid/slappart15/srv/runner/software/104d3d67a7dca200da22b97280c85eb6/parts/nxdtest, inifile: pytest.ini
plugins: timeout-1.4.2, mock-2.0.0
collected 1 item

test.py .                                                                  [100%]

============================ 1 passed in 0.01 seconds ============================
"""),
b(''),
'ok\ttestname\t1.000s\t# 1t 0e 0f 0s')

case1('ok+xfail', b("""\
============================= test session starts ==============================
platform linux2 -- Python 2.7.18, pytest-4.6.11, py-1.9.0, pluggy-0.13.1
rootdir: /srv/slapgrid/slappart9/srv/testnode/dfq/soft/46d349541123ed5fc6ceea58fd013a51/parts/zodbtools-dev
collected 43 items

zodbtools/test/test_analyze.py .                                         [  2%]
zodbtools/test/test_commit.py .x                                         [  6%]
zodbtools/test/test_dump.py .x.                                          [ 13%]
zodbtools/test/test_tidrange.py .............................            [ 81%]
zodbtools/test/test_zodb.py ........                                     [100%]

=============== 41 passed, 2 xfailed, 1 warnings in 4.62 seconds ===============
"""),
b(''),
'ok\ttestname\t1.000s\t# 43t 0e 0f 0s')

case1('ok+fail', b("""\
============================= test session starts ==============================
platform linux2 -- Python 2.7.18, pytest-4.6.11, py-1.9.0, pluggy-0.13.1
rootdir: /srv/slapgrid/slappart16/srv/testnode/dfj/soft/8b9988ce0aa31334c6bd56b40e4bba65/parts/pygolang-dev
collected 112 items

golang/_gopath_test.py ..                                                [  1%]
golang/context_test.py ..                                                [  3%]
golang/cxx_test.py ..                                                    [  5%]
golang/errors_test.py ........                                           [ 12%]
golang/fmt_test.py ...                                                   [ 15%]
golang/golang_test.py ................................................   [ 58%]
golang/io_test.py .                                                      [ 58%]
golang/strconv_test.py ..                                                [ 60%]
golang/strings_test.py .....                                             [ 65%]
golang/sync_test.py .............                                        [ 76%]
golang/time_test.py ...F....                                             [ 83%]
golang/pyx/build_test.py ...                                             [ 86%]
golang/pyx/runtime_test.py .                                             [ 87%]
gpython/gpython_test.py ssssss.sssssss                                   [100%]

=================================== FAILURES ===================================
__________________________________ test_timer __________________________________

    def test_timer():
        # start timers at x5, x7 and x11 intervals an verify that the timers fire
        # in expected sequence. The times when the timers fire do not overlap in
        # checked range because intervals are prime and chosen so that they start
        # overlapping only after 35 (=5·7).
        tv = [] # timer events
        Tstart = time.now()

        t23 = time.Timer(23*dt)
        t5  = time.Timer( 5*dt)

        def _():
            tv.append(7)
            t7f.reset(7*dt)
        t7f = time.Timer( 7*dt, f=_)

        tx11 = time.Ticker(11*dt)

        while 1:
            _, _rx = select(
                t23.c.recv,     # 0
                t5 .c.recv,     # 1
                t7f.c.recv,     # 2
                tx11.c.recv,    # 3
            )
            if _ == 0:
                tv.append(23)
                break
            if _ == 1:
                tv.append(5)
                t5.reset(5*dt)
            if _ == 2:
                assert False, "t7f sent to channel; must only call func"
            if _ == 3:
                tv.append(11)

        Tend = time.now()
        assert (Tend - Tstart) >= 23*dt
>       assert tv == [        5,  7,     5, 11,       7, 5,             5, 7,11,23]
E       assert [5, 7, 5, 11, 5, 7, ...] == [5, 7, 5, 11, 7, 5, ...]
E         At index 4 diff: 5 != 7
E         Use -v to get the full diff

golang/time_test.py:106: AssertionError
=============== 1 failed, 98 passed, 13 skipped in 26.85 seconds ===============
"""),
b(''),
'fail\ttestname\t1.000s\t# 112t 0e 1f 13s')

case1('notest', b("""\
============================= test session starts ==============================
platform linux -- Python 3.7.7, pytest-4.6.11, py-1.9.0, pluggy-0.13.1
rootdir: /srv/slapgrid/slappart15/srv/runner/software/104d3d67a7dca200da22b97280c85eb6/parts/nxdtest, inifile: pytest.ini
plugins: timeout-1.4.2, mock-2.0.0
collected 0 items

========================= no tests ran in 0.01 seconds =========================
"""),
b(''),
'ok\ttestname\t1.000s\t# 0t 0e 0f 0s')

case1('error', b("""\
============================= test session starts ==============================
platform linux -- Python 3.7.7, pytest-4.6.11, py-1.9.0, pluggy-0.13.1
rootdir: /srv/slapgrid/slappart15/srv/runner/software/104d3d67a7dca200da22b97280c85eb6/parts/nxdtest, inifile: pytest.ini
plugins: timeout-1.4.2, mock-2.0.0
collected 0 items / 2 errors                                                   

==================================== ERRORS ====================================
_________________________ ERROR collecting tmp/test.py _________________________
ImportError while importing test module 'tmp/test.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
test.py:4: in <module>
    import error
E   ModuleNotFoundError: No module named 'error'
________________________ ERROR collecting tmp/test2.py _________________________
ImportError while importing test module 'tmp/test2.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
test2.py:4: in <module>
    import error
E   ModuleNotFoundError: No module named 'error'
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
=========================== 2 error in 0.11 seconds ============================
"""),
b(''),
'error\ttestname\t1.000s\t# 2t 2e 0f 0s')

case1('ok+tailtext', b("""\
date:   Sun, 08 Nov 2020 12:26:24 MSK
xnode:  kirr@deco.navytux.spb.ru
uname:  Linux deco 5.9.0-1-amd64 #1 SMP Debian 5.9.1-1 (2020-10-17) x86_64
cpu:    Intel(R) Core(TM) i7-6600U CPU @ 2.60GHz

>>> test.py/fs-wcfs:
$ make test.py # GOMAXPROCS= WENDELIN_CORE_TEST_DB=<fs> WENDELIN_CORE_VIRTMEM=r:wcfs+w:uvmm
...
==================== 54 passed, 1 xpassed in 13.47 seconds =====================
# unmount/stop wcfs pid39670 @ /tmp/wcfs/cff0a836e51839ee7b10ba76277c639fe11bdb11
wcfs: 2020/11/08 12:26:38 /tmp/testdb_fs.Z9IvT0/1.fs: watcher: stat /tmp/testdb_fs.Z9IvT0/1.fs: use of closed file
# unmount/stop wcfs pid39653 @ /tmp/wcfs/40cc7154ed758d6a867205e79e320c1d3b56458d
wcfs: 2020/11/08 12:26:38 /tmp/testdb_fs.B3rbby/1.fs: watcher: stat /tmp/testdb_fs.B3rbby/1.fs: use of closed file
# unmount/stop wcfs pid39595 @ /tmp/wcfs/d0b5d036a2cce47fe73003cf2d9f0b22c7043817
==== aaa bbb ====
"""),
b(''),
'ok\ttestname\t1.000s\t# 55t 0e 0f 0s')


@pytest.mark.parametrize("name,out,err,summaryok", testv)
def test_pytest_summary(name, out, err, summaryok):
    kw = {'duration': 1.0}
    kw.update(PyTest.summary(out, err))
    summary = _test_result_summary('testname', kw)
    assert summary == summaryok
