#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018-2022  Nexedi SA and Contributors.
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
"""nxdtest - tox-like tool to run tests under Nexedi testing infrastructure(*).

Nxdtest runs tests defined by .nxdtest file.
A project defines set of tests cases to verify itself in that file.
.nxdtest file is Python program executed in special environment described below.

Test cases are declared with `TestCase`. Each test case specifies:

- its name,
- a program to run,
- (optionally) an environment for the run,
- (optionally) a summary function to extract summary from test output.

For example the following .nxdtest defines 3 test cases that run Wendelin.core
`test.py` tests with FileStorage, ZEO and NEO as database backend::

    for stor in ['fs1', 'zeo', 'neo']:
        TestCase('test.py/%s' % stor, ['make', 'test.py'],
                 envadj={'WENDELIN_CORE_TEST_DB': '<%s>' % stor,
                 summaryf=PyTest.summary)

Nxdtest only runs tests, but - unlike tox - does not prepare variants of
software build. Nxdtest assumes that the software build is already fully
prepared. This matches SlapOS environment, where software building is separate
step handled by SlapOS.

(*) https://www.erp5.com/NXD-Presentation.ci.testing.system.buildout
    https://www.erp5.com/erp5-Guideline.Nexedi.Testing.Extended
    https://stack.nexedi.com/test_status

Local mode
----------

Tests are run locally if --master_url option is not specified.
"""

from __future__ import print_function, absolute_import

from erp5.util.taskdistribution import TaskDistributor
from subprocess import Popen, PIPE
from time import strftime, gmtime, localtime
import os, sys, argparse, logging, traceback, re, pwd, socket
from os.path import dirname
import six
from golang import b, chan, defer, func, go, select, default
from golang import errors, context, os as gos, sync, syscall, time
from golang.os import signal

# trun.py is a helper via which we run tests.
trun_py = "%s/trun.py" % dirname(__file__)

# loadNXDTestFile loads .nxdtest file located @path.
def loadNXDTestFile(path): # -> TestEnv
    t = TestEnv()
    g = {'TestCase': t.TestCase,    # TODO + all other public TestEnv methods
         'PyTest':   PyTest,
         'PyLint': PyLint,
         'UnitTest': UnitTest,}
    with open(path, "r") as f:
        src = f.read()
    six.exec_(compile(src, os.path.realpath(path), 'exec'), g)
    return t

# TestCase defines one test case to run.
class TestCase:
    def __init__(self, name, argv, summaryf=None, **kw):
        self.name = name            # testcase name
        self.argv = argv            # program to run
        self.kw   = kw              # **kw is passed to Popen
        self.summaryf = summaryf    # function to extract summary from test output

    # command_str returns string representation of the command that test case runs.
    # it returns something like 'make test.py # WENDELIN_CORE_TEST_DB=<fs>'
    def command_str(t):
        eadj = t.kw.get('envadj', {})
        sadj = ' '.join(['%s=%s' % (k,eadj[k]) for k in sorted(eadj.keys())])
        return '%s%s' % (' '.join(t.argv), ' # '+sadj if sadj else '')

# TestEnv represents a testing environment with set of TestCases to run.
class TestEnv:
    def __init__(self):
        self.byname = {} # name -> TestCase
        self.testv  = [] # of TestCase

    # TestCase adds new test case to the environment.
    def TestCase(self, name, argv, **kw):
        assert name not in self.byname
        t = TestCase(name, argv, **kw)
        self.testv.append(t)
        self.byname[name] = t

def emit(*message):
  """Emit a message on stdout and flush output.
  """
  print(*message)
  sys.stdout.flush()

# interval we will poll master periodically for test_alive.isAlive.
# NOTE it is not e.g. one second not to overload master.
_tmasterpoll = 5*time.minute

