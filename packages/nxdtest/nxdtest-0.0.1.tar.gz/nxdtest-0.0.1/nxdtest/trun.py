#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2021-2022  Nexedi SA and Contributors.
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
""" `trun ...` - run test specified by `...`

The test is run in dedicated environment, which, after test completes, is
checked for leaked files, leaked mount entries, leaked processes, etc.

The environment is activated only if user namespaces are available(*).
If user namespaces are not available, the test is still run but without most of the checks.

(*) see https://man7.org/linux/man-pages/man7/user_namespaces.7.html
"""

from __future__ import print_function, absolute_import

import errno, os, sys, stat, difflib, pwd, grp, shutil
from subprocess import check_call as xrun, CalledProcessError, Popen
from os.path import join, devnull
from golang import func, defer, chan, select, default
from golang import os as gos, syscall, time
from golang.os import signal
import prctl
import psutil

# userns_available detects if user-namespaces and necessary features are provided by OS kernel.
def userns_available(): # -> (yes|no, {details})
    have = {"userns": False, "userns/fuse": False}

    try:
        # check if user namespaces are available
        with open(devnull, "w") as null:
            xrun(["unshare"] + _unshare_argv + ["true"], stdout=null, stderr=null)
    except (OSError, CalledProcessError):
        pass
    else:
        have["userns"] = True

    if have["userns"]:
        # check if FUSE works inside user namespaces.
        # Using FUSE inside user namespaces requires Linux >= 4.18 (see
        # https://git.kernel.org/linus/da315f6e0398 and
        # https://git.kernel.org/linus/8cb08329b080). For simplicity we check
        # for that kernel version instead of actually trying to mount a test
        # FUSE filesystem.
        sysname, _, release, _, _ = os.uname()
        if sysname == "Linux":
            major, minor, _ = release.split('.', 2) # 5.10.0-9-amd64 -> 5 10 0-9-amd64
            version = (int(major), int(minor))
            if version >= (4, 18):
                have["userns/fuse"] = True

    ok = True
    for _, haveit in have.items():
        if not haveit:
            ok = False
    return (ok, have)


_unshare_argv = ["-Umc", "--keep-caps"]
def main():
    # Try to respawn ourselves in user-namespace where we can mount things, e.g. new /tmp.
    # Keep current uid/gid the same for better traceability. In other words current user
    # stays the same. Activate ambient capabilities(*) so that mounting filesystems,
    # including FUSE-based ones for wendelin.core, still works under regular non-zero uid.
    #
    # (*) see https://man7.org/linux/man-pages/man7/capabilities.7.html
    #     and git.kernel.org/linus/58319057b784.
    in_userns = True
    mypid = str(os.getpid())
    _ = os.environ.get("_NXDTEST_TRUN_RESPAWNED", "")
    if mypid != _:
        userns_works, details = userns_available()
        if not userns_works:
            in_userns = False
            details_str = [] # of +feat, -feat
            for feat, haveit in details.items():
                details_str.append('%s%s' % ('+' if haveit else '-', feat))
            print("# user namespaces not available (%s)." % " ".join(details_str))
            print("# isolation and many checks will be deactivated.")
        else:
            os.environ["_NXDTEST_TRUN_RESPAWNED"] = mypid
            os.execvp("unshare", ["unshare"] + _unshare_argv + [sys.executable] + sys.argv)
            raise AssertionError("unreachable")

    # either respawned in new namespace, or entered here without respawn with in_userns=n.
    # run the test via corresponding driver.
    run = run_in_userns if in_userns else run_no_userns
    @func
    def _():
        try:
            # run the command in a new session, so that it is easy to find out leaked spawned subprocesses.
            # TODO session -> cgroup, because a child process could create another new session.
            def newsession():
                os.setsid()
            p = Popen(sys.argv[1:], preexec_fn=newsession)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
            #print(e.strerror, file=sys.stderr)   # e.strerror does not include filename on py2
            print("%s: %s" % (sys.argv[1], os.strerror(e.errno)), # e.filename is also ø on py2
                    file=sys.stderr)
            sys.exit(127)

        def _():
            p.wait()
            sys.exit(p.returncode)
        defer(_)

        # in the end: check if p leaked processes and terminate/kill them
        # kill p in the end if it does not stop from just SIGTERM.
        def _():
            while 1:
                procv = session_proclist(sid=p.pid)
                if len(procv) == 0:
                    break
                for proc in procv:
                    if proc.pid != p.pid:
                        print('# leaked pid=%d %r %s' % (proc.pid, proc.name(), proc.cmdline()))
                        proc.terminate()
                gone, alive = psutil.wait_procs(procv, timeout=5)
                for proc in gone:
                    if proc.pid == p.pid:
                        # waitpid(pid=p.pid) done.
                        # Propagate returncode to p else ^^^ p.wait() will set it to 0
                        p.returncode = proc.returncode
                for proc in alive:
                    proc.kill()
        defer(_)

        # wait for p to complete
        # terminate it on any signal
        sigq = chan(1, dtype=gos.Signal)
        signal.Notify(sigq, syscall.SIGINT, syscall.SIGTERM)
        def _():
            signal.Stop(sigq)
        defer(_)
        while 1:
            if p.poll() is not None:
                break

            _, _rx = select(
                    default,    # 0
                    sigq.recv,  # 1
            )

            if _ == 1:
                p.terminate()
                break

            time.sleep(0.1)

    run(_)


