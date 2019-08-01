import logging

from tool.File import check_file_exist, mkdir

startPath = "/data/app/"
javaPath = "/data/jdk/jdk1.8.0_201/bin/java"
uploadPath = "appupload/"
killCount = 15
killMaxCount = 60
startupCheckTime = 15
checkHealthMaxCount = 60
quitJavaProcessTime = 10
quitTomcatProcessTime = 45
dev_startCmd = "-jar -Dspring.profiles.active=dev"
prod_startCmd = "-jar -Dspring.profiles.active=prod"
logoutpath = "nohup.out"
prod_healthCheckUrl = "http://localhost:8500/v1/agent/health/service/name/{}?format=text"
dev_healthCheckUrl = "http://172.31.15.10:8500/v1/agent/health/service/name/{}?format=text"
springClass = 'lib.SpringAppHandler.SpringAppHandler'
emailUrl = "http://172.31.2.183:8678/email/operation/sendEmail"
buildFailEmailTo = "16969228@qq.com"
loggingLevel = logging.INFO

if not check_file_exist("log", False):
    mkdir("log")

logging.basicConfig(level=loggingLevel,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    handlers={logging.FileHandler(filename='log/deploy.log', mode='a', encoding='utf-8')})
# 定义一个Handler打印INFO及以上级别的日志到sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# 设置日志打印格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# 将定义好的console日志handler添加到root logger
logging.getLogger('').addHandler(console)


def get_file_upload_path(o):
    return startPath + uploadPath + o.fileName()


def get_property(key, env=None):
    if env is None:
        return globals().get(key)
    return globals().get(env + "_" + key)
