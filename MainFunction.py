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


'''

import argparse
import time
import Constant
import logging

from importAny import importAny
from tool.File import check_file_exist, mkdir
from tool.Http import http_request_post_ret_content

logger = Constant.logging.getLogger("MainFunction")


def kill_app(obj, currentPid):
    totalCount = 0
    while obj.isAlive(currentPid) and totalCount < Constant.killMaxCount:
        obj.kill(currentPid)
        thisCount = 0
        while obj.isAlive(currentPid) and thisCount < Constant.killCount:
            time.sleep(1)
            thisCount += 1
        totalCount += Constant.killCount
    if obj.isAlive(currentPid):
        return False
    else:
        return True


def recover_app(obj_, projectPath, backup_location, deployFilePath, needStartupFlag, needKillFlag, toKillPid,
                java_path):
    '''

    :param obj:
    :param to_location:
    :param backup_location:
    :param new_file_location:
    :param needStartupFlag:
    :param needKillFlag:
    :param currentPid:
    :param java_path:
    :return:
    '''
    # 如果备份路径不存在，则无法进行恢复重启操作

    if backup_location:
        recoveryFilePath = obj_.recoverOldFile(projectPath, backup_location, deployFilePath)
        if needStartupFlag:
            if needKillFlag:
                if not kill_app(obj_, toKillPid):
                    raise RuntimeError("kill " + toKillPid + " fail")
            thisPid = obj_.applicationStartUp(projectPath, recoveryFilePath, java_path)
            # TODO check startup status
            time.sleep(Constant.startupCheckTime)
            if not obj_.isAlive(thisPid):
                raise RuntimeError("recoverApp fail")
    else:
        raise RuntimeError("backup_location is None and recovery can't be done")
        # if check fail


def file_handling(obj, projectPath, newFileFlag):
    if newFileFlag:
        # 执行文件处理
        # 执行旧文件处置
        uploadFilePathForDeploy = Constant.get_file_upload_path(obj)
        if not check_file_exist(uploadFilePathForDeploy):
            raise RuntimeError('new file not exist. Please check file {} first'.format(uploadFilePathForDeploy))
        # 如果有新文件，则先判断新文件是否存在，如果存在再停止进程，否则不停止
        oldFileBackupPath = None
        deployFilePath = None
        try:
            kill_process(obj)
            oldFileBackupPath = obj.backupOldFile()
            # 执行新文件处置
            deployFilePath = obj.handleNewFile(uploadFilePathForDeploy, oldFileBackupPath)
            # 执行文件处置结果check，返回异常表示失败，否则表示成功
            if not obj.checkNewFile(deployFilePath):
                raise RuntimeError("handle file fail")
            return uploadFilePathForDeploy, oldFileBackupPath, deployFilePath
        except IOError as e:
            logging.error("file_handling error: {0}".format(e))
            # 处置失败时，执行旧文件恢复操作,进程中止
            recover_app(obj, projectPath, oldFileBackupPath, deployFilePath, True, False, -1, Constant.javaPath)
            # obj.recoverOldFile(newFilePath, oldFileBackupPath, deployFilePath)
            raise RuntimeError('new file handle fail')
    else:
        # TODO 增加默认路径返回
        return None, None, obj.get_default_deploy_path()


def application_startup(obj, projectPath, deployFilePath, oldFileBackupPath):
    currentPid = -1
    if obj.needStartup():
        # 确认启动命令执行成功
        # 获取启动进程的id
        try:
            currentPid = obj.applicationStartUp(projectPath, deployFilePath, Constant.javaPath)
            time.sleep(Constant.startupCheckTime)
            logger.info("currentPid {}".format(currentPid))
            # print("currentPid {}".format(currentPid))
            # 确认进程有效存在
            if not obj.isAlive(currentPid):
                raise RuntimeError("start app fail")
        except Exception as e:
            recover_app(obj, projectPath, oldFileBackupPath, deployFilePath, True, False, -1, Constant.javaPath)
            raise e
    return currentPid


def health_check(obj, currentPid, deployFilePath, projectPath, oldFileBackupPath):
    checkHealthCount = 0
    # 循环检查启动是否成功
    while checkHealthCount < Constant.checkHealthMaxCount and not obj.checkHealth(currentPid, deployFilePath):
        time.sleep(1)
        checkHealthCount += 1
    # 超过检查时间上限，认定启动失败，执行停止操作，并恢复旧文件，执行旧文件启动操作，再次执行检查，如果仍然失败，则停止尝试
    if not obj.checkHealth(currentPid, deployFilePath):
        try:
            recover_app(obj, projectPath, oldFileBackupPath, deployFilePath, True, True, currentPid,
                        Constant.javaPath)
        finally:
            # 无论旧文件恢复是否成功，项目均抛出失败异常，表标注失败原因和当前状态
            raise RuntimeError('deploy ' + str(obj) + ' fail')


def kill_process(obj):
    if obj.needCheckPid():
        pid = obj.getPid()
        logger.info("kill_process find pid {}".format(pid))
        if pid.__len__() > 1:
            raise RuntimeError('pid more than one ' + pid + '. please check manually')
        if pid.__len__() == 1 and pid[0] > 0:
            if not kill_app(obj, pid[0]):
                raise RuntimeError('kill ' + str(obj) + ' fail')


def get_obj(artifactId, isSpringAppFlag, env):
    cls = importAny('lib.' + artifactId + '.' + artifactId + '')
    obj = None
    if not cls:
        if isSpringAppFlag:
            cls = importAny(Constant.springClass)
            obj = cls(Constant.startPath + artifactId.replace("_", "-"), artifactId, env)
        else:
            raise RuntimeError('handle class not found')
    else:
        logger.info("env {}".format(env))
        # print("env {}".format(env))
        obj = cls(Constant.startPath + artifactId.replace("_", "-"), None, env)
    return obj


def arg_handling(argparse):
    parser = argparse.ArgumentParser(description='manual to this script')
    # 应用名
    parser.add_argument('--artifactId', type=str)
    # 确认版本号
    parser.add_argument('--confirmVersion', type=str)
    parser.add_argument('--newFileFlag', type=str)
    parser.add_argument('--isSpringAppFlag', type=str)
    parser.add_argument('--env', type=str)
    args = parser.parse_args()
    artifactId = args.artifactId
    confirmVersion = args.confirmVersion
    env = args.env
    artifactId = artifactId.replace("-", "_")
    logger.info("artifactId: " + artifactId)
    # print("artifactId: " + artifactId)

    newFileFlag = True
    if args.newFileFlag:
        if not str(args.newFileFlag).__eq__("false"):
            newFileFlag = True
    isSpringAppFlag = False
    if args.isSpringAppFlag:
        if str(args.isSpringAppFlag).__eq__("true"):
            isSpringAppFlag = True
    return artifactId, confirmVersion, newFileFlag, isSpringAppFlag, env


def del_useless_file(obj, oldFileBackupPath, uploadFilePathForDeploy):
    try:
        if oldFileBackupPath:
            obj.delete_backup_file(oldFileBackupPath)
    except Exception as e:
        logger.error("delete_backup_file fail" + str(e))
        # print("delete_backup_file fail" + str(e))

    # 移除传输过来的文件
    try:
        if uploadFilePathForDeploy:
            obj.delete_upload_file(uploadFilePathForDeploy)
    except Exception as e:
        logger.error("delete_upload_file fail" + str(e))
        # print("delete_upload_file fail" + str(e))


'''
    argruments init
'''


def sendEmail(artifactId, ex):
    try:
        map_ = {"to": Constant.buildFailEmailTo, "subject": "deploy fail",
                "content": ("app " + artifactId + " deploy fail for {}").format(ex)}
        # map.__setitem__("to", "16969228@qq.com")
        # o.artifactId = artifactId
        # o.ex = ex
        # http_request_post_ret_content()
        from json import dumps
        json = dumps(map_)
        http_request_post_ret_content(Constant.emailUrl, data=json, json=None)
    except Exception as ex2:
        logger.error("send email fail {}".format(ex2))
        # print("send email fail {}".format(ex2))
    '''
        {"to":"${applierEmailAddress}","cc":"${BUILD_USER_EMAIL}","subject":"Online Apply Deploy Report","content":"${mailContent}"}
    :param artifactId:
    :param ex:
    :return:
    '''
