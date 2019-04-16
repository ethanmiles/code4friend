"""
Request URL:
https://fe-api.zhaopin.com/c/i/city-page/user-city?
ipCity=%E5%8C%97%E4%BA%AC
ipProvince=%E5%8C%97%E4%BA%AC
userDesiredCity=&_v=0.22033319
x-zp-page-request-id=bb13a1dabeee41b3ae09fd4421ef19db-1555425061894-612574
"""


import requests
import json
import csv
from urllib.parse import urlencode
import time
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import numpy as np
import seaborn as sb


def GetData(url, writer):  # 解析并将数据保存为CSV文件
    # 下面这行 模拟浏览器打开这个网页

    response = requests.get(url)
    data = response.content
    #  转换成人能看得懂的格式
    jsondata = json.loads(data)
    #  从里面拿出 所需的信息
    jobs = jsondata['data']['results']
    # 对每个岗位摘出来，分别处理

    年限规则 = {'不限': 0, '无经验': 0, '1年以下': 1, '1-3年': 2,
            '3-5年': 3, '5-10年': 4, '10年以上': 5}
    学历规则 = {'不限': 0, '中技': 1, '中专': 2, '高中': 3,
            '大专': 4, '本科': 5, '硕士': 6, '博士': 7}

    for job in jobs:
        if '薪资面议' in job['salary']:
            continue
        salary = int(float(job['salary'].split("K")[0]))
        # city = job['city']['display']  # 城市
        # if '-' in city:
        #    city = city.split('-')[0]
        eduLevel = 学历规则[job['eduLevel']['name']]  # 学历要求
        workingExp = 年限规则[job['workingExp']['name']]  # 工作经验
        writer.writerow([salary,
                         eduLevel, workingExp])


def Crawler():
    # 参数配置
    param = {'start': 0,
             'pageSize': 60,
             'cityId': 489,
             'workExperience': -1,
             'education': -1,
             'companyType': -1,
             'employmentType': -1,
             'jobWelfareTag': -1,
             'kw': '运营',  # 搜索关键词，可以根据你需要爬取的岗位信息进行更换
             'kt': 3,
             'lastUrlQuery': {"p": 1, "pageSize": "60", "jl": "681", "kw": "python", "kt": "3"}
             }
    with open("test.csv", "w", encoding="utf-8", newline='') as out_f:
        writer = csv.writer(out_f)
        writer.writerow(['salary', 'eduLevel', 'workingExp'])
        for p in range(1, 5):
            # 更新请求的页面，
            param['start'] = (p-1)*60
            param['lastUrlQuery']['p'] = p
            # 拼接成一个网址
            url = 'https://fe-api.zhaopin.com/c/i/sou?' + urlencode(param)
            # 保存该页面的信息
            GetData(url, writer)
            # 休息一下
            time.sleep(3)  # 间隔休眠3秒，防止IP被封
            # 继续爬取下一页


class KNN生成器:
    def __init__(self, data):
        self.data = data

    def run(self):
        x = np.array(self.data.drop('salary', axis=1))
        y = np.array(self.data['salary'])

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.2, random_state=0)
        clf = DecisionTreeClassifier(random_state=14, max_depth=5)
        clf.fit(x_train, y_train.astype('int'))
        res = clf.predict(x_test)
        cm = confusion_matrix(y_test, res)
        print(cm)
        sb.heatmap(cm, annot=True)


if __name__ == "__main__":
    Crawler()
    data = pd.read_csv('test.csv', sep=',')
    KNN生成器(data).run()
