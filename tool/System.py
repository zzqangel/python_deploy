#!/usr/bin/python3
# coding:utf-8
import psutil

import Constant
from Constant import quitJavaProcessTime

logger = Constant.logging.getLogger("Java")


def check_process_alive(pid):
    if get_process(pid):
        return True
    return False


def get_app_pid(check_file_path):
    retPids = []
    logger.debug("get_app_pid with {}".format(check_file_path))
    for process in psutil.process_iter():
        processInfo = None
        try:
            processInfo = process.as_dict(attrs=['pid', 'memory_maps'])
        except psutil.NoSuchProcess:
            pass
        else:
            mm = processInfo.get("memory_maps")
            if not mm:
                continue
            # print(processInfo)
            for _mm in mm:
                if not _mm or not _mm.path:
                    continue
                if str(_mm.path).__contains__(check_file_path):
                    logger.debug("found process with pid " + str(processInfo.get("pid")))
                    # print("found process with pid " + str(processInfo.get("pid")))
                    retPids.append(processInfo.get("pid"))
                    break
    return retPids


"Tries hard to terminate and ultimately kill all the children of this process."


def on_terminate(proc):
    logger.debug("process {} terminated with exit code {}".format(proc, proc.returncode))
    # print("process {} terminated with exit code {}".format(proc, proc.returncode))


def kill_pid(pid, timeout=quitJavaProcessTime):
    if not reap_children(pid, timeout):
        return False
    process = get_process(pid)
    if not process:
        return False
    proces = [process]
    return kill_processes(proces, timeout)


def reap_children(pid, timeout=quitJavaProcessTime):
    process = get_process(pid)
    if not process:
        return False
    procs = process.children()
    if not procs or procs.__len__() == 0:
        return True
    # send SIGTERM
    for p in procs:
        try:
            p.terminate()
        except psutil.NoSuchProcess:
            pass
    return kill_processes(procs, timeout)


def kill_processes(procs, timeout=quitJavaProcessTime):
    gone, alive = psutil.wait_procs(procs, timeout=timeout, callback=on_terminate)
    if alive:
        # send SIGKILL
        for p in alive:
            logger.debug("process {} survived SIGTERM; trying SIGKILL".format(p))
            # print("process {} survived SIGTERM; trying SIGKILL".format(p))
            try:
                p.kill()
            except psutil.NoSuchProcess:
                pass
        gone, alive = psutil.wait_procs(alive, timeout=timeout, callback=on_terminate)
        if alive:
            # give up
            for p in alive:
                logger.debug("process {} survived SIGKILL; giving up" % p)
                # print("process {} survived SIGKILL; giving up" % p)
            return False
    return True


def get_process(pid):
    s = str(pid).strip()
    for process in psutil.process_iter():
        s2 = str(process.pid).strip()
        eq = s.__eq__(s2)
        logger.debug("s {} s2 {} is eq {}".format(s, s2, eq))
        # print("s {} s2 {} is eq {}".format(s, s2, eq))
        # print("process {}".format(process.pid))
        if eq:
            logger.debug("found pid {}".format(pid))
            # print("found pid {}".format(pid))
            return process
    return None
