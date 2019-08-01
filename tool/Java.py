#!/usr/bin/python3
# coding:utf-8
import os
import random
import subprocess

import Constant
from tool.File import read_file

logger = Constant.logging.getLogger("Java")


def java_application_start(java_path, startCmd, startJarPath, logoutPath):
    n = random.randint(1000, 9999)
    filePath = str(n) + ".pid"
    cmd = "nohup " + java_path + " " + startCmd + " " + startJarPath + " >" + logoutPath + " 2>&1 &\n echo \"$!\" >" + filePath
    logger.debug("java start cmd is {}".format(cmd))
    # print("java start cmd is {}".format(cmd))
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    if p.returncode != 0:
        raise RuntimeError("start java application fail")
    pid = read_file(filePath)
    os.remove(filePath)
    return pid


def cmd_invoke(startCmd, timeout=None):
    logger.debug("cmd_start invoke cmd {}".format(startCmd))
    # print("cmd_start invoke cmd {}".format(startCmd))
    p = subprocess.Popen(
        startCmd,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait(timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError("cmd_start application fail {}".format(p.returncode))

# print(java_application_start("/data/jdk/jdk1.8.0_201/bin/java", "-jar -Dspring.profiles.active=dev",
#                       "/data/app/id-creator-service/id-creator-service-1.0-SNAPSHOT.jar",
#                       "/data/app/id-creator-service/nohup.out"))
