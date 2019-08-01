#!/usr/bin/python3
# coding:utf-8
'''
    接口父类
    所有接口类均需要继承本类，并实现接口方法
'''
import abc

import Constant
from tool.File import delete_file
from tool.System import check_process_alive


class HandlerParent(metaclass=abc.ABCMeta):
    def __init__(self, start_path, init_class, env):
        print('init parent')
        self.start_path = start_path
        self.init_class = init_class
        self.env = env
        self.logger = Constant.logging.getLogger(self.get_artifact_id())

    @abc.abstractmethod
    def checkNewFile(self, new_file_locate_path):
        '''

        :param new_file_locate_path: 新文件处理完成以后的项目文件路径
        :return: 不需要返回值
                如果检查失败，则抛出IOError，指定错误原因
        '''

    @abc.abstractmethod
    def backupOldFile(self):
        '''

        :param old_file_path: 旧文件路径
        :return: 旧文件备份结果路径
        '''

    @abc.abstractmethod
    def handleNewFile(self, uploadFilePathForDeploy, old_file_backup_path):
        '''

        :param new_file_path: 新文件的当前路径
        :param old_file_backup_path: 旧文件的备份路径
        :return: 新文件处理完成以后的项目文件路径
        '''

    @abc.abstractmethod
    def getPid(self):
        '''
            获取当前任务的pid
        '''

    @abc.abstractmethod
    def fileName(self):
        '''
            获取当前文件的传输到指定路径的文件名的名称
        '''

    @abc.abstractmethod
    def kill(self, pid):
        'implement should return kill success or fail'
        'if success return True otherwise return False'
        'if current application does not have to be killed then return True without any action'
        'kill should check whether process with pid of current app still alive'
        'make sure the process is dead'
        'the max waiting time should less than 60s'

    '''
        检查指定进程是否存在
    '''

    def isAlive(self, pid):
        return check_process_alive(pid)

    @abc.abstractmethod
    def applicationStartUp(self, project_path, new_file_location, java_path):
        '''

        :param start_path: 项目起始地址
        :param new_file_location: 新部署的文件的地址
        :param java_path:  java命令地址
        :return:  启动服务的pid
        '''

    @abc.abstractmethod
    def checkHealth(self, current_pid, deploy_file_path):
        '''

        :param current_pid: 当前需要检测的进程pid
        :param new_file_locate_path: 新部署的文件的地址
        :return:  True False
        '''

    @abc.abstractmethod
    def needCheckPid(self):
        '''

        :return:
        '''

    @abc.abstractmethod
    def needStartup(self):
        '''

        :return: True需要执行启动，否则不需要
        '''

    def get_artifact_id(self):
        if self.init_class:
            return self.init_class.replace("_", "-")
        return str(self.__class__.__name__).replace("_", "-")

    def create_backup_file_name(self, origin_file_path):
        return origin_file_path + ".bak"

    @abc.abstractmethod
    def recoverOldFile(self, project_path, backup_location, deployFilePath=None):
        '''

        :param project_path: 项目路径
        :param backup_location: 备份文件路径
        :param new_file_location: 新替换文件的路径
        :return: 替换结束后旧文件的新路径
        '''

    @abc.abstractmethod
    def delete_backup_file(self, oldFileBackupPath):
        '''

        :param oldFileBackupPath:  备份文件的路径
        :return:
        '''

    def delete_upload_file(self, newUploadFilePath):
        delete_file(newUploadFilePath)

    @abc.abstractmethod
    def get_default_deploy_path(self):
        pass
