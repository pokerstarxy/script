#!/usr/bin/env python
#-*- coding:utf8 -*-
# Author Pokerstarxy 2017-05-31 14:51:48
# Email pokerstarxy@sina.com

import random,time,commands,smtplib
from email.mime.text import MIMEText
from email.utils import formataddr



"""
zhouyuan@ic.net.cn
 'zhouyuan@ic.net.cn',  'wangxuan@ic.net.cn', 'zll@ic.net.cn', 'lidong@dzji.com','jiajing@ic.net.cn'
"""


def info_mail(name,cont):
    """
    sending E-mail;
    :return: 
    """
    if type(name)==str:
        msg['To'] = formataddr([u"user", name])
    else:
        msg['To'] = ','.join(name)
    subject_cont = u"Tips -- 关于动态生成验证信息的提示(lvbu)"
    msg = MIMEText(cont, 'plain', 'utf-8')
    msg["From"] = formataddr(["icgoo", "pokerstar_xy@sina.com"])
    msg['Subject'] = subject_cont
    server = smtplib.SMTP("smtp.sina.com")
    server.login('pokerstar_xy@sina.com', 'xy906307')
    server.sendmail("pokerstar_xy@sina.com", name, msg.as_string())
    server.quit()


def ran_num(mode):
    ran_str=[]
    if mode == 'u':
        for i in xrange(4):
            num = random.randint(97, 123)
            ran_str.append(str(chr(num)))
    elif mode == 'p':
        for i in xrange(6):
            num = random.randint(48, 58)
            ran_str.append(str(chr(num)))
    else:
        pass
    return "".join(ran_str)


def user_info():
    """
    produce  random info 
    :return username,userpwd: 
    """
    return (ran_num('u'),ran_num('p'))


def exec_command():
    """
    update userinfo everyday
    :return: 
    """
    username,userpwd=user_info()
    local_time=time.asctime(time.localtime(time.time()))
    # com_line='sudo printf "%s:$(openssl passwd -crypt %s)\n" > /home/yunwei/nginx/conf/basic_auth' %(username,userpwd)
    com_line='ls'
    try:
        status,output=commands.getstatusoutput(com_line)
    except Exception as e:
        msg="localtime:%s:" \
            "msg:%s" \
            "Please check the problem!"%(local_time,e.message)
        info_mail("pokerstarxy@qq.com",msg)
        raise
    else:
        print output
        if status == 0:
            msg="date:%s \n" \
                "username:%s \n" \
                "userpasswd:%s" %(local_time,username,userpwd)
            info_mail(mailto_list,msg)
        else:
            msg="date:%s \n" \
                "error:" %(local_time,output)
            info_mail("pokerstarxy@qq.com",msg)
        # info_mail("lidong@dzji.com",msg)


if __name__ == "__main__":
    mailto_list=[]
    exec_command()

