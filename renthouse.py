#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,requests,json,time
from bs4 import  BeautifulSoup
from selenium import webdriver
reload(sys)
sys.setdefaultencoding('utf8')
# area_list = {
#              u'罗湖': 'house-a086',
#              u'福田': 'house-a085',
#              u'龙岗': 'house-a090',
#              u'龙华': 'house-a013080',
#             }
area_list = {u'罗湖': 'house-a086',}
urlbase = 'http://zu.sz.fang.com/{0}/c2500-d21000-g21-n31/'
urldetail='http://zu.sz.fang.com'


def write_down(msg):
    with open('house.txt','a+') as f:
        f.write(msg)
        f.write('\n')
        f.flush()


def get_house_info(url):
    print url
    driver=webdriver.PhantomJS(service_args=['--load-images=no'])
    driver.get(url)
    print 'download html successful'
    all_info=driver.page_source
    soup=BeautifulSoup(all_info,'lxml',from_encoding='utf8')
    info_a = soup.find_all('ul', class_='house-info')
    info_des = []
    price_house=''
    type_house=''
    area_house=''
    for i in info_a:
        for j in i.find_all('li'):
            m_info=j.get_text().replace('\n', '').replace(' ', '')
            info_des.append(m_info)
            if m_info.split('：')[0]==u'租金':
                price_house=m_info.split('：')[1].split(r'/')[0][:-1]
            elif m_info.split('：')[0]==u'房屋概况':
                type_house=m_info.split('：')[1].split(r'|')[1]
                area_house=m_info.split('：')[1].split(r'|')[2][:-2]
            else:
                pass
    info_des = '\n'.join(info_des)
    info_tel = soup.find_all('div', class_='phonewrap')
    info_des+=info_tel[0].get_text().replace('\n', '').replace(' ', '')
    info_owner = soup.find_all('div', class_='agent-txt agent-txt-per floatl')[0].get_text().replace('\n', '').replace(
        ' ', '')
    info_des += info_owner
    info_image=[]
    info_photo_url = soup.find_all('img', class_='mt10')
    for p in info_photo_url:
         info_image.append(p['data-src'])
    info_map = soup.find_all(id='rentid_208')
    try:
        info_map = 'http://zu.sz.fang.com' + info_map[0]['src']
    except:
        info_map=u'无'
    info_time = soup.find_all('p', class_='gray9')[0].find_all('span', class_='')[0].get_text()
    info_time = info_time.split('：')[1]
    each_info={
                u'describe':info_des,
                u'updatetime':info_time,
                u'houseprice':price_house,
                u'houseimg':info_image,
                u'housemap':info_map,
                u'housetype':type_house,
                u'housearea':area_house,
                 }
    driver.close()
    return each_info


def deal_html(url,cont,area):
    soup=BeautifulSoup(cont,'lxml',from_encoding='utf8')
    house_info=soup.find_all('dd',class_='info rel')
    for i in house_info:
        detail_info=get_house_info(urldetail+i.find_all('a')[0]['href'])
        detail_info=json.dumps(detail_info,ensure_ascii=False)
        write_down(detail_info)
        time.sleep(5)
    return 'end'


def get_info(url,position):
    html_info=requests.get(url).text
    Flag=deal_html(url,html_info,position)
    if Flag != 'end':
        return get_info(url,position)


def main():
    for i,j in area_list.items():
        url=urlbase.format(j)
        get_info(url,i)


if __name__=="__main__":
    with open('house.txt', 'w') as f:
        pass
    main()



#多线程,最后一页，再加数据库，还有异常捕捉