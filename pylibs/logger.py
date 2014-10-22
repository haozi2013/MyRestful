#!/usr/bin/python
# -*- coding: utf-8 -*-

"logger 0.1.0"
#
# 导入外部模块
#

import os
import sys
import time

class Logger:

    def __init__(self, logdir, verbose='LV_WARNING'):
        """
        初始函数
        """
        self.logdir = logdir    # 日志存放目录
        # 定义消息等级（-1为最高）
        self.LV_DICT = {
            'LV_DEBUG': 3,     # 调试输出
            'LV_INFO': 2,      # 每个情节的细节信息
            'LV_WARNING': 1,   # 警告，非致命性错误
            'LV_EVENT': 0,     # 重大事件
            'LV_ERROR': -1    # 致命性错误
        }
        self.verbose = self.LV_DICT[verbose]  # 日志等级
        self.checkLogdir()

    def checkLogdir(self):
        """
        检查日志目录是否存在
        """
        if not os.path.isdir(self.logdir):
            os.mkdir(self.logdir)

    def write(self, msg, verbose):
        """
        记录日志和消息输出
        Args:
            msg    : 消息
            verbose: 消息等级（只有当消息等级大于等于日志等级时才执行日志记录和消息输出）
        """
        verbose = self.LV_DICT[verbose]
        if verbose > self.verbose:
            return
        now_time = time.time()
        content = '%s\t%d\t%s' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now_time)), verbose, msg.replace('\n', '\\n').replace('\r', '\\r'))
        print >> sys.stdout, content
        logpath = self.logdir + '/' + time.strftime('%Y-%m-%d', time.localtime(now_time))
        f = open(logpath, 'a')
        print >> f, content
        f.close()
