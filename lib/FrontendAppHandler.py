#!/usr/bin/python3
# coding:utf-8
import abc
from lib.parent import HandlerParent
from tool.File import delete_file
from tool.Http import http_request_ret_200


class FrontendAppHandler(HandlerParent, abc.ABC):

    def needStartup(self):
        return False

    # 前端项目不需要checkPid
    def needCheckPid(self):
        return False

    # 前端项目pid一律返回-1，表示不存在
    def getPid(self):
        return []

    # 默认返回当前类名处理的结果
    def fileName(self):
        return self.__class__.__name__.replace("_", "-") + ".tar.gz"

    # 前端项目不需要执行kill操作
    def kill(self, pid):
        pass

    # 前端项目不需要启动应用
    def applicationStartUp(self):
        pass

    def delete_backup_file(self, oldFileBackupPath):
        delete_file(oldFileBackupPath)

    @abc.abstractmethod
    def get_check_health_url(self):
        pass

    def checkHealth(self, current_pid, new_file_locate_path):
        return http_request_ret_200(self.get_check_health_url())

    def __init__(self, start_path, init_class, env):
        super().__init__(start_path, init_class, env)
