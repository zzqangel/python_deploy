#!/usr/bin/python3
# coding:utf-8
import os
import shutil

import Constant

logger = Constant.logging.getLogger("File")


def get_file_length(file_path):
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return -1
    return os.path.getsize(file_path)


def copy_file(source_file_path, target_file_path, delete_target_file_if_exist=True):
    if not os.path.exists(source_file_path) or not os.path.isfile(source_file_path):
        return False
    if not delete_target_file_if_exist:
        if os.path.exists(target_file_path) and os.path.isfile(target_file_path):
            return False
    else:
        if os.path.exists(target_file_path) and os.path.isfile(target_file_path):
            os.remove(target_file_path)
    shutil.copyfile(source_file_path, target_file_path)
    return True


def copy_dir(source_dir_path, target_dir_path, delete_target_dir_if_exist=True):
    if not os.path.exists(source_dir_path) or os.path.isfile(source_dir_path):
        return False
    if not delete_target_dir_if_exist:
        if os.path.exists(target_dir_path) and os.path.isdir(target_dir_path):
            return False
    else:
        if os.path.exists(target_dir_path) and os.path.isdir(target_dir_path):
            shutil.rmtree(target_dir_path)
    shutil.copytree(source_dir_path, target_dir_path)
    return True


def copy_dir_cover(source_dir_path, target_dir_path):
    if not os.path.exists(source_dir_path) or os.path.isfile(source_dir_path):
        return False
    shutil.copytree(source_dir_path, target_dir_path)
    return True


def read_file(file_path):
    return open(file_path).read()


def delete_file(file_path):
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            if os.remove(file_path) is None:
                return True
        else:
            if shutil.rmtree(file_path) is None:
                return True
            # return os.removedirs(file_path)
    return False


def move_file(file_path, target_path):
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return False
    if os.path.exists(target_path) and os.path.isfile(target_path):
        delete_file(target_path)
    if os.rename(file_path, target_path) is not None:
        return False
    return True


def get_connect_path(file_path):
    if str(file_path).endswith("/"):
        return file_path
    else:
        return file_path + "/"


def mkdir(path):
    os.mkdir(path)


def check_file_exist(file_path, file_flag=True):
    if not os.path.exists(file_path):
        logger.debug("file {} not exist".format(file_path))
        # print("file not exist")
        return False
    if file_flag:
        # logger.info("file not is file {}".format(os.path.isfile(file_path)))
        # print("file not is file {}".format(os.path.isfile(file_path)))
        return os.path.isfile(file_path)
    else:
        logger.debug("file {} not is dir".format(file_path))
        # print("file {} not is dir".format(file_path))
        return os.path.isdir(file_path)


def move_dir(source_dir_path, target_dir_path, delete_target_dir_if_exist=True):
    if copy_dir(source_dir_path, target_dir_path, delete_target_dir_if_exist):
        return delete_file(source_dir_path)
    return False


def move_file_all(file_path, target_path, delete_target_file_if_exist=True):
    if not check_file_exist(file_path):
        return False
    if os.path.isfile(file_path):
        return move_file(file_path, target_path)
    else:
        return move_dir(file_path, target_path, delete_target_file_if_exist)


def list_files(file_path):
    if not os.path.exists(file_path) or os.path.isfile(file_path):
        return None
    return os.listdir(file_path)
