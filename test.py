# -*- coding:utf-8 -*-
import urllib
import re, codecs
import time, random
import requests
from lxml import html
from urllib import parse

key = '数据分析'
key = parse.quote(parse.quote(key))
headers = {'Host': 'search.51job.com',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


def get_links(page):
    url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,' + key + ',2,' + str(page) + '.html'
    r = requests.get(url, headers, timeout=10)
    s = requests.session()
    s.keep_alive = False
    r.encoding = 'gb18030'
    reg = re.compile(
        r'class="t1 ">.*? <a target="_blank" title=".*?" href="(.*?)".*? <span class="t2">.*?<span class="t4">(.*?)</span>',
        re.S)
    links = re.findall(reg, r.text)
    return links


# 多页处理，下载到文件
def get_content(link, salary):
    r1 = requests.get(link, headers, timeout=10)
    s = requests.session()
    s.keep_alive = False
    r1.encoding = 'gb18030'
    t1 = html.fromstring(r1.text)
    l = []
    try:
        job = t1.xpath('//div[@class="tHeader tHjob"]//h1/text()')[0]
        company = t1.xpath('//p[@class="cname"]/a/text()')[0]
        label = t1.xpath('//div[@class="t1"]/span/text()')
        education = t1.xpath('//div[@class="cn"]/p[2]/text()')[2]
        salary = salary
        area = t1.xpath('//div[@class="cn"]/p[2]/text()')[0]
        companytype = 'Null'
        workyear = t1.xpath('//div[@class="cn"]/p[2]/text()')[1]
        describe = re.findall(re.compile(r'<div class="bmsg job_msg inbox">(.*?)任职要求', re.S), r1.text)
        require = re.findall(re.compile(r'<div class="bmsg job_msg inbox">.*?任职要求(.*?)<div class="mt10">', re.S),
                             r1.text)
        try:
            file = codecs.open('51job.xls', 'a+', 'utf-8')
            item = str(company) + '\t' + str(job) + '\t' + str(education) + '\t' + str(label) + '\t' + str(
                salary) + '\t' + str(companytype) + '\t' + str(workyear) + '\t' + str(area) + '\t' + str(
                workyear) + str(describe) + '\t' + str(require) + '\n'
            file.write(item)
            file.close()
            return True
        except Exception as e:
            print(e)
            return None
        # output='{},{},{},{},{},{},{},{}\n'.format(company,job,education,label,salary,area,describe,require)
        # with open('51job.csv', 'a+', encoding='utf-8') as f:
        # f.write(output)
    except:
        print('None')
    print(l)
    return l


for i in range(1, 2):
    print('正在爬取第{}页信息'.format(i))
    try:
        # time.sleep(random.random()+random.randint(1,5))
        links = get_links(i)
        for link in links:
            url = link[0]
            salary = link[1]
            get_content(url, salary)
            # time.sleep(random.random()+random.randint(0,1))
    except:
        continue
        print('有点问题')