@func
def main():
    # testnode executes us giving URL to master results collecting instance and other details
    # https://lab.nexedi.com/nexedi/erp5/blob/744f3fde/erp5/util/testnode/UnitTestRunner.py#L137
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--master_url', help='The URL of Master controlling many suites (local run if not specified)')
    parser.add_argument('--revision', help='The revision to test', default='dummy_revision')
    parser.add_argument('--test_suite', help='The test suite name')
    parser.add_argument('--test_suite_title', help='The test suite title')
    parser.add_argument('--test_node_title', help='The test node title')
    parser.add_argument('--project_title', help='The project title')

    parser.add_argument('--verbose', action='store_true', help='increase output verbosity')

    local = parser.add_argument_group('local run')
    local.add_argument('-l', '--list', action='store_true', help='Only list tests')
    local.add_argument('-k', '--run',  help='Run only tests whose names match provided expression')

    args = parser.parse_args()
    if args.master_url is not None:
        if args.list or args.run:
            print('E: local options can be used only without --master_url', file=sys.stderr)
            sys.exit(2)

    # if verbose -> log to stderr
    logger = None
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger()

    # load list of tests to run
    tenv = loadNXDTestFile('.nxdtest')

    # --list
    if args.list:
        for t in tenv.testv:
            emit(t.name)
        return

    # log information about local node
    system_info()

    # emit run summary at the end
    summaryv = [] # of summary line for each ran testcase
    def _():
        stat = {} # st -> count
        for line in summaryv:
            st, _ = line.split(None, 1) # 'ok testname ...' -> 'ok'
            stat[st] = stat.get(st, 0) + 1

        s = '# ran %d test case' % len(summaryv)
        if len(summaryv) == 0:
            s += 's.'
        else:
            if len(summaryv) > 1:
                s += 's'
            s += ':'
            # ok, fail, error go in that order
            for st in ('ok', 'fail', 'error') + tuple(stat.keys()):
                n = stat.pop(st, 0)
                if n != 0:
                    s += '  %d·%s' % (n, st)
        emit(s)
    defer(_)

    # master_url provided -> run tests under master control
    if args.master_url is not None:
        # connect to master and create 'test result' object with list of tests to run
        tool = TaskDistributor(portal_url = args.master_url, logger = logger)
        test_result = tool.createTestResult(
                        revision        = args.revision,
                        test_name_list  = [t.name for t in tenv.testv],
                        node_title      = args.test_node_title,
                        test_title      = args.test_suite_title or args.test_suite,
                        project_title   = args.project_title)

        if test_result is None:
            # a test run for given name and revision has already been completed
            emit("# master says: nothing to run")
            return

        emit("# running for %s" % test_result.test_result_path)

    # master_url not provided -> run tests locally
    else:
        emit("# local mode")
        test_result = LocalTestResult(tenv, run=args.run)

    # make sure we get output from subprocesses without delay.
    # go does not buffer stdout/stderr by default, but python does for stdout.
    # tell python not to buffer anything.
    os.environ['PYTHONUNBUFFERED'] = 'y'

    if sys.version_info < (3,):
      bstdout = sys.stdout
      bstderr = sys.stderr
    else:
      bstdout = sys.stdout.buffer
      bstderr = sys.stderr.buffer


    # setup main context that is canceled on SIGINT/SIGTERM
    # we will use this context as the base for all spawned jobs
    ctx, cancel = context.with_cancel(context.background())
    sigq = chan(1, dtype=gos.Signal)
    signal.Notify(sigq, syscall.SIGINT, syscall.SIGTERM)
    def _():
        signal.Stop(sigq)
        sigq.close()
    defer(_)
    def _(cancel):
        sig, ok = sigq.recv_()
        if not ok:
            return
        emit("# %s" % sig)
        cancel()
    go(_, cancel)
    defer(cancel)

    # adjust ctx to be also canceled when/if test_result is canceled on master
    ctx, cancel = context.with_cancel(ctx)
    cancelWG = sync.WorkGroup(ctx)
    @func
    def _(ctx, cancel):
        defer(cancel)
        while 1:
            _, _rx = select(
                    ctx.done().recv,                # 0
                    time.after(_tmasterpoll).recv,  # 1
            )
            if _ == 0:
                break

            if not test_result.isAlive():
                emit("# master asks to cancel test run")
                break
    cancelWG.go(_, cancel)
    defer(cancelWG.wait)
    defer(cancel)

    # run the tests
    devnull = open(os.devnull)
    while 1:
        if ctx.err() is not None:
            emit("# test run canceled")
            break

        # ask master for next test to run; stop if no more.
        test_result_line = test_result.start()
        if test_result_line is None:
            break

        # run tenv[name]
        t = tenv.byname[test_result_line.name]
        tstart = time.now()

        emit('\n>>> %s' % t.name)
        emit('$ %s' % t.command_str())

        # default status dict
        status = {
            'test_count':       1,
            'error_count':      0,
            'failure_count':    0,
            'skip_count':       0,
            #html_test_result
        }

        try:
            # Run t.argv in t.kw['env'] environment.
            # In addition to kw['env'], kw['envadj'] allows users to define
            # only adjustments instead of providing full env dict.
            # Test command is spawned with unchanged cwd. Instance wrapper cares to set cwd before running us.
            # The test is run via trun.py helper to which we delegate checking
            # for leaked files/processes/mounts/... We trust trun.py not to hang.
            kw = t.kw.copy()
            env = kw.pop('env', os.environ)
            env = env.copy()
            envadj = kw.pop('envadj', {})
            env.update(envadj)
            p = Popen([sys.executable, trun_py] + t.argv, env=env, stdin=devnull, stdout=PIPE, stderr=PIPE, bufsize=0, **kw)
        except:
            stdout, stderr = b'', b(traceback.format_exc())
            bstderr.write(stderr)
            status['error_count'] += 1
        else:
            # tee >stdout,stderr so we can also see in testnode logs
            # (explicit teeing instead of p.communicate() to be able to see incremental progress)
            buf_out = []
            buf_err = []
            wg = sync.WorkGroup(ctx)
            wg.go(tee, p.stdout, bstdout, buf_out)
            wg.go(tee, p.stderr, bstderr, buf_err)
            # wait for trun to exit; terminate it on cancel
            @func
            def _(ctx):
                defer(p.wait)
                err = None
                while 1:
                    done = p.poll()
                    if done is not None:
                        break

                    # cancel -> terminate p
                    _, _rx = select(
                            default,            # 0
                            ctx.done().recv,    # 1
                    )
                    if _ == 1:
                        emit("# stopping due to cancel")
                        p.terminate()
                        err = ctx.err()
                        break

                    time.sleep(0.1)

                if err is not None:
                    raise err
            wg.go(_)

            try:
                wg.wait()
            except Exception as e:
                if errors.Is(e, context.canceled):
                    pass # ok, finish current test_result_line
                else:
                    raise

            stdout = b''.join(buf_out)
            stderr = b''.join(buf_err)

            if p.returncode != 0:
                status['error_count'] += 1

            # postprocess output, if we can
            if t.summaryf is not None:
                try:
                    summary = t.summaryf(stdout, stderr)
                except:
                    bad = b(traceback.format_exc())
                    bstderr.write(bad)
                    stderr += bad
                    status['error_count'] += 1

                else:
                    status.update(summary)


        tend = time.now()

        # print summary and report result of test run back to master
        tres = {
            'command':  t.command_str(),
            'duration': tend - tstart,
            'date':     strftime("%Y/%m/%d %H:%M:%S", gmtime(tend)),

            'stdout':   stdout,
            'stderr':   stderr,
        }
        tres.update(status)

        _ = _test_result_summary(t.name, tres)
        summaryv.append(_)
        emit(_)
        test_result_line.stop(**tres)

