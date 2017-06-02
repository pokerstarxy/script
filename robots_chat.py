#!/usr/bin/env python
#coding=utf8
import  itchat,re,time,requests,smtplib,json,os
from itchat.content import *
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


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
    server.login('pokerstar_xy@sina.com', 'xy906307')
    server.sendmail("pokerstar_xy@sina.com", "pokerstarxy@qq.com", msg.as_string())
    server.quit()


@itchat.msg_register([TEXT, PICTURE, MAP, CARD, NOTE, SHARING,RECORDING, ATTACHMENT, VIDEO])
def text_reply(msg):
    friend = itchat.search_friends(userName=msg['FromUserName'])
    print friend['NickName']
    if msg['Type'] == 'Text' :
        receive_cont=msg['Text']
        msg_info = "%s:  %s--%s " % (time.ctime(), msg['NickName'], receive_cont)
        msg_store(msg_info)
        try:
            reply_content = tuling_api(receive_cont).text
        except Exception as e:
            reply_content = {u'text':u'机器人出了故障哦', u'code':u'error'}
            mailme()
    else:
        reply_content = {u'text':u'你发的是什么科技啊！',u'code':u'error'}
    reply_content = json.loads(reply_content)
    results = ''
    del reply_content[u'code']
    ##多层次嵌套字典处理
    results='\n'.join(reply_content.values())
    itchat.send(u"Friend:%s -- %s    "
                u"Time:%s    "
                u" Message:%s" % (friend['NickName'], friend['RemarkName'], time.ctime(), receive_cont),
                toUserName='filehelper')

    itchat.send(results, toUserName=msg['FromUserName'])
    # itchat.send(u"我已经收到你在【%s】发送的消息,稍后回复。--微信助手" % (time.ctime(),),toUserName=msg['FromUserName'])
    #                     toUserName=msg['FromUserName'])


def msg_back(reply,msg):
    pass


def trans_photos():
    path=os.path.join(os.path.dirname("__file__"),'itchat.pkl')
    with open (path,'rb+') as f:
        cont=f.read()

def msg_store(msg):
    with open('msg.bak','a+') as f:

        f.write(msg)


def main():
    try:
        itchat.auto_login(hotReload=True)
        itchat.run()
    except ConnectionError as e:
        print e.message


if __name__ == "__main__":
    main()




