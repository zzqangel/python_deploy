import gzip
import os
import tarfile
import zipfile
import rarfile

import Constant
from tool.File import delete_file

logger = Constant.logging.getLogger("Zip")


def un_gz(file_name):
    """ungz zip file"""
    g_file = None
    f_name = file_name.replace(".gz", "")
    # 获取文件的名称，去掉
    try:
        g_file = gzip.GzipFile(file_name)
        # 创建gzip对象
        # open(f_name, "w+").
        f = None
        try:
            with open(f_name, 'ba') as f:
                buf = bytearray(g_file.read())
                f.write(buf)
        except Exception as e:
            print("{}".format(e))
            raise e
        finally:
            if f:
                f.close()
        return f_name
        # open(f_name, "w+").write(g_file.read())
        # gzip对象用read()打开后，写入open()建立的文件里。
    except Exception as e:
        logger.error("{}".format(e))
        # print("{}".format(e))
        raise e
    finally:
        if g_file:
            g_file.close()
    # 关闭gzip对象


# tar
# XXX.tar.gz解压后得到XXX.tar，还要进一步解压出来。
# 注：tgz与tar.gz是同样的格式，老版本号DOS扩展名最多三个字符，故用tgz表示。
# 因为这里有多个文件，我们先读取全部文件名称。然后解压。例如以下：
# 注：tgz文件与tar文件同样的解压方法。
def un_tar(file_name):
    # untar zip file"""
    tar = None
    try:
        tar = tarfile.open(file_name)
        names = tar.getnames()
        targetName = str(file_name).replace(".tar", "")
        if os.path.isdir(targetName):
            pass
        else:
            os.mkdir(targetName)
        # 因为解压后是很多文件，预先建立同名目录
        for name in names:
            tar.extract(name, targetName)
        return targetName
    except Exception as e:
        logger.error("{}".format(e))
        # print("{}".format(e))
        raise e
    finally:
        if tar:
            tar.close()


# zip
# 与tar类似，先读取多个文件名称，然后解压。例如以下：

def un_zip(file_name):
    """unzip zip file"""
    zip_file = None
    try:
        zip_file = zipfile.ZipFile(file_name)
        targetName = str(file_name).replace(".zip", "")
        if os.path.isdir(targetName):
            pass
        else:
            os.mkdir(targetName)
        for names in zip_file.namelist():
            zip_file.extract(names, targetName)
        return targetName
    except Exception as e:
        logger.error("{}".format(e))
        # print("{}".format(e))
        raise e
    finally:
        if zip_file:
            zip_file.close()


# rar
# 由于rar通常为window下使用，须要额外的Python包rarfile。
#
# 可用地址： http://sourceforge.net/projects/rarfile.berlios/files/rarfile-2.4.tar.gz/download
#
# 解压到Python安装文件夹的/Scripts/文件夹下，在当前窗体打开命令行,
#
# 输入Python setup.py install
#
# 安装完毕。

def un_rar(file_name):
    """unrar zip file"""
    rar = None
    try:
        rar = rarfile.RarFile(file_name)
        targetName = str(file_name).replace(".rar", "")
        if os.path.isdir(targetName):
            pass
        else:
            os.mkdir(targetName)
        os.chdir(targetName)
        rar.extractall()
        return targetName
    except Exception as e:
        logger.error("{}".format(e))
        # print("{}".format(e))
        raise e
    finally:
        if rar:
            rar.close()


def un_tar_gz(file_path):
    tar_file = None
    try:
        tar_file = un_gz(file_path)
        return un_tar(tar_file)
    finally:
        delete_file(tar_file)
