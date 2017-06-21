#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,requests,json,time,random,MySQLdb,datetime
from multiprocessing import Pool
from bs4 import  BeautifulSoup
from selenium import webdriver
reload(sys)
sys.setdefaultencoding('utf8')
area_list = {
             u'罗湖': 'house-a086',
             u'福田': 'house-a085',
             u'龙岗': 'house-a090',
             u'龙华': 'house-a013080',
            }
# area_list = {u'罗湖': 'house-a086',}
urlbase = 'http://zu.sz.fang.com/{0}/c2500-d21000-g21-n31/'
urldetail='http://zu.sz.fang.com'


def mysql_down(msg):
    try:
        SQL = 'insert into test.house (url,typehouse,map,area,price,img_url,info,status,uptime) values("%s","%s","%s","%s",%d,"%s","%s",%d,"%s");' % (
        msg['houseurl'],msg['housetype'], msg['housemap'], msg['housearea'], int(msg['houseprice']), msg['houseimg'], msg['describe'],
        int(msg['status']), msg['updatetime'].replace('/', '-'))
        cursor.execute(SQL)
        db.commit()
    except:
        msg=json.dumps(msg,ensure_ascii=False)
        write_down(msg)



def write_down(msg):
    with open('house.txt','a+') as f:
        f.write(msg)
        f.write('\n')
        f.flush()


def get_house_info(url):
    print url
    driver=webdriver.PhantomJS(service_args=['--load-images=no'])
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(20)
    try:
        driver.get(url)
        status=1
    except:
        status=0
    print 'download html successful'
    try:
        all_info=driver.page_source
        soup=BeautifulSoup(all_info,'lxml',from_encoding='utf8')
        info_a = soup.find_all('ul', class_='house-info')
        info_des = []
        price_house=''
        type_house=''
        area_house=''
        for i in info_a:
            for j in i.find_all('li'):
                try:
                    m_info=j.get_text().replace('\n', '').replace(' ', '')
                except:
                    pass
                else:
                    info_des.append(m_info)
                    if m_info.split('：')[0]==u'租金':
                        price_house=m_info.split('：')[1].split(r'/')[0][:-1]
                    elif m_info.split('：')[0]==u'房屋概况':
                        type_house=m_info.split('：')[1].split(r'|')[1]
                        area_house=m_info.split('：')[1].split(r'|')[2][:-2]
                    else:
                        pass
        info_des = '\n'.join(info_des)
    except:
        info_des=''
    try:
        info_tel = soup.find_all('div', class_='phonewrap')
        info_des += info_tel[0].get_text().replace('\n', '').replace(' ', '')
    except:
        pass
    try:
        info_owner = soup.find_all('div', class_='agent-txt agent-txt-per floatl')[0].get_text().replace('\n', '').replace(
        ' ', '')
        info_des += info_owner
    except:
        pass
    info_image=''
    try:
        info_photo_url = soup.find_all('img', class_='mt10')
        for p in info_photo_url:
            info_image+=(p['data-src']+';')
    except:
        info_photo_url =''
    try:
        info_map = soup.find_all(id='rentid_208')
    except:
        info_map='/None'
    try:
        info_map = 'http://zu.sz.fang.com' + info_map[0]['src']
    except:
        info_map=u'无'
    try:
        info_time = soup.find_all('p', class_='gray9')[0].find_all('span', class_='')[0].get_text()
        info_time = info_time.split('：')[1]
    except:
        info_time=''
    each_info={
                u'describe':info_des,
                u'updatetime':info_time,
                u'houseprice':price_house,
                u'houseimg':info_image,
                u'housemap':info_map,
                u'housetype':type_house,
                u'housearea':area_house,
                u'status':status,
                u'houseurl':url
                 }
    driver.close()
    return each_info


def deal_html(url,cont,area):
    global  max_page
    global  page_now
    try:
        soup=BeautifulSoup(cont,'lxml',from_encoding='utf8')
        max_page = soup.find_all('span', class_='txt')[0].get_text()[1:3]
        page_now = soup.find_all('a', class_='pageNow')[0].get_text()
    except:
        max_page=max_page
        page_now=page_now+1
    try:
        urllist=soup.find_all('div',id='rentid_D10_01')[0].find_all('a')
        for list_per  in urllist:
            re_sta=list_per.get_text()
            if re_sta==u'下一页':
                next_url=urldetail+list_per['href']
    except:
        next_url=url
    if int(page_now)<=int(max_page):
        try:
            house_info=soup.find_all('dd',class_='info rel')
        except:
            return url
        else:
            for i in house_info:
                detail_info=get_house_info(urldetail+i.find_all('a')[0]['href'])
                mysql_down(detail_info)
                ran_time=random.randint(1,4)
                time.sleep(ran_time)
            print '%s ok' %page_now
            if int(page_now)==int(max_page):
                return 'end'
            else:
                return next_url
    else:
        print '%s area ok' %area
        return 'end'


def get_info(url,position):
    html_info=requests.get(url).text
    Flag=deal_html(url,html_info,position)
    if Flag != 'end':
        return get_info(Flag,position)


def main():
    p = Pool(4)
    for i,j in area_list.items():
        url=urlbase.format(j)
        p.apply_async(get_info,(url,i))
    p.close()
    p.join()

if __name__=="__main__":
    max_page=1
    page_now=1
    # urllist_xx={}
    db = MySQLdb.connect("127.0.0.1", "root", "171024", "test")
    db.set_character_set('utf8')
    cursor = db.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    main()
    db.close()



