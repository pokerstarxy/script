#!/usr/bin/env python
#coding=utf8

#pip install itchat  运行这个
import  itchat,re,time,requests,smtplib,json,os,sys
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
#图灵api
def tuling_api(info):
    api_key = 'd2ce0ef74fa64f13964270d90dec6652'
    api_url = 'http://www.tuling123.com/openapi/api'
    data={
        'key':api_key,
        'info':info,
        'userid':'webchat',
    }
    return requests.post(api_url,data=data)

#邮件
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

#计时
def gettime():
    timexx=time.strftime("%Y%m%d%H%M%S", time.localtime())
    strtime=time.strptime(timexx, '%Y%m%d%H%M%S')
    time1 = time.mktime(strtime)
    return time1

#用户名
def getusername(name):
    return name

#传输二维码
def trans_photos():
    path=os.path.join(os.path.dirname("__file__"),'itchat.pkl')
    with open (path,'rb+') as f:
        cont=f.read()

#本地存储
def msg_store(msg):
    with open('msg.bak','a+') as f:
        f.writelines(msg)
        f.writelines('\n')


def send_msg(reply_content):
    reply_content = json.loads(reply_content)
    results = ''
    del reply_content[u'code']
    results = '\n'.join(reply_content.values())
    return results

# def handle_chat():
@itchat.msg_register([TEXT, PICTURE, MAP, CARD, NOTE, SHARING,RECORDING, ATTACHMENT, VIDEO])
def text_reply(msg):
    global user_status
    global user_name
    friend = itchat.search_friends(userName=msg['FromUserName'])
    if friend['NickName'] == user_name:
        if msg['Text']=='up':
            user_status=True
        elif msg['Text']=='down':
            user_status=False
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
            reply_content = u"图片: " + msg['FileName']
        elif msg['Type'] == 'Card':
            reply_content = u" " + msg['RecommendInfo']['NickName'] + u" 的名片"
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
            reply_content = u"通知"
        elif msg['Type'] == 'Sharing':
            reply_content = u"分享"
        elif msg['Type'] == 'Recording':
            reply_content = u"语音"
        elif msg['Type'] == 'Attachment':
            reply_content = u"文件: " + msg['FileName']
        elif msg['Type'] == 'Video':
            reply_content = u"视频: " + msg['FileName']
        else:
            reply_content = {u'text': u'你发的是什么科技啊！', u'code': u'error'}
        if not user_status:
            # itchat.send(u'我不在线哦~,有事情先说！以下是机器人的回复',toUserName=msg['FromUserName'])
            itchat.send(u"Friend:%s -- %s  \n"
                        u"Time:%s    \n"
                        u" Message:%s" % (friend['NickName'], friend['RemarkName'], time.ctime(), receive_cont),
                        toUserName='filehelper')
            if msg["Type"]=='Text':
                itchat.send('%s' %send_msg(reply_content),toUserName=msg['FromUserName'])
            else:
                itchat.send(u"我已经收到你在【%s】发送的消息,稍后回复。--微信助手" % (time.ctime(),), toUserName=msg['FromUserName'])
        else:
            itchat.send(u"Friend:%s -- %s  \n"
                        u"Time:%s    \n"
                        u" Message:%s \n"
                        u"recommend:%s" % (friend['NickName'], friend['RemarkName'], time.ctime(), receive_cont,send_msg(reply_content)),
                        toUserName='filehelper')

def main():
    itchat.auto_login(hotReload=True)
    itchat.run()

if __name__ == "__main__":
    user_name = getusername("qwert")
    main()




