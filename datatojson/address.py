import os
import json
import uuid
import pandas as pd
import numpy as np

ylq_star_infos = pd.read_csv('ylq_star_infos.csv', encoding='utf-8')
ylq_star_infos['address'] = ylq_star_infos.infos.apply(lambda info: eval(info)[0]) # '新西兰,北岛,惠灵顿'
# b = ylq_star_infos.head()
# print(ylq_star_infos['address'].value_counts())
address_list = list(set(ylq_star_infos['address'].tolist()))
# print(len(address_list))
area_list = ['美国', '以色列', '澳大利亚', '英国', '加拿大', '文莱', '新加坡', '西班牙', '越南', '罗马尼亚', '马来西亚', '菲律宾', '新西兰',
           '韩国', '日本', '北京', '天津', '上海', '重庆', '河北', '山西', '辽宁', '吉林', '江苏', '浙江', '安徽', '福建', '江西', '山东',
           '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '台湾', '广西', '西藏', '宁夏', '新疆',
           '香港', '澳门', '内蒙古', '黑龙江']

area_map = {'纽约': '美国', '美籍': '美国', '俄克拉荷马': '美国', '加州': '美国', '伦敦': '英国',
          '东京': '日本', '京畿道高阳市': '韩国', '大邱广域市': '韩国', '台北':'台湾', '遵义': '贵州',
          '南京': '江苏', '青岛': '山东', '深圳': '广东', '杭州': '浙江', '成都': '四川', '衡水': '河北',
          '大连': '山东', '齐齐哈尔': '黑龙江', '淮安': '江苏', '温州': '浙江', '唐山': '河北', '福州': '福建',
          '营口': '辽东', '武汉': '湖北', '广州': '广东'}

def get_city(address):
    for area in area_list:
        if area in address:
            return area
    for area in area_map.keys():
        if area in address:
            return area_map[area]
    if '中国' in address: return '中国'
    else: return '不详'
ylq_star_infos['area'] = ylq_star_infos['address'].apply(get_city)
# a = ylq_star_infos.head()
area_counts = ylq_star_infos['area'].value_counts()
area_index = list(area_counts.index)
area_num = list(area_counts.values)
# print(len(area_index), len(area_num))
# print(area_index)

dic_categories = {'Star': '明星', 'Area': '地区'}

# 构造地区结点
nodes = []
area2id = {}
for i in range(len(area_index)):
    node = dict()
    node['label'] = area_index[i] # 地区名
    node['value'] = area_num[i] # 出现次数
    node['id'] = int(uuid.uuid1()) # uuid / id
    node['categories'] = ['Area'] # 节点类目
    node['info'] = ''
    area2id[area_index[i]] = node['id'] # 给每个地区名指定 uuid / id
    nodes.append(node)
# print(area2id)
# nodes
area = [i for i in nodes if i['categories'] == ['Area']]
print('地区数量:', len(area))
# a = 1
df_relations = pd.read_csv('ylq_all_star_relations.csv', encoding='utf-8')
df_relations_small = df_relations[['subject', 'relation', 'object']]
# print(ylq_star_infos.shape)
# print(df_relations_small.shape)

# 构造明星结点
# .loc 基于标签(label)，包括行标签(index)和列标签(columns)
# 即行名称和列名称
# ylq_star_infos.iloc[2]['name'], ylq_star_infos.loc[2, 'name']
star2id = {}
for idx in range(ylq_star_infos.shape[0]): # 1282
    node = dict()
    star_name = ylq_star_infos.loc[idx, 'name'] # ylq_star_infos.iloc[idx]['name']
    node['label'] = star_name
    node['value'] = ylq_star_infos.loc[idx, 'relation_num']# counter[star_name] # 貌似后者是前者一倍
    node['id'] = idx+1
    node['image'] = "static/images/star/{}.jpg".format(star_name)
    node['categories'] = ['Star']
    infos = eval(ylq_star_infos.loc[idx, 'infos']) # ylq_star_infos.iloc[idx]['infos']
    infos = [info for info in infos if info not in ['0000-00-00', '不详']]
    node['info'] = ' / '.join(infos)
    star2id[star_name] = idx + 1
    nodes.append(node)
star = [i for i in nodes if i['categories'] == ['Star']]
print('明星数量:', len(star))
# print('明星结点数:' + len(nodes)) # 1332
# nodes

# 构造明星与明星之间的边关系
edges = []
for idx in range(df_relations_small.shape[0]):
    edge = dict()
    edge['id'] = int(uuid.uuid1())
    edge['label'] = df_relations_small.loc[idx, 'relation'] # df_relations_small.iloc[idx]['relation']
    subject_star = df_relations_small.loc[idx, 'subject']
    object_star = df_relations_small.loc[idx, 'object'] # KeyError:'李蒽熙 ' 可手动去csv里去掉空格变成 '李蒽熙'
    edge['from'] = star2id[subject_star] # ylq_star_infos[ylq_star_infos.name == subject_star].iloc[0]['num']
    edge['to'] = star2id[object_star] # ylq_star_infos[ylq_star_infos.name == object_star].iloc[0]['num']
    # print(edge)
    edges.append(edge)
starrel = [i for i in edges if i['label'] in list(df_relations_small['relation'])]
print('明明关系数量:', len(starrel)) # 3433
# edges

# 构造明星与地区之间的边关系
for idx in range(ylq_star_infos.shape[0]):
    edge = dict()
    edge['id'] = int(uuid.uuid1())
    edge['label'] = '出生于'
    edge['from'] = idx+1
    area = ylq_star_infos.loc[idx, 'area']
    edge['to'] = area2id[area]
    edges.append(edge)
addrrel = [i for i in edges if i['label'] == '出生于']
print('明地关系数量:', len(addrrel)) # 3433
# print(len(edges))
# edges

# 生成 JSON 文件
# TypeError: Object of type 'int32' is not JSON serializable
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)
dic = dict()
dic['categories'] = dic_categories
dic['data'] = dict()
dic['data']['nodes'] = nodes
dic['data']['edges'] = edges
# print(dic)

dic_json = json.dumps(dic, cls=MyEncoder, indent=2, ensure_ascii=False)
#dic_json = json.dumps(dic, ensure_ascii=False)
# print(dic_json)
