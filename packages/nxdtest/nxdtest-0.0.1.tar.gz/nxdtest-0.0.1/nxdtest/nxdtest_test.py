# -*- coding: utf-8 -*-
# Copyright (C) 2020-2022  Nexedi SA and Contributors.
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

# verify general functionality

import grp
import os
import pwd
import sys
import re
import tempfile
import signal
import shutil
from subprocess import Popen, PIPE
from os.path import dirname, exists
from golang import chan, select, default, func, defer, b
from golang import context, sync, time

import pytest

import nxdtest
from nxdtest import trun


@pytest.fixture
def run_nxdtest(tmpdir):
    """Fixture which returns a function which invokes nxdtest in a temporary
    directory, with the provided .nxdtest file content and with arguments
    passed as `argv`.
    """

    @func
    def _run_nxdtest(nxdtest_file_content, argv=("nxdtest",)):
        with tmpdir.as_cwd():
            with open(".nxdtest", "w") as f:
                f.write(nxdtest_file_content)
            sys_argv = sys.argv
            sys.argv = argv
            def _():
                sys.argv = sys_argv
            defer(_)

            # run nxdtest in thread so that timeout handling works
            # ( if nxdtest is run on main thread, then non-py wait in WorkGroup.wait, if
            #   stuck, prevents signals from being handled at python-level )
            wg = sync.WorkGroup(context.background())
            done = chan()
            @func
            def _(ctx):
                defer(done.close)
                nxdtest.main()
            wg.go(_)

            while 1:
                _, _rx = select(
                            default,    # 0
                            done.recv,  # 1
                )
                if _ == 0:
                    time.sleep(0.1)
                    continue
                wg.wait()
                break

    return _run_nxdtest


# run all tests twice:
# 1) with user namespaces disabled,
# 2) with user namespaces potentially enabled.
@pytest.fixture(autouse=True, params=('userns_disabled', 'userns_default'))
def with_and_without_userns(tmp_path, monkeypatch, request):
    if request.param == 'userns_disabled':
        if request.node.get_closest_marker("userns_only"):
            pytest.skip("test is @userns_only")
        with open(str(tmp_path / 'unshare'), 'w') as f:
            f.write('#!/bin/sh\nexit 1')
        os.chmod(f.name, 0o755)
        monkeypatch.setenv("PATH", str(tmp_path), prepend=os.pathsep)

    else:
        assert request.param == 'userns_default'
        request.node.add_marker(
            pytest.mark.xfail(not userns_works,
                reason="this functionality needs user-namespaces to work"))

# @userns_only marks test as requiring user-namespaces to succeed.
userns_works, _ = trun.userns_available()
userns_only = pytest.mark.userns_only


def test_main(run_nxdtest, capsys):
    run_nxdtest(
        """\
TestCase('TESTNAME', ['echo', 'TEST OUPUT'])
"""
    )

    captured = capsys.readouterr()
    output_lines = captured.out.splitlines()
    assert ">>> TESTNAME" in output_lines
    assert "$ echo TEST OUPUT" in output_lines
    assert "TEST OUPUT" in output_lines
    assert re.match("ok\tTESTNAME\t.*s\t# 1t 0e 0f 0s", output_lines[-2])
    assert re.match(u"# ran 1 test case:  1·ok", output_lines[-1])


def test_command_does_not_exist(run_nxdtest, capsys):
    run_nxdtest(
        """\
TestCase('TESTNAME', ['not exist command'])
"""
    )

    captured = capsys.readouterr()
    assert 'Traceback' not in captured.out
    assert 'Traceback' not in captured.err
    assert captured.err == "not exist command: No such file or directory\n"


def test_command_exit_with_non_zero(run_nxdtest, capsys):
    run_nxdtest(
        """\
TestCase('TESTNAME', ['false'])
"""
    )

    captured = capsys.readouterr()
    assert 'Traceback' not in captured.out
    assert 'Traceback' not in captured.err


def test_error_invoking_summary(run_nxdtest, capsys):
    run_nxdtest(
        """\
TestCase('TESTNAME', ['echo'], summaryf="error")
"""
    )

    captured = capsys.readouterr()
    assert "TypeError" in captured.err


