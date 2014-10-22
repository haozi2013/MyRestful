#!/usr/bin/python
# -*- coding: utf-8 -*-

"mail 0.1.0"
#
# 功能：发送邮件
#
# 目前支持smtp服务

import smtplib
import time
from email.mime.text import MIMEText


class Mail():
    def setConfig(self, config):
        #正文
        self.mail_body = config['mail_body']
        #收信邮箱
        self.mail_to = config['mail_to']
        #发信邮箱
        self.mail_from = config['mail_from']
        #发信用户和邮箱后缀 
        self.mail_user = config['mail_from']
        self.mail_postfix = self.mail_from.split('@')[1]
        #发信用户密码
        self.mail_pwd = config['mail_pwd']
        #发信的SMTP服务器地址
        self.mail_host = 'smtp.' + self.mail_postfix
        #定义正文
        self.msg = MIMEText(self.mail_body)
        #定义
        self.msg['Subject'] = config['Subject']
        #定义发信邮箱
        self.msg['From'] = self.mail_from
        self.msg['To'] = self.mail_to
        self.msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

    def sendMail(self):
        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.mail_host)
            smtp.login(self.mail_user, self.mail_pwd)
            reslut = smtp.sendmail(self.mail_from, self.mail_to, self.msg.as_string())
            smtp.close()
            if reslut == {}:
                return 'OK'
            return result
        except Exception as e:
            return str(e)