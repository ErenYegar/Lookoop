#!/usr/bin/python
# coding: utf-8

import sys
import os
import django
from django.core.management import execute_from_command_line
import shlex
import urllib
import socket
import subprocess


jms_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(jms_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'jumpserver.settings'
if django.get_version() != '1.6':
    setup = django.setup()

from juser.user_api import db_add_user, get_object, User
from install import color_print
from jumpserver.api import get_mac_address, bash

socket.setdefaulttimeout(2) #2秒后超时


class Setup(object):
    """
    安装jumpserver向导
    """

    def __init__(self):
        self.admin_user = 'admin'
        self.admin_pass = '5Lov@wife'

    @staticmethod
    def _pull(): 
        color_print('开始更新jumpserver', 'green') 
        #应该是记录安装jumpserver的主机数目
        # bash('git pull')
        try:
            mac = get_mac_address()
            '''
            def get_mac_address():
                node = uuid.getnode()
                mac = uuid.UUID(int=node).hex[-12:]
                return mac
            '''
            version = urllib.urlopen('http://jumpserver.org/version/?id=%s' % mac)
        except:
            pass

    def _input_admin(self):
        while True:
            print
            admin_user = raw_input('请输入管理员用户名 [%s]: ' % self.admin_user).strip()
            admin_pass = raw_input('请输入管理员密码: [%s]: ' % self.admin_pass).strip()
            admin_pass_again = raw_input('请再次输入管理员密码: [%s]: ' % self.admin_pass).strip()

            if admin_user:
                self.admin_user = admin_user

            if not admin_pass_again:
                admin_pass_again = self.admin_pass

            if admin_pass:
                self.admin_pass = admin_pass

            if self.admin_pass != admin_pass_again:
                color_print('两次密码不相同请重新输入')
            else:
                break
            print

    @staticmethod
    def _sync_db():
        os.chdir(jms_dir) #改变当前工作目录到指定文件下
        execute_from_command_line(['manage.py', 'syncdb', '--noinput']) #本命令会修复SQL的匹配问题，同步数据库，生成管理界面使用的额外的数据库表

    def _create_admin(self):
        user = get_object(User, username=self.admin_user)
        if user:
            user.delete()
        db_add_user(username=self.admin_user, password=self.admin_pass, role='SU', name='admin', groups='',
                    admin_groups='', email='admin@jumpserver.org', uuid='MayBeYouAreTheFirstUser', is_active=True)
        cmd = 'id %s 2> /dev/null 1> /dev/null || useradd %s' % (self.admin_user, self.admin_user)
        '''
        &  表示任务在后台执行，如要在后台运行redis-server,则有  redis-server &
        && 表示前一条命令执行成功时，才执行后一条命令 ，如 echo '1‘ && echo '2'
        | 表示管道，上一条命令的输出，作为下一条命令参数，如 echo 'yes' | wc -l
        || 表示上一条命令执行失败后，才执行下一条命令，如 cat nofile || echo "fail"
        '''
        shlex.os.system(cmd)

    @staticmethod
    def _chmod_file():
        os.chdir(jms_dir) #工作路径移动到当前目录下
        os.chmod('init.sh', 0755)
        os.chmod('connect.py', 0755)
        os.chmod('manage.py', 0755)
        os.chmod('run_server.py', 0755)
        os.chmod('service.sh', 0755)
        os.chmod('logs', 0777)
        os.chmod('keys', 0777)

    @staticmethod
    def _run_service():
        cmd = 'bash %s start' % os.path.join(jms_dir, 'service.sh') #$1结果未出
        shlex.os.system(cmd)
        print
        color_print('安装成功，Web登录请访问http://ip:8000, 祝你使用愉快。\n请访问 https://github.com/jumpserver/jumpserver/wiki 查看文档', 'green')

    def start(self):
        print "开始安装Jumpserver ..."
        self._pull()
        self._sync_db()
        self._input_admin()
        self._create_admin()
        self._chmod_file()
        self._run_service()


if __name__ == '__main__':
    setup = Setup()
    setup.start()