def test_error_execing_nxdtest_file(run_nxdtest, capsys):
    with pytest.raises(ZeroDivisionError) as excinfo:
        run_nxdtest(
        """\
1 / 0
"""
    )
    assert '1 / 0' in str(excinfo.traceback[-1])
    # The actual .nxdtest filename is also included in traceback
    assert ".nxdtest':1" in str(excinfo.traceback[-1])


def test_run_argument(run_nxdtest, capsys):
    run_nxdtest(
        """\
TestCase('TEST1', ['echo', 'TEST1'])
TestCase('TEST2', ['echo', 'TEST2'])
""",
        argv=["nxdtest", "--run", "TEST1"],
    )
    captured = capsys.readouterr()
    assert "TEST1" in captured.out
    assert "TEST2" not in captured.out

    # --run uses search
    run_nxdtest(
        """\
TestCase('TEST1', ['echo', 'TEST1'])
TestCase('TEST2', ['echo', 'TEST2'])
TestCase('TEST10', ['echo', 'TEST10'])
""",
        argv=["nxdtest", "--run", "ST1"],
    )
    captured = capsys.readouterr()
    assert "TEST1" in captured.out
    assert "TEST10" in captured.out
    assert "TEST2" not in captured.out


# verify that nxdtest detects leaked processes.
@pytest.mark.timeout(timeout=10)
def test_run_procleak(run_nxdtest, capsys):
    procleak = "%s/testprog/procleak" % (dirname(__file__),)

    run_nxdtest(
        """\
TestCase('TEST_WITH_PROCLEAK', ['%s', 'AAA', 'BBB', 'CCC'])
"""     % procleak
    )

    captured = capsys.readouterr()
    assert "AAA: terminating" in captured.out
    assert "BBB: terminating" in captured.out
    assert "CCC: terminating" in captured.out


# verify that files leaked on /tmp are detected.
@userns_only
@func
def test_run_tmpleak(run_nxdtest, capsys):
    xtouch = "%s/testprog/xtouch" % (dirname(__file__),)

    tmpd = tempfile.mkdtemp("", "nxdtest-leak.", "/tmp")
    def _():
        shutil.rmtree(tmpd)
    defer(_)

    tmpleakv = list('%s/%d' % (tmpd, i) for i in range(10))
    for f in tmpleakv:
        assert not exists(f)

    run_nxdtest(
        """
TestCase('TESTCASE', ['%s'] + %r)
""" % (xtouch, tmpleakv,)
    )
    captured = capsys.readouterr()

    for f in tmpleakv:
        assert ("# leaked %s" % f) in captured.out
        assert not exists(f)


# verify that leaked mounts are detected.
@userns_only
def test_run_mountleak(run_nxdtest, capsys):
    run_nxdtest(
        """
TestCase('TESTCASE', ['mount', '-t', 'tmpfs', 'none', '/etc'])
""")
    captured = capsys.readouterr()
    assert "# leaked mount: none /etc tmpfs" in captured.out


# verify that inside environment, that nxdtest creates, user/group database is
# minimal.
@userns_only
def test_run_usermap(run_nxdtest, capsys):
    tdumpusergroups = "%s/testprog/tdumpusergroups" % (dirname(__file__),)

    run_nxdtest(
        """
TestCase('TESTCASE', %r)
""" % [tdumpusergroups])
    captured = capsys.readouterr()
    assert captured.err == ''

    # we expect only current user, root and nobody/nogroup to be present
    # disk group should also be present, at least for now, because slapos.core tests need it
    uok = [repr(u) for u in [
        pwd.getpwuid(os.getuid()),
        pwd.getpwnam('root'),
        pwd.getpwnam('nobody')]]
    gok = [repr(g) for g in [
        grp.getgrgid(os.getgid()),
        grp.getgrnam('root'),
        grp.getgrnam('nogroup'),
        grp.getgrnam('disk')]]
    want = '---- 8< ----\n' # XXX won't need this scissors, if we would test trun directly
    for _ in sorted(uok) + sorted(gok):
        want += _+'\n'
    want += '---- 8< ----'

    assert want in captured.out


# verify that inside environment, that nxdtest creates, file permissions are
# still respected.
def test_run_writero(run_nxdtest, capsys):
    twritero = "%s/testprog/twritero" % (dirname(__file__),)

    run_nxdtest(
        """\
TestCase('TESTNAME', ['%s'])
""" % twritero)

    captured = capsys.readouterr()
    output_lines = captured.out.splitlines()
    assert re.match(u"# ran 1 test case:  1·ok", output_lines[-1])


