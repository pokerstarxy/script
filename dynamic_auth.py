#!/usr/bin/env python
#-*- coding:utf8 -*-
# Author Pokerstarxy 2017-05-31 14:51:48
# Email pokerstarxy@sina.com


import random,time,paramiko,smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def info_mail(name,cont):
    """
    sending E-mail;
    :return: 
    """
    subject_cont = u"Tips -- 关于动态生成验证信息的提示(lvbu)"
    msg = MIMEText(cont, 'plain', 'utf-8')
    msg["From"] = formataddr(["test", "xx@sina.com"])
    msg['To'] = formataddr([u"user", name])
    msg['Subject'] = subject_cont
    server = smtplib.SMTP("smtp.sina.com")
    server.login('xx@sina.com', 'passwd')
    server.sendmail("xx@sina.com", name, msg.as_string())
    server.quit()


# def ran_num_bak():
#     ran_str=[]
#     for i in xrange(8):
#         if i<4:
#             num = random.randint(65,91)    #letter
#             per_str = str(chr(num)).lower() if num % 2 == 0 else str(chr(num))
#         elif 4 <= i < 7:
#             num = random.randint(48,58)   #number
#             per_str=str(chr(num))
#         else:
#             num = random.randint(33,48)    #special sign
#             per_str=str(chr(num))
#         ran_str.append(per_str)
#     return "".join(ran_str)


def ran_num(mode):
    ran_str=[]
    if mode == 'u':
        for i in xrange(4):
            num = random.randint(48, 58)
            ran_str.append(str(chr(num)))
    else:
        for i in xrange(6):
            num = random.randint(97, 123)
            ran_str.append(str(chr(num)))
    return "".join(ran_str)





def user_info():
    """
    produce  random info 
    :return username,userpwd: 
    """
    return (ran_num('u'),ran_num('p'))



def exec_command(ip,hostname,hostpwd):
    """
    update userinfo everyday
    :return: 
    """
    username,userpwd=user_info()
    local_time=time.asctime(time.localtime(time.time()))
    com_line='ls'
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, hostname, hostpwd, timeout=5, allow_agent=False, look_for_keys=False)
        stdin, stdout, stderr = ssh.exec_command(com_line)

    except Exception as e:
        msg="localtime:%s:" \
            "msg:%s" \
            "Please check the problem!"%(local_time,e.message)
        info_mail("xx@qq.com",msg)
        raise
    else:
        if stderr.read() == '':
            msg="date:%s \n" \
                "username:%s \n" \
                "userpasswd:%s" %(local_time,username,userpwd)
        else:
            msg="date:%s \n" \
                "error:" %(local_time,stderr.read())
        info_mail("xx@qq.com",msg)
    finally:
        ssh.close()



if __name__ == "__main__":
    exec_command()

