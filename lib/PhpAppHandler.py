import abc
from abc import ABC

from lib.FrontendAppHandler import FrontendAppHandler
from tool.File import check_file_exist, list_files, move_dir, delete_file, move_file_all
from tool.Zip import un_tar_gz


class PhpAppHandler(FrontendAppHandler, ABC):

    def __init__(self, start_path, init_class, env):
        super().__init__(start_path, init_class, env)

    def checkNewFile(self, new_file_locate_path):
        if not check_file_exist(new_file_locate_path, False):
            return False
        list = list_files(new_file_locate_path)
        if list:
            if list.__len__() > 0:
                if str(self.start_path).endswith("/"):
                    return check_file_exist(self.start_path + ".env")
                else:
                    return check_file_exist(self.start_path + "/.env")
        return False

    def backupOldFile(self):
        # self.start_path进行备份移动
        targetPath = self.start_path
        if str(targetPath).endswith("/"):
            targetPath = targetPath[0:str(targetPath).__len__() - 1]
        targetPath += "_bak"
        self.logger.info("to backupOldFile targetPath {}".format(targetPath))
        if not move_dir(self.start_path, targetPath):
            raise RuntimeError("back old file fail")
        return targetPath

    def handleNewFile(self, uploadFilePathForDeploy, old_file_backup_path):
        # 解压缩
        sourcePath = un_tar_gz(uploadFilePathForDeploy)
        # 将压缩包文件移动至start_path
        unZipPath = sourcePath + "/zipDir"
        if not move_dir(unZipPath, self.start_path):
            raise RuntimeError("move new file to deploy path fail")
        # 执行文件更名
        appPath = self.start_path
        if not str(appPath).endswith("/"):
            appPath += "/"
        envFile = appPath + ".env"
        delete_file(envFile)
        envFile2 = appPath + self.get_env_file_name()
        sourceEnvExist = check_file_exist(envFile2)
        self.logger.info("envFile2 {} to envFile {}".format(sourceEnvExist, check_file_exist(envFile)))
        # print("envFile2 {} to envFile {}".format(sourceEnvExist, check_file_exist(envFile)))
        if not sourceEnvExist:
            raise RuntimeError("env file not exist")
        move_file_all(envFile2, envFile)
        self.logger.info("envFile2 {} to envFile {} replace result {}".format(envFile2, envFile, check_file_exist(envFile)))
        # print("envFile2 {} to envFile {} replace result {}".format(envFile2, envFile, check_file_exist(envFile)))
        configPath = appPath + self.get_config_path()
        if check_file_exist(configPath, False):
            # 如果存在再执行本替换，否则不执行
            if check_file_exist(configPath + self.env + ".config.js"):
                move_file_all(configPath + self.env + ".config.js", configPath + "config.js")
        delete_file(sourcePath)
        # 返回start_path
        return self.start_path

    def recoverOldFile(self, project_path, backup_location, deployFilePath=None):
        delete_file(self.start_path)
        move_file_all(backup_location, self.start_path)
        return self.start_path

    def get_default_deploy_path(self):
        return self.start_path

    @abc.abstractmethod
    def get_env_file_name(self):
        pass

    @abc.abstractmethod
    def get_config_path(self):
        pass