@pytest.fixture
def distributor_with_cancelled_test(mocker):
    """A distributor for a test result with one test result line named TEST1.

    test_result.isAlive() will return False after 2 invocations, to simulate
    a test_result that was cancelled by distributor.
    """
    def _retryRPC(func_id, args=()):
        if func_id == 'getProtocolRevision':
            return 1
        assert False, ('unexpected RPC call', (func_id, args))
    mocker.patch(
        'erp5.util.taskdistribution.RPCRetry._retryRPC',
        side_effect=_retryRPC)

    test_result_line_proxy = mocker.patch(
        'erp5.util.taskdistribution.TestResultLineProxy',
        autospec=True)
    type(test_result_line_proxy).name = mocker.PropertyMock(return_value='TEST1')

    test_result_proxy = mocker.patch(
        'erp5.util.taskdistribution.TestResultProxy',
        autospec=True)
    test_result_proxy.start.side_effect = [test_result_line_proxy, None]
    test_result_proxy.isAlive.side_effect = [True, True, False]

    mocked_createTestResult = mocker.patch(
        'erp5.util.taskdistribution.TaskDistributor.createTestResult',
        return_value=test_result_proxy)

    yield

    mocked_createTestResult.assert_called_once()
    test_result_proxy.start.assert_called()
    test_result_proxy.isAlive.assert_called()
    test_result_line_proxy.stop.assert_called()


# verify that nxdtest cancels test run when master reports that test_result is no longer alive.
@pytest.mark.timeout(timeout=10)
def test_cancel_from_master(run_nxdtest, capsys, distributor_with_cancelled_test, mocker):
    # nxdtest polls every 5 minutes, but in test we don't want to wait so long.
    # set master poll interval to small, but enough time for spawned hang to
    # setup its signal handler.
    mocker.patch('nxdtest._tmasterpoll', 1*time.second)

    hang = "%s/testprog/hang" % (dirname(__file__),)
    run_nxdtest(
        """\
TestCase('TEST1', ['%s'])
""" % (hang),
        argv=[
            "nxdtest",
            "--master_url", "http://localhost",
        ],
    )
    captured = capsys.readouterr()
    assert "TEST1" in captured.out
    assert "# master asks to cancel test run" in captured.out
    assert "# test run canceled" in captured.out
    assert "hang: terminating" in captured.out
    assert "leaked pid" not in captured.out
    assert u"ran 1 test case:  1·error" in captured.out
    assert captured.err == ''


# verify that nxdtest cancels test run on SIGINT/SIGTERM.
#@pytest.mark.timeout(timeout=10)
@pytest.mark.timeout(timeout=3)
@pytest.mark.parametrize('sig', [(signal.SIGINT, "Interrupt"), (signal.SIGTERM, "Terminate")])
@func
def test_cancel_from_signal(tmpdir, sig):
    hang = "%s/testprog/hang" % (dirname(__file__),)

    with tmpdir.as_cwd():
        with open(".nxdtest", "w") as f:
            f.write("""\
TestCase('TEST1', ['%s'])
""" % hang)

        proc = Popen([sys.executable, "%s/__init__.py" % dirname(nxdtest.__file__)], stdout=PIPE)
        def _():
            proc.terminate()
            if proc.poll() is None:
                time.sleep(1)
                proc.kill()
            proc.wait()
        defer(_)

        # procreadline reads next line from proc stdout.
        outv = []
        def procreadline():
            l = proc.stdout.readline()
            if len(l) != 0: # EOF
                outv.append(l)
            return l

        # wait for hang to start and setup its signal handler
        while 1:
            l = procreadline()
            if not l:
                raise AssertionError("did not got 'hanging'")
            if b"hanging" in l:
                break

        # send SIGINT/SIGTERM to proc and wait for it to complete
        signo, sigmsg = sig
        proc.send_signal(signo)
        while 1:
            if not procreadline():
                break

        out = b''.join(outv)

        assert b"TEST1" in out
        assert b("# %s" % sigmsg) in out
        assert b"# test run canceled" in out
        assert b"hang: terminating" in out
        assert b"leaked pid" not in out
        assert b("ran 1 test case:  1·error") in out