# tee, similar to tee(1) utility, copies data from fin to fout appending them to buf.
def tee(ctx, fin, fout, buf):
    while 1:
        # poll for cancellation periodically and stop if requested.
        # FIXME handle ↓↓↓ os.read and .write in non-blocking way so that we
        # are not stuck in case ctx is cancelled but we remain blocked in any of those calls.
        e = ctx.err()
        if e is not None:
            raise e

        # NOTE use raw os.read because it does not wait for full data to be available.
        # ( we could use fin.readline(), but there are cases when e.g. progress
        #   is reported via printing consequent dots on the same line and
        #   readline() won't work for that.
        #
        #   besides when a lot of output is available it would be a waste to
        #   read/flush it line-by-line. )
        data = os.read(fin.fileno(), 4096)
        if not(data):
            return  # EOF

        fout.write(data)
        fout.flush()
        buf.append(data)


# _test_result_summary returns one-line summary for test result.
# it returns something like 'ok # 100t 3f'
# **kw is what is passed to test_result_line.stop().
def _test_result_summary(name, kw):
    def v(name):
        return kw.get(name, '?')

    _ = v('error_count')
    if _ == '?':
        st = '?'
    elif _ != 0:
        st = 'error'
    else:
        _ = v('failure_count')
        if _ == '?':
            st = '?'
        elif _ != 0:
            st = 'fail'
        else:
            st = 'ok'

    return '%s\t%s\t%.3fs\t# %st %se %sf %ss' % (st, name, kw['duration'], v('test_count'), v('error_count'), v('failure_count'), v('skip_count'))


# system_info prints information about local computer.
def system_info():
    emit('date:\t%s' % (strftime("%a, %d %b %Y %H:%M:%S %Z", localtime())))
    whoami = pwd.getpwuid(os.getuid()).pw_name
    emit('xnode:\t%s@%s' % (whoami, socket.getfqdn()))
    emit('uname:\t%s' % ' '.join(os.uname()))
    cpu = get1('/proc/cpuinfo', 'model name', None) # e.g. no 'model name' on riscv
    isa = get1('/proc/cpuinfo', 'isa', None)        # present on riscv, but not on x86
    if cpu:
        emit('cpu:\t%s' % cpu)
    if isa:
        emit('isa:\t%s' % isa)

