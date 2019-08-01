#!/usr/bin/python3
# coding:utf-8
'''
    standard run command
    python3 dynamicImport.py
        --artifactId={artifactId}(required)
        --isSpringAppFlag={true or false}(not required, if class not exist and not necessary)
        --newFileFlag={true or false}(not required, give false if no file need to be operated)
        --confirmVersion={current version}(not required, useless now)
        --env={current environment}(not required, default is prod. selection include dev, test, vprod, prod)

    spring jar app:
        python3 dynamicImport.py --artifactId=aaaa-bbb --isSpringAppFlag=true --env=dev

'''
import argparse

import Constant
from MainFunction import get_obj, kill_process, application_startup, health_check, del_useless_file, sendEmail, \
    file_handling, arg_handling

env = None
logger = Constant.logging.getLogger("dynamicImport")
try:

    artifactId, confirmVersion, newFileFlag, isSpringAppFlag, env = arg_handling(argparse)
    obj = get_obj(artifactId, isSpringAppFlag, env)
    logger.info("obj start")
    # print("ob start")
    projectPath = Constant.startPath + "/" + artifactId.replace("_", "-")
    if not newFileFlag:
        kill_process(obj)
    # 前台项目跳过kill过程
    logger.info("kill pid finish")
    # print("kill pid finish")
    uploadFilePathForDeploy, oldFileBackupPath, deployFilePath = file_handling(obj, projectPath, newFileFlag)
    # print("new file handle finish")
    logger.info("new file handle finish")
    currentPid = application_startup(obj, projectPath, deployFilePath, oldFileBackupPath)
    # print("application start finish")
    logger.info("application start finish")
    health_check(obj, currentPid, deployFilePath, projectPath, oldFileBackupPath)
    # print("check application finish")
    logger.info("check application finish")
    # TODO 前端工程的最终访问确认
    '''
        Frontend accessible check
    '''
    del_useless_file(obj, oldFileBackupPath, uploadFilePathForDeploy)
except Exception as e:
    # send email
    if env and str(env).__eq__("prod"):
        sendEmail(artifactId, str(e))
    raise e
