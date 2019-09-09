import time
import random
import requests
from lxml import etree
import pandas as pd
from fake_useragent import UserAgent

ylq_all_star_ids = pd.DataFrame(columns=['num', 'name', 'star_id', 'star_url', 'image'])
total_pages = 153  # 9174 # 153 # 4475=74*60+36-1 # 75
for page in range(1, total_pages + 1):
    ua = UserAgent()  # 随机生成用户代理
    headers = {"User-Agent": ua.random}
    url = 'http://www.ylq.com/star/list-all-all-all-all-all-all-all-{}.html'
    r = requests.get(url=url.format(page), headers=headers)
    r.encoding = r.apparent_encoding
    dom = etree.HTML(r.text)

    # 'http://www.ylq.com/neidi/xingyufei/'
    star_urls = dom.xpath('//div[@class="fContent"]/ul/li/a/@href')
    star_ids = [star_url.split('/')[-2] for star_url in star_urls]
    star_names = dom.xpath('//div[@class="fContent"]/ul/li/a/h2/text()')
    star_images = dom.xpath('//div[@class="fContent"]/ul/li/a/img/@src')

    print(page, len(star_urls), len(star_ids), len(star_images), len(star_names))

    for i in range(len(star_ids)):
        ylq_all_star_ids = ylq_all_star_ids.append({'num': int((page - 1) * 60 + i + 1), 'name': star_names[i],
                                                    'star_id': star_ids[i], 'star_url': star_urls[i],
                                                    'image': star_images[i]}, ignore_index=True)
    # if page%5 == 0:
    #    time.sleep(random.randint(0,2))
print("爬虫结束！")

# # print(ylq_all_star_ids.head())
# # print(ylq_all_star_ids.tail())
# # zgr_url = 'http://www.ylq.com/gangtai/zhangguorong/' # 张国荣 主页
# # ua = UserAgent()
# # headers = {"User-Agent": ua.random,
# #           'Host': 'www.ylq.com'}
# # r = requests.get(url = zgr_url, headers = headers, timeout=3)
# # r.encoding = r.apparent_encoding
# # print('starRelation' in r.text)
# # dom = etree.HTML(r.text)
# # star_relations = dom.xpath('//div[@class="hd starRelation"]//text()')
# # print(star_relations)
# # filter_relation = [item for item in star_relations if '\r\n' not in item]
# # print(filter_relation)
star_urls = ylq_all_star_ids.star_url.tolist()
print(len(star_urls))
star_has_relations = []
# index = 0
for num, url in enumerate(star_urls):  # star_urls[index:]
    ua = UserAgent()
    headers = {"User-Agent": ua.random,
               'Host': 'www.ylq.com'}
    try:
        r = requests.get(url=url, headers=headers, timeout=5)
        r.encoding = r.apparent_encoding

        if 'starRelation' in r.text:
            star_has_relations.append(url)
            print(num, "Bingo!", end=' ')
        if num % 100 == 0:
            print(num, end=' ')
    except:
        print(num, star_has_relations)

#     if (num+index)%50==0:
#         time.sleep(random.randint(0,2))
a = len(star_has_relations)
# star_has_relations
ylq_all_star_ids['has_relations'] = ylq_all_star_ids.star_url.apply(lambda x: 'true' if x in star_has_relations else 'false')
b = ylq_all_star_ids.head()
# ylq_all_star_ids['has_relations'].value_counts()
ylq_all_star_ids.to_csv('ylq_all_star_ids.csv', index=False, encoding='utf-8')

# 爬取明星的关系数据
datas = []
ylq_all_star_relations = pd.DataFrame(columns = ['num', 'subject', 'relation', 'object',
                                                 'subject_url', 'object_url', 'obeject_image'])
for num, subject_url in enumerate(star_has_relations):
    ua = UserAgent()  #随机生成用户代理
    headers = {"User-Agent": ua.random,
              'Host': 'www.ylq.com'}
    try:
        r = requests.get(url = subject_url, headers = headers, timeout=5)
        r.encoding = r.apparent_encoding
        dom = etree.HTML(r.text)
        subject = dom.xpath('//div/div/div/h1/text()')[0]
        relations = dom.xpath('//div[@class="hd starRelation"]/ul/li/a/span/em/text()')
        objects = dom.xpath('//div[@class="hd starRelation"]/ul/li/a/p/text()')
        object_urls = dom.xpath('//div[@class="hd starRelation"]/ul/li/a/@href')
        object_images = dom.xpath('//div[@class="hd starRelation"]/ul/li/a/img/@src')
        for i in range(len(relations)):
            relation_data = {'num': int(num+1), 'subject': subject, 'relation': relations[i],
                             'object': objects[i], 'subject_url':subject_url,
                             'object_url': object_urls[i], 'obeject_image': object_images[i]}
            datas.append(relation_data)
            ylq_all_star_relations = ylq_all_star_relations.append(relation_data,
                                                                   ignore_index=True)
        print(num, subject, end=' ')
    except:
        print(num, datas)

# print(ylq_all_star_relations.info())
ylq_all_star_relations = pd.read_csv('ylq_all_star_relations.csv', encoding='utf-8')
objects = ylq_all_star_relations.object.tolist()
print(len(objects))
# ylq_all_star_relations.to_csv('ylq_all_star_relations.csv', index=False, encoding='utf-8')
ylq_all_star_ids = pd.read_csv('ylq_all_star_ids.csv', encoding='utf-8')

# 完善节点
all_star_nodes = ylq_all_star_ids.name.tolist()
print(len(all_star_nodes))
other_ids = []
for obj in objects:
    if obj not in all_star_nodes:
        other_ids.append(obj)
# print(other_ids)
# print(len(all_star_nodes + other_ids))
node_map = {}
for index, node in enumerate(all_star_nodes + other_ids):
    if node not in node_map:
        node_map[node] = index + 1
# print(len(node_map))
all_nodes = pd.DataFrame(columns=['name', 'id'])
all_nodes['name'] = list(node_map.keys())
all_nodes['id'] = list(node_map.values())
all_nodes.to_csv('ylq_all_star_nodes.csv', index=False, encoding='utf-8')
all_nodes = pd.read_csv('ylq_all_star_nodes.csv', encoding='utf-8')
ylq_all_star_relations['from_id'] = ylq_all_star_relations['subject'].map(node_map)
ylq_all_star_relations['to_id'] = ylq_all_star_relations['object'].map(node_map)
ylq_all_star_relations.to_csv('ylq_all_star_relations.csv', index=False, encoding='utf-8')