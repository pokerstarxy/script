#!/usr/bin/env python
#-*- coding:utf8 -*-
# Author Pokerstarxy 2017-06-02 13:12:44
# Email pokerstarxy@sina.com



# elif msg['Type'] == 'Picture':
#     reply_content = u"图片: " + msg['FileName']
# elif msg['Type'] == 'Card':
#     reply_content = u" " + msg['RecommendInfo']['NickName'] + u" 的名片"
# elif msg['Type'] == 'Map':
#     x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(
#         1,
#         2,
#         3)
#     if location is None:
#         reply_content = u"位置: 纬度->" + x.__str__() + u" 经度->" + y.__str__()
#     else:
#         reply_content = u"位置: " + location
# elif msg['Type'] == 'Note':
#     reply_content = u"通知"
# elif msg['Type'] == 'Sharing':
#     reply_content = u"分享"
# elif msg['Type'] == 'Recording':
#     reply_content = u"语音"
# elif msg['Type'] == 'Attachment':
#     reply_content = u"文件: " + msg['FileName']
# elif msg['Type'] == 'Video':
#     reply_content = u"视频: " + msg['FileName']
