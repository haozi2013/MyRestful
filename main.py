#!/usr/bin/python
# -*- coding: utf-8 -*-


# 工作流程：
# 1、调用Restful 通过post模式接收到发送者的信息
# 2、发送邮件给信息发送者、发送邮件给特定邮箱并记录下信息发送者


import time
import os
import time
import sys
from pylibs.restful import Restful
from pylibs.mail import Mail
from pylibs.logger import Logger
from BaseHTTPServer import HTTPServer

VERSION = '0.1.0'

class MyRestful(Restful):
    def __init__(self, request, client_address, server):
        """
        初始化
        """
        # 建立邮件对象
        self.mail = Mail()
        # 建立日志对象
        self.logger = Logger('./log/', verbose='LV_DEBUG')
        # sender的信息
        self.sender_info = {}
        self.sender_items = ['email', 'first_name', 'last_name', 'contact_number', 'title', 'content', 'link']
        # 获取邮箱服务器信息
        self.mail_config = self.getMailConfig()
        Restful.__init__(self,request, client_address, server)

    def processDatas(self, datas):
        """
        处理通过post获取的数据
        """
        # URI路径不对则返回
        if self.path != '/rest':
            msg = 'Wrong path: %s' % self.path
            self.logger.write(msg, 'LV_WARNING')
            self.wfile.write(msg + '\n')
            return
        # 获取sender的信息
        datas = self.getSenderInfo(datas)
        if datas is False:  # 数据非法则返回
            msg = "Sender's information is wrong!"
            self.logger.write(msg, 'LV_WARNING')
            self.wfile.write("Your information is wrong!\n")
            return
        msg = "Received sender information succ!"
        self.logger.write(msg, 'LV_INFO')
        self.wfile.write("Received your information succ!\n")
        # sender信息存档
        self.storeSenderMsg(datas)
        msg = "Stored sender information succ!"
        self.logger.write(msg, 'LV_INFO')
        # 发送邮件给sender
        result = self.sendMailToSender(datas)
        if result != 'OK':
            msg = "Sent mail to sender failed, error is: %s" % str(result)
            self.logger.write(msg, 'LV_WARNING')
            return
        msg = "Sent mail to sender succ!"
        self.logger.write(msg, 'LV_INFO')
        # 发送邮件给特定邮箱
        result = self.sendMailToDedicatedAccount(datas)
        if result != 'OK':
            msg = "Sent mail to dedicated email account failed, error is: %s" % str(result)
            self.logger.write(msg, 'LV_WARNING')
            return
        msg = "Sent mail to dedicated email account succ!"
        self.logger.write(msg, 'LV_INFO')

    def storeSenderMsg(self, datas, archive_dir='./archive/'):
        """
        sender信息存档（文件）
        Args:
            datas: sender信息，字典模式
            archive_dir: sender信息存放的目录
        Returns：
            成功则返回'OK'，失败返回 False
        """
        file_name = datas['first_name'] + ' ' + datas['last_name']
        try:
            if not os.path.isdir(archive_dir):
                os.mkdir(archive_dir)
            f_content = ''
            for item in self.sender_items:
                f_content += "%-15s: %s\n" % (item, datas[item])
            f = open(archive_dir + file_name, 'wb')
            f.write(f_content)
            f.close()
            return 'OK'
        except:
            try:
                f.close()
            except:
                pass
            return False

    def sendMailToSender(self, datas):
        """
        根据post获得的参数发送邮件给sender
        """
        # 邮件接收方、邮件正文、邮件主题的配置
        self.mail_config['mail_to'] = datas['email']
        self.mail_config['mail_body'] = self.mkSenderMailBody(datas['last_name'])
        self.mail_config['Subject'] = "Thanks for your application"
        # 开始配置邮件对象
        self.mail.setConfig(self.mail_config)
        # 发送邮件
        result = self.mail.sendMail()
        return result


    def mkSenderMailBody(self, last_name):
        """
        生成发送给sender的邮件内容
        """
        return "Dear %s,\n\nWe have received your application. Please do NOT reply this email.\n\n\
Thanks,\nTech Team" % last_name

    def sendMailToDedicatedAccount(self, datas):
        """
        根据post获得的参数发送邮件给专用邮箱
        """
        # 邮件接收方、邮件正文、邮件主题的配置
        self.mail_config['mail_to'] = self.mail_config['dedicated_email_account']
        self.mail_config['mail_body'] = self.mkDedicatedMailBody(datas['last_name'], datas['first_name'])
        self.mail_config['Subject'] = "Application Received from %s" % datas['email']
        # 开始配置邮件对象
        self.mail.setConfig(self.mail_config)
        # 发送邮件
        result = self.mail.sendMail()
        return result

    def mkDedicatedMailBody(self, last_name, first_name):
        """
        发送求职者邮箱给专用的邮箱
        """
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        return "Received an application from %s %s at %s" % (last_name, first_name, datetime)

    def getSenderInfo(self, datas):
        """
        获取sender信息
        """
        try:
            datas = eval(datas)
            items = datas.keys()
            if len(items) != 7:
                return False
            for item in self.sender_items:
                if not datas.has_key(item):
                    return False
            return datas
        except Exception as e:
            return False

    def getMailConfig(self, config_file="./config/mail_config"):
        """
        获取服务器邮箱信息，通过配置文件，默认路径为 ./config/mail_config
        """
        f = open(config_file, 'rb')
        f_content = f.read()
        f.close()
        f_content = eval(f_content)
        for item in ['mail_from', 'mail_pwd', 'dedicated_email_account']:
            if not f_content.has_key(item):
                raise Exception("Config error: Without %s" % item)
        return f_content


if __name__ == '__main__':
    try:
        server = HTTPServer(('', 8000), MyRestful)
        print >> sys.stdout, "started httpserver..."
        server.serve_forever()
    except Exception as e:
        print >> sys.stderr, "VERSION: %s" % VERSION
        print >> sys.stderr, "Server Error: %s" % str(e)
