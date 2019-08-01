import abc
import time
from abc import ABC

from lib.BackendAppHandler import BackendAppHandler
from tool.Java import cmd_invoke


class TomcatAppHandler(BackendAppHandler, ABC):

    def __init__(self, start_path, init_class, env):
        super().__init__(start_path, init_class, env)

    def kill(self, pid):
        # /data/app/**/**/tomcat/bin/shutdown.sh
        start_path = self.start_path
        if not str(self.start_path.endswith("/")):
            start_path += "/"
        cmd_invoke(self.get_tomcat_shutdown_cmd(start_path))

    def applicationStartUp(self, project_path, new_file_location, java_path):
        # /data/app/**/**/tomcat/bin/startup.sh
        if not str(project_path.endswith("/")):
            project_path += "/"
        cmd_invoke(self.get_tomcat_start_cmd(project_path))
        time.sleep(1)
        ids = self.getPid()
        if ids.__len__() > 0:
            return self.getPid()[0]
        return -1

    @abc.abstractmethod
    def get_tomcat_start_cmd(self, project_path):
        pass

    @abc.abstractmethod
    def get_tomcat_shutdown_cmd(self, start_path):
        pass
