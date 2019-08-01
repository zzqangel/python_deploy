#!/usr/bin/python3
# coding:utf-8
import abc

from tool.System import get_app_pid
from lib.parent import HandlerParent


class BackendAppHandler(HandlerParent, abc.ABC):
    def needCheckPid(self):
        return True

    def needStartup(self):
        return True

    def getPid(self):
        return get_app_pid(self.get_pid_check_need_path())

    @abc.abstractmethod
    def get_pid_check_need_path(self):
        '''

        :return:  检查必须的路径
        '''

    def __init__(self, start_path, init_class, env):
        super().__init__(start_path, init_class, env)
