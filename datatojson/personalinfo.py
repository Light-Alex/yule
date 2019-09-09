import time
import random
import requests
from lxml import etree
import pandas as pd
from fake_useragent import UserAgent

df_relations = pd.read_csv('ylq_all_star_relations.csv', encoding='utf-8')
print(df_relations.info())
star_urls = list(set(df_relations.subject_url.tolist() + df_relations.object_url.tolist()))
print(len(star_urls))
ylq_star_infos = pd.DataFrame(columns = ['num', 'name', 'relation_num', 'url', 'infos', 'image'])
for num, url in enumerate(star_urls):
    ua = UserAgent()
    headers ={"User-Agent": ua.random, 'Host': 'www.ylq.com'}
    r = requests.get(url=url, headers=headers, timeout=10)
    r.encoding = r.apparent_encoding
    dom = etree.HTML(r.text)
    name = dom.xpath('//div/div/div/h1/text()')[0]
    relations = dom.xpath('//div[@class="hd starRelation"]/ul/li/a/span/em/text()')
    infos = dom.xpath('//div[@class="sLeft"]/ul/li/text()') # infos = ' / '.join(infos)
    # image1 = dom.xpath('///div[@class="sRight"]/a/img/@src')
    image = dom.xpath('///div[@class="sRight"]/a/img/@src')[0]
    data = {'num': int(num+1), 'name': name, 'relation_num': len(relations),
                'url': url, 'infos': infos, 'image': image}
    ylq_star_infos = ylq_star_infos.append(data, ignore_index=True)
    # print(num, name, url, infos, relations, image)
    print(num, end=' ')
ylq_star_infos.to_csv('ylq_star_infos.csv', index=False, encoding='utf-8')
print('Finish!')