#!/usr/bin/python3
# coding:utf-8

import Constant
from Constant import quitJavaProcessTime
from tool.File import get_file_length, copy_file, delete_file, move_file, get_connect_path
from tool.Http import http_request_ret_content
from tool.Java import java_application_start
from tool.System import kill_pid
from lib.BackendAppHandler import BackendAppHandler


class SpringAppHandler(BackendAppHandler):

    def __init__(self, start_path, init_class, env):
        super().__init__(start_path, init_class, env)
        self.oldFileLength = get_file_length(start_path + self.fileName())

    # 默认名字，名字不同的需要重写本方法
    def fileName(self):
        name = self.get_artifact_id()
        return name + "-1.0-SNAPSHOT.jar"

    def get_pid_check_need_path(self):
        # name = self.get_artifact_id()
        return self.get_default_deploy_path()

    def get_default_deploy_path(self):
        if str(self.start_path).endswith("/"):
            return self.start_path + self.fileName()
        else:
            return self.start_path + "/" + self.fileName()

    def kill(self, pid):
        return kill_pid(pid, quitJavaProcessTime)

    def checkNewFile(self, new_file_locate_path):
        return get_file_length(new_file_locate_path) != self.oldFileLength

    def default_jar_path(self):
        return self.fileName()

    def backupOldFile(self):
        jarPath = self.get_jar_path()
        targetPath = self.create_backup_file_name(jarPath)
        if copy_file(jarPath, targetPath):
            return targetPath
        else:
            raise RuntimeError('backupOldFile fail source {0} target {1}'.format(jarPath, targetPath))

    def get_jar_path(self):
        if str(self.start_path).endswith("/"):
            targetFilePath = self.start_path + self.default_jar_path()
        else:
            targetFilePath = self.start_path + "/" + self.default_jar_path()
        targetFilePath = str(targetFilePath).replace("_", "-")
        return targetFilePath

    def handleNewFile(self, new_file_source_path, old_file_backup_path):
        targetFilePath = self.get_jar_path()
        if copy_file(new_file_source_path, targetFilePath):
            return targetFilePath
        return None

    def applicationStartUp(self, project_path, new_file_location, java_path):
        return java_application_start(Constant.javaPath, Constant.get_property("startCmd", self.env), new_file_location,
                                      get_connect_path(project_path) + Constant.logoutpath)

    def recoverOldFile(self, project_path, backup_location, deployFilePath=None):
        # 删除新文件
        # 旧文件改名为新文件
        # 返回新文件路径
        if deployFilePath:
            targetFilePath = deployFilePath
        else:
            targetFilePath = self.get_jar_path()
        delete_file(targetFilePath)
        ret = move_file(backup_location, targetFilePath)
        if ret is True:
            return targetFilePath
        else:
            raise RuntimeError("recoverOldFile fail")

    def checkHealth(self, current_pid, new_file_locate_path):
        url = Constant.get_property("healthCheckUrl", self.env).replace("{}", self.get_artifact_id())
        try:
            ret = http_request_ret_content(url)
            return "passing".__eq__(ret)
        except Exception as e:
            return False

    def delete_backup_file(self, oldFileBackupPath):
        delete_file(oldFileBackupPath)
