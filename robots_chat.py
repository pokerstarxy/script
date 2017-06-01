#!/usr/bin/env python
#coding=utf8
import  itchat,re,time,requests,smtplib,json
from itchat.content import *
from email import encoders
from email.header import Header
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


def main():
    @itchat.msg_register([TEXT, PICTURE, MAP, CARD, NOTE, SHARING,RECORDING, ATTACHMENT, VIDEO])
    def text_reply(msg):
        friend = itchat.search_friends(userName=msg['FromUserName'])
        if msg['Type'] == 'Text' :
            if friend['NickName']!='qwert':
                reply_content=msg['Text']
                try:
                    reply_bak = tuling_api(reply_content).text
                    reply_bak=json.loads(reply_bak)
                except Exception:
                    reply_bak = u'网络不好哦'
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
            reply_content = u"你发的是什么科技啊！"
        if friend['NickName']!='qwert':
            if reply_content!="<Response [200]>":
                itchat.send(u"Friend:%s -- %s    "
                            u"Time:%s    "
                            u" Message:%s" % (friend['NickName'], friend['RemarkName'], time.ctime(), reply_content),
                            toUserName='filehelper')
            if msg['Type']!='Text':
                itchat.send(u"我已经收到你在【%s】发送的消息,稍后回复。--微信助手" % (time.ctime(), ),
                            toUserName=msg['FromUserName'])
            else:
                results=''

                del reply_bak[u'code']
                for p,q in reply_bak.items():
                    results=results+"%s:%s\n" %(p,q)
                itchat.send(results,toUserName=msg['FromUserName'])
    itchat.auto_login(hotReload=True)
    itchat.run()


if __name__ == "__main__":
    main()




