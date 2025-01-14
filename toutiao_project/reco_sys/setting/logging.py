# ----------------------------------------------
# -*- encoding=utf-8 -*-                      #
# __author__:'焉知飞鱼'                        #
# CreateTime:                                 #
#       2020/2/4 21:24                       #
#                                             #
#               天下风云出我辈，                 #
#               一入江湖岁月催。                 #
#               皇图霸业谈笑中，                 #
#               不胜人生一场醉。                 #
# ----------------------------------------------

import logging
import logging.handlers
import os

logging_file_dir = 'root/logs'


def create_logger():
    # 离线处理更新打印日志
    trace_file_handler = logging.FileHandler(
        os.path.join(logging_file_dir, 'offline.log')
    )
    trace_file_handler.setFormatter(logging.Formatter('%(message)s'))
    log_trace = logging.getLogger('offline')
    log_trace.addHandler(trace_file_handler)
    log_trace.setLevel(logging.INFO)

    # 在线日志打印
    trace_file_handler = logging.FileHandler(
        os.path.join(logging_file_dir, 'online.log')
    )
    trace_file_handler.setFormatter(logging.Formatter('%(message)s'))
    log_trace = logging.getLogger('online')
    log_trace.addHandler(trace_file_handler)
    log_trace.setLevel(logging.INFO)

    # 实时推荐日志打印
    trace_file_handler = logging.FileHandler(
        os.path.join(logging_file_dir, 'recommend.log')
    )
    trace_file_handler.setFormatter(logging.Formatter('%(message)s'))
    log_trace = logging.getLogger('recommend')
    log_trace.addHandler(trace_file_handler)
    log_trace.setLevel(logging.INFO)
