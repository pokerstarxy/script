#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests,re,sys,random,time,json,MySQLdb
from bs4 import BeautifulSoup
from multiprocessing import Pool
reload(sys)
sys.setdefaultencoding('utf8')
urlbase='https://sz.zu.anjuke.com/fangyuan/{0}/fx1-je1500-js500/'
area_list=['futian','luohu','yantian','longhua','longgang']
# area_list=['longgang','futian']
db = MySQLdb.connect("127.0.0.1", "root", "171024", "test")
db.set_character_set('utf8')
cursor = db.cursor()
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]
headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "User-Agent":random.choice(USER_AGENTS)
            }
proxy_list=['']
proxies=''


def get_proxy(num):
    r = requests.get(('http://127.0.0.1:8000/?types=0&count=%s&country=国内') %num)
    proxies_list = json.loads(r.text)
    for each_proxy in proxies_list:
        ip = each_proxy[0]
        port = each_proxy[1]
        proxy_list = proxy_list.append([('http','http://%s:%s' % (ip, port))])
    return proxy_list


def get_html(url):
    global proxies
    rest_time=random.randint(50,100)
    rest_time=float(rest_time)/100+2
    time.sleep(rest_time)
    bd_session = requests.Session()
    try:
        results=bd_session.get(url,headers=headers,proxies=proxies)
    except Exception:
        print '---------------- get url wrong'
        proxies=dict(get_proxy('1').pop())
    else:
        if results.headers.get('Set-Cookie',''):
            return results.text
        else:
            if proxy_list:
                proxies = dict(get_proxy('30').pop())
            else:
                proxies=dict(proxy_list.pop())
            print '-----------------------'+proxies
    get_html(url)


def msg_down(msg):
    with open('house.txt','a+')as f:
        cont=json.dumps(msg)
        f.write(cont)
        f.write('\n')


def mysql_down(msg):
    SQL = 'insert into mydjango.houseajk (photo_house_url,agent_name,agent_phone,agent_company,price_house,' \
          'size_house,map_house,house_detail,propty_house,url_house,release_time) ' \
          'values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s");' % ((msg['photo_house_url'],msg['agent_name'],
             msg['agent_phone'], msg['agent_company'], msg['price_house'], msg['size_house'],
                    msg['map_house'],MySQLdb.escape_string(msg['house_detail']), msg['propty_house'],msg['url_house'],msg['release_time']))
    try:
        cursor.execute(SQL)
    except Exception as e:
        msg = json.dumps(msg, ensure_ascii=False)
        msg_down(msg)
        print SQL
        print e
    db.commit()


def each_page(url):
    print 'download %s' %url
    house_simple =''
    size_house = ''
    propty_house=''
    html=get_html(url)
    soup=BeautifulSoup(html,'lxml')
    try:
        photo_house_url=soup.find_all('img',attrs={'src':re.compile(r'^https://pic1.ajkimg.com')})
        photo_house_url = [x['src'] for x in photo_house_url]
    except:
        photo_house_url=''
    try:
        agent_name = soup.find(id='broker_true_name').get_text()
    except:
        agent_name='nobody'
    try:
        agent_phone=soup.find('p',class_='broker-mobile').get_text().replace(' ','')
    except AttributeError:
        agent_phone=soup.find('i',class_='p_icon icon_tel').get_text().replace(' ','')
    except:
        agent_phone=''
    try:
        agent_company=soup.find('div',class_='broker-company').get_text().split('：')[-1].replace('\n','')
    except:
        agent_company=u'个人'
    try:
        price_house = soup.find('span', class_='f26').get_text()
    except:
        price_house=''
    try:
        house_simple_bak=soup.find_all('dl',class_='p_phrase cf')
    except:
        house_simple_bak=[]
    try:
        release_time=soup.find('div', class_=['text-mute', 'extra-info']).get_text().split('：')[-1]
        release_time='/'.join([release_time[:4],release_time[5:7],release_time[8:10]])
    except:
        release_time='2017/07/22'
    for info in house_simple_bak:
        ea_info=info.dd.get_text()
        if re.search(u'平米',ea_info):
            if re.search(u'平米/',ea_info):
                propty_house=ea_info[:-6]
            else:
                size_house=ea_info[:-2]
        house_simple=house_simple+ea_info
    try:
        house_detail=soup.find('div',class_='pro_detail').get_text()
        house_detail=house_simple.replace(' ','').replace('\n','')+'\n'+house_detail.replace(' ','').replace('\n','')
    except:
        house_detail=''
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
        'url_house':url,
        'release_time':release_time,
               }
    return house_info


def get_page_url(url,place):
    html=get_html(url)
    soup=BeautifulSoup(html,'lxml')
    page_house=soup.find_all('div',class_='zu-itemmod')
    page_now=soup.find('i',class_='curr').get_text()
    try:
        next_page=soup.find('a',class_='aNxt').get('href')
    except AttributeError :
        next_page=''
    for per_houose in [x['link'] for x in page_house]:
        house_info=each_page(per_houose)
        mysql_down(house_info)
        print ' %s  infomation save successful' %per_houose
    print '%s download %s complete ' %(place,page_now)
    if next_page:
        get_page_url(next_page,place)

if __name__=='__main__':
    p = Pool(4)
    for place in area_list:
        url=urlbase.format(place)
        # get_page_url(url,place)
        p.apply_async(get_page_url,(url,place))
    p.close()
    p.join()
    db.close()