# get1 returns first entry from file @path prefixed with ^<field>\s*:
_nodefault = object()
def get1(path, field, default=_nodefault):
    with open(path, 'r') as f:
        data = f.read()
    rex = re.compile(r'^%s\s*:\s*(.*)$' % field)
    for l in data.splitlines():
        m = rex.match(l)
        if m is not None:
            return m.group(1)
    if default is not _nodefault:
        return default
    raise KeyError('%s does not have field %r' % (path, field))



# LocalTestResult* handle tests runs, when master_url was not provided and tests are run locally.
class LocalTestResult:
    def __init__(self, tenv, run=None):
        assert isinstance(tenv, TestEnv)
        self.tenv = tenv
        self.next = 0   # tenv.testv[next] is next test to consider executing
        self.run  = run # None | re to filter which tests to execute

    def start(self): # -> test_result_line
        while 1:
            if self.next >= len(self.tenv.testv):
                return None # all tests are done

            t = self.tenv.testv[self.next]
            self.next += 1

            # --run
            if self.run is not None and not re.search(self.run, t.name):
                continue

            test_result_line = LocalTestResultLine()
            test_result_line.name = t.name
            return test_result_line

    def isAlive(self): # -> bool (whether still running)
        return True # don't need to handle SIGINT - CTRL+C interrupts whole process

class LocalTestResultLine:
    def stop(self, **kw):
        # XXX + dump .json ?
        pass


# support for well-known summary functions
class PyTest:
    @staticmethod
    def summary(out, err): # -> status_dict
        # end of output is like
        # ================ 1 failed, 1 passed, 12 skipped in 0.39 seconds ================
        # ...
        textv = out.splitlines()
        for l in reversed(textv):
            if re.match(br'^====* .*(failed|passed|skipped|error|no tests).* ====*$', l):
                pytail = l
                break
        else:
            return {}

        def get(name, default=None):
            m = re.search(br'\b([0-9]+) ' + name.encode() + br'\b', pytail)
            if m is None:
                return default
            return int(m.group(1))

        stat = {'test_count': 0}
        def stat_set(stat_key, from_name):
            v = get(from_name, 0)
            stat[stat_key] = v
            stat['test_count'] += v
        stat_set('skip_count', 'skipped')
        stat_set('failure_count', 'failed')
        stat_set('expected_failures', 'xfailed')
        stat_set('unexpected_successes', 'xpassed')
        stat_set('error_count', 'error')
        stat['test_count'] += get('passed',  0)
        return stat


class UnitTest:

    @staticmethod
    def summary(out, err): # -> status_dict
        run_re = re.compile(
            br'.*Ran (?P<all_tests>\d+) tests? in (?P<seconds>\d+\.\d+)s',
            re.DOTALL)
        status_re = re.compile(br"""
              .*(OK|FAILED)\s+\(
                (failures=(?P<failures>\d+),?\s*)?
                (errors=(?P<errors>\d+),?\s*)?
                (skipped=(?P<skips>\d+),?\s*)?
                (expected\s+failures=(?P<expected_failures>\d+),?\s*)?
                (unexpected\s+successes=(?P<unexpected_successes>\d+),?\s*)?
              \)
              """, re.DOTALL | re.VERBOSE)

        status_dict = {
        }
        run = run_re.search(err)
        if run:
            groupdict = run.groupdict()
            status_dict.update(
                duration=float(groupdict['seconds']),
                test_count=int(groupdict['all_tests']),
                error_count=0,
                failure_count=0,
                skip_count=0,
            )
        status = status_re.search(err)
        if status:
            groupdict = status.groupdict()
            status_dict.update(
                error_count=int(groupdict.get('errors') or 0),
                failure_count=int(groupdict.get('failures') or 0)
                              + int(groupdict.get('unexpected_successes') or 0),
                skip_count=int(groupdict.get('skips') or 0)
                           + int(groupdict.get('expected_failures') or 0))
        return status_dict


class PyLint:

    @staticmethod
    def summary(out, err): # -> status_dict
        test_count = 1
        error_count = 0
        if err:
            test_count = error_count = '?'
        else:
            message_re = re.compile(br'^.*:[\d]+:[\d]+: .+: .*')
            for line in out.splitlines():
                if message_re.match(line):
                    error_count += 1
        return {
            'test_count': test_count,
            'error_count': error_count,
            'failure_count': 0,
            'skip_count': 0,
        }


if __name__ == '__main__':
    main()