# run_in_userns runs f with checks assuming that we are in a user namespace.
@func
def run_in_userns(f):
    # leave only capabilities that are needed for mount/fusermount.
    # in particular drop cap_dac_override so that file permissions are still
    # respected (e.g. write to read/only file is rejected).
    prctl.cap_inheritable.limit('sys_admin')

    # mount new /tmp and /dev/shm to isolate this run from other programs and to detect
    # leaked temporary files at the end.
    tmpreg = {
        "/tmp":     [], # mountpoint -> extra options
        "/dev/shm": []
    }
    for tmp, optv in tmpreg.items():
        xrun(["mount", "-t", "tmpfs", "none", tmp] + optv)

    # in the end: check file leakage on /tmp and friends.
    def _():
        for root in tmpreg:
            for d, dirs, files in os.walk(root):
                if d != root:
                    st = os.stat(d)
                    if st.st_mode & stat.S_ISVTX:
                        # sticky wcfs/ alike directories are used as top of registry for
                        # multiple users. It is kind of normal not to delete such
                        # directories by default.
                        print("# found sticky %s/" % d)
                    else:
                        print("# leaked %s/" % d)
                for f in files:
                    print("# leaked %s" % join(d, f))
    defer(_)

    # in the end: check fstab changes.
    fstab_before = mounts()
    def _():
        fstab_after = mounts()
        for d in difflib.ndiff(fstab_before, fstab_after):
            if d.startswith("- "):
                print("# gone mount: %s" % d[2:])
            if d.startswith("+ "):
                print("# leaked mount: %s" % d[2:])
    defer(_)

    # pretend we don't have tty or any other special group to avoid issues with e.g. pseudo-terminals.
    #
    # POSIX requires /dev/pts/* slaves to be chown'ed to tty group (gid=5) on
    # grantpt. However we do not have that gid mapped and chown fails. Glibc
    # stopped insisting on such chown and delegates proper setup to the kernel
    # expecting /dev/pts to be mounted with gid=5,mode=0620 options:
    # https://sourceware.org/git/?p=glibc.git;a=commitdiff;h=77356912e836
    #
    # However e.g. openssh still wants to do the chown(group=tty):
    # https://github.com/openssh/openssh-portable/blob/V_8_8_P1-120-ga2188579/sshpty.c#L165-L205
    #
    # Avoid that by adjusting the system view so that there is only one sole
    # single regular user and group with uid/gid of current user. We anyway
    # mapped only single uid/gid to parent namespace.
    #
    # Still include root and nobody/nogroup as an exception since several software
    # expect to have zero ID and those names in the user/group database - see e.g.
    # https://lab.nexedi.com/nexedi/slapos/merge_requests/1095#note_147177
    # https://lab.nexedi.com/nexedi/slapos/merge_requests/1095#note_147201
    #
    # Include disk group as well as slapos.core tests currently depend on this group being present:
    # https://lab.nexedi.com/nexedi/slapos/merge_requests/1107#note_148758
    # https://lab.nexedi.com/nexedi/slapos.core/blob/1.7.1-28-g0b6bf2af4/slapos/tests/test_slapgrid.py#L3229-3230
    xetc = "/tmp/xetc"
    os.mkdir(xetc)
    ustr = lambda u: "%s:%s:%d:%d:%s:%s:%s\n" % (u.pw_name, u.pw_passwd, u.pw_uid, u.pw_gid, u.pw_gecos, u.pw_dir, u.pw_shell)
    gstr = lambda g: "%s:%s:%d:%s\n" % (g.gr_name, g.gr_passwd, g.gr_gid, ','.join(g.gr_mem))
    writefile("%s/passwd" % xetc,
        ustr(pwd.getpwuid(os.getuid())) +
        ustr(pwd.getpwnam("root")) +
        ustr(pwd.getpwnam("nobody")))
    writefile("%s/group" % xetc,
        gstr(grp.getgrgid(os.getgid())) +
        gstr(grp.getgrnam("root")) +
        gstr(grp.getgrnam("nogroup")) +
        gstr(grp.getgrnam("disk")))
    xrun(["mount", "--bind", xetc+"/passwd", "/etc/passwd"])
    xrun(["mount", "--bind", xetc+"/group",  "/etc/group"])
    def _():
        xrun(["umount", "-n", "/etc/passwd"])
        xrun(["umount", "-n", "/etc/group"])
        shutil.rmtree(xetc)
    defer(_)

    # run the test
    f()


# run_no_userns runs f assuming that we are not in a user namespace.
def run_no_userns(f):
    f()


# mounts returns current mount entries.
def mounts(): # -> []str
    return readfile("/proc/mounts").split('\n')


# readfile returns content of file @path.
def readfile(path): # -> str
    with open(path, "r") as f:
        return f.read()

# writefile creates file @path and fills it with data.
def writefile(path, data):
    with open(path, "w") as f:
        f.write(data)

# session_proclist returns all processes that belong to specified session.
def session_proclist(sid):
    procv = []
    for proc in psutil.process_iter(['pid']):
        try:
            proc_sid = os.getsid(proc.pid)
        except OSError as e:
            if e.errno in (errno.ESRCH, errno.EPERM):
                # proc either finished, or we are not allowed to retrieve its sid
                # (see getsid(1) for details)
                continue
            raise
        if proc_sid == sid:
            procv.append(proc)
    return procv



if __name__ == '__main__':
    main()
