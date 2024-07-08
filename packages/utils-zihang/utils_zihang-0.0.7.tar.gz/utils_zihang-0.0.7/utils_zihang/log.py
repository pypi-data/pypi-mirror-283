# -*- coding:utf-8 -*-
"""
Created on 2023/7/26 17:43
@File: log.py
---------
@summary:
---------
@Author: luzihang
@Contact: https://github.com/luzihang123
"""
import os
import sys
from loguru import logger
from pathlib import Path

# 获取当前工作目录和父目录
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent


def setup_logger(app_name, env='DEV', log_dir=None):
    logger_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "[<light-blue>{extra[trace]}</light-blue>] | "
        "<level>{message}</level>"
    )

    # 直接绑定 trace 而不重新赋值给 logger
    bound_logger = logger.bind(trace="")

    bound_logger.configure(handlers=[{"sink": sys.stdout, "format": logger_format}])

    log_name = f'{app_name.lower()}.log'
    error_log_name = f'{app_name.lower()}-error.log'
    analysis_log_name = f'{app_name.lower()}-analysis.log'

    # 确定日志文件路径
    if log_dir:
        log_path = os.path.join(log_dir, log_name)
        error_log_path = os.path.join(log_dir, error_log_name)
        analysis_log_path = os.path.join(log_dir, analysis_log_name)
    else:
        log_path = os.path.join('/data/log' if env in ['PROD', 'UAT', 'TEST'] else parent_dir, log_name)
        error_log_path = os.path.join('/data/log' if env in ['PROD', 'UAT', 'TEST'] else parent_dir, error_log_name)
        analysis_log_path = os.path.join('/data/log' if env in ['PROD', 'UAT', 'TEST'] else parent_dir, analysis_log_name)

    # 确保日志目录存在
    if not os.path.exists(os.path.dirname(log_path)):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    try:
        # 配置Loguru日志输出到文件
        bound_logger.add(log_path, rotation="500 MB", retention=3, level="INFO", format=logger_format)
        # 配置Loguru日志输出到文件 - 错误日志
        bound_logger.add(error_log_path, rotation="500 MB", retention=3, level="ERROR", format=logger_format)
        # 配置Loguru日志输出到文件 - 分析日志
        bound_logger.add(analysis_log_path, rotation="500 MB", retention=1, level="INFO", format=logger_format,
                         filter=lambda record: record["extra"].get("analysis", False))
    except Exception as e:
        bound_logger.error(f"Error configuring logging: {e}")

    return bound_logger


if __name__ == '__main__':
    from utils_zihang.log import setup_logger

    # # 示例：指定自定义日志路径

    custom_log_dir = "/Users/luzihang/Desktop/LocalProjectHome/utils_zihang/log"
    log = setup_logger(app_name="my_app", env="DEV", log_dir=custom_log_dir)
    log.info("这是一条信息日志")
    import uuid

    trace_id = str(uuid.uuid4())
    log.bind(trace=trace_id).info("这是一条带有trace的信息日志")
    log.bind(trace=trace_id, analysis=True).info("这是一条带有trace和analysis的信息日志")
    log.bind(analysis=True).info("这是一条带有analysis的信息日志")
