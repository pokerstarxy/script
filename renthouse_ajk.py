#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re,sys,random,time,json
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')
urlbase='https://sz.zu.anjuke.com/fangyuan/{0}/fx1-je1500-js500/'
# area_list=['longgang','futian','luohu','yantian','longhua']
area_list=['futian','yantian']
headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
            }


def get_html(url):
    rest_time=random.randint(2,5)
    time.sleep(rest_time)
    bd_session = requests.Session()
    results=bd_session.get(url,headers=headers)
    return results.text


def msg_down(msg):
    with open('house.txt','a+')as f:
        cont=json.dumps(msg)
        f.write(cont)
        f.write('\n')


def each_page(url):
    print 'download %s' %url
    house_simple =''
    size_house = ''
    propty_house=''
    html=get_html(url)
    soup=BeautifulSoup(html,'lxml')
    photo_house_url=soup.find_all('img',attrs={'src':re.compile(r'^https://pic1.ajkimg.com')})
    photo_house_url=[x['src'] for x in photo_house_url]
    agent_name=soup.find('h2',id='broker_true_name').get_text()
    agent_phone=soup.find('p',class_='broker-mobile').get_text().replace(' ','')
    agent_company=soup.find('div',class_='broker-company').get_text().split('：')[-1].replace('\n','')
    price_house = soup.find('span', class_='f26').get_text()
    house_simple_bak=soup.find_all('dl',class_='p_phrase cf')
    for info in house_simple_bak:
        ea_info=info.dd.get_text()
        if re.search(u'平米',ea_info):
            if re.search(u'平米/',ea_info):
                propty_house=ea_info[:-6]
            else:
                size_house=ea_info[:-2]
        house_simple=house_simple+ea_info
    house_detail=soup.find('div',class_='pro_detail').get_text()
    house_detail=house_simple.replace(' ','').replace('\n','')+'\n'+house_detail.replace(' ','').replace('\n','')
    try:
        map_house=soup.find('a',attrs={'class':'f12','id':''})['href']
    except :
        map_house=''
    house_info={
        'photo_house_url':photo_house_url,
        'agent_name':agent_name,
        'agent_phone':agent_phone,
        'agent_company':agent_company,
        'price_house':price_house,
        'size_house':size_house,
        'map_house':map_house,
        'house_detail':house_detail,
        'propty_house':propty_house,
               }
    return house_info


def get_page_url(url,place):
    html=get_html(url)
    soup=BeautifulSoup(html,'lxml')
    page_house=soup.find_all('div',class_='zu-itemmod')
    page_now=soup.find('i',class_='curr').get_text()
    next_page=soup.find('a',class_='aNxt').get('href','')
    for per_houose in [x['link'] for x in page_house]:
        house_info=each_page(per_houose)
        msg_down(house_info)
        print ' %s  infomation save successful' %per_houose
    print '%s download %s complete ' %(place,page_now)
    if next_page:
        get_page_url(next_page,place)


for place in area_list:
    url=urlbase.format(place)
    get_page_url(url,place)