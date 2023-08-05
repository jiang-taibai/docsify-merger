# -*- coding: utf-8 -*-
# Time    : 2023-08-05 14:24
# Author  : Jiang Liu
# Desc    : 日志模块

import logging
import logging.config as logging_config

logger = None


def init_logging(ini_file_path):
    """
    初始化日志模块
    """
    global logger
    logging_config.fileConfig(ini_file_path)
    logger = logging.getLogger()


def get_logger():
    """
    获取日志对象
    """
    global logger
    return logger
