#!/usr/bin/env python
#-*- coding:utf8 -*-
# Author Pokerstarxy 2017-07-04 09:23:51
# Email pokerstarxy@sina.com
#pip install itchat  运行这个
import itchat,re,time,requests,smtplib,json,os,sys,shutil
from itchat.content import *
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
reload(sys)
sys.setdefaultencoding('utf8')
user_status = False    #用户是否在线
time_reply=''          #回复时间
code_type={'100000':u"文本类",
           '200000':u"链接类",
           '302000':u'新闻类',
           '308000':u'菜谱类'
           }
error_code=['40001','40002','40004','40007']
dirname=['file','image','media','voice']


def tuling_api(info):
    api_key = 'd2ce0ef74fa64f13964270d90dec6652'
    api_url = 'http://www.tuling123.com/openapi/api'
    data={
        'key':api_key,
        'info':info,
        'userid':'webchat',
    }
    return requests.post(api_url,data=data)


def mailme():
    subject_cont = u"温馨提示--关于微信错误提示"
    cont = u"robots wrong！"
    msg = MIMEText(cont, 'plain', 'utf-8')
    msg["From"] = formataddr(["webchat", "pokerstar_xy@sina.com"])
    msg['To'] = formataddr([u"me", "pokerstartxy@qq.com"])
    msg['Subject'] = subject_cont
    server = smtplib.SMTP("smtp.sina.com")
    server.login('test_code@sina.com', 'pwd@test')
    server.sendmail("test_code@sina.com", "pokerstarxy@qq.com", msg.as_string())
    server.quit()


def getusername(name):
    return name


def msg_store(msg):
    with open('msg.bak','a+') as f:
        f.writelines(msg)
        f.writelines('\n')


def send_msg(reply_content):
    reply_content = json.loads(reply_content)
    results = ''
    if reply_content[u'code'] in error_code:
        return u'something wrong'
    else:
        del reply_content[u'code']
        results = '\n'.join(reply_content.values())
        """目前没看到list形式的返回，无法测试"""
        return results


@itchat.msg_register([TEXT, PICTURE, MAP, CARD, NOTE, SHARING,RECORDING, ATTACHMENT, VIDEO])
def text_reply(msg):
    global user_status
    global user_name
    global basedir
    friend = itchat.search_friends(userName=msg['FromUserName'])
    if friend['NickName'] == user_name:
        if msg['Text']=='up':
            user_status=True
        elif msg['Text']=='down':
            user_status=False
        elif msg['Text']=='clearall':
            for listdir in dirname:
                pathname=os.path.join(basedir, listdir)
                shutil.rmtree(pathname)
                os.mkdir(pathname)
            itchat.send(u'clear', toUserName='filehelper')
        else:
            pass
    else:
        if msg['Type'] == 'Text':
            receive_cont = msg['Text']
            msg_info = "%s:  %s--%s " % (time.ctime(), friend['NickName'], receive_cont)
            msg_store(msg_info)
            try:
                reply_content = tuling_api(receive_cont).text
            except Exception as e:
                reply_content = {u'text': u'机器人出了故障哦', u'code': u'error'}
                mailme()
        elif msg['Type'] == 'Picture':
            reply_content = u"图片已经远程存储在电脑上"
            msg['Text']('image/'+msg['FileName'])
        elif msg['Type'] == 'Card':
            reply_content = msg['RecommendInfo']['NickName'] + u"已被添加 \n"
        elif msg['Type'] == 'Map':
            x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(
                1,
                2,
                3)
            if location is None:
                reply_content = u"位置: 纬度->" + x.__str__() + u" 经度->" + y.__str__()
            else:
                reply_content = u"位置: " + location
        elif msg['Type'] == 'Note':
            reply_content = u"笔记"
        elif msg['Type'] == 'Sharing':
            reply_content = "%s \n%s" %(msg['FileName'],msg['Url'])
        elif msg['Type'] == 'Recording':
            reply_content = u"语音已经远程存储在电脑上"
            msg['Text']('voice/'+msg['FileName'])
        elif msg['Type'] == 'Attachment':
            reply_content = u"文件已经远程存储在电脑上"
            msg['Text']('file/'+msg['FileName'])
        elif msg['Type'] == 'Video':
            reply_content = u"视频已经远程存储在电脑上"
            msg['Text']('media/'+msg['FileName'])
        else:
            reply_content = {u'text': u'你发的是什么科技啊！', u'code': u'error'}
        if not user_status:
            if msg["Type"] != 'Text':
                receive_cont=reply_content
            else:
                itchat.send('%s  ^--robots--^' % send_msg(reply_content), toUserName=msg['FromUserName'])
            itchat.send(u"Friend:%s -- %s  \n"
                        u"Time:%s    \n"
                        u" Message:%s" % (friend['NickName'], friend['RemarkName'], time.ctime(), receive_cont),
                        toUserName='filehelper')
        else:
            if msg["Type"] != 'Text':
                receive_cont=reply_content
            else:
                pass
            itchat.send(u"Friend:%s -- %s  \n"
                        u"Time:%s    \n"
                        u" Message:%s \n"
                        u"recommend:%s" % (friend['NickName'], friend['RemarkName'], time.ctime(), receive_cont,send_msg(reply_content)),
                        toUserName='filehelper')


@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.get_contract()
    itchat.send_msg(msg['RecommendInfo']['UserName'], 'Nice to meet you!')


def logon_t00ls(cont_msg):
    offical_account=itchat.get_mps()
    for eachone in offical_account:
        if eachone['PYQuanPin']== 'T00ls':
            gzh_id=eachone['UserName']
            for  i in cont_msg:
                itchat.send(i,gzh_id)
        else:
            pass


def main():
    global basedir
    for i in dirname:
        listdir=os.path.join(basedir,i)
        if os.path.exists(listdir):
            pass
        else:
            os.mkdir(listdir)
    itchat.auto_login(hotReload=True)
    # logon_t00ls(['3','4'])
    itchat.run()

if __name__ == "__main__":
    basedir = os.path.dirname(__file__)
    user_name = getusername("qwert")
    main()







