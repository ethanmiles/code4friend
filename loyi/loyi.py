import h5py
import numpy as np
import collections
import matplotlib.pyplot as plt
import pandas as pd
import re
import seaborn as sb

# file path config
path = 'newratinglist20.mat'

# numpy global config
np.set_printoptions(precision=0, suppress=True)

# seaborn global config
sb.set()
sb.set_style('darkgrid')


class Analysis:
    def __init__(self, path):
        f = h5py.File(path, "r")
        name = re.findall(r"'(.*)'", str(f.keys()))[0]
        mat_t = f[name]
        mat = np.transpose(mat_t)
        mat = mat.astype(np.int32)  # float2int
        mat[:, 2] = mat[:, 2] / (24*30)   # hours2year
        self.mat = mat

    # self.mat
    def get_frequency_of_A(self, a):
        return self.mat[:, a]

    # self.mat
    def get_frequency_of_colC_where_colA_is_B(self, a, b, c):
        return self.mat[self.mat[:, a] == b][:, c]

     # self.mat
    def get_max_of_colA(self, a):
        max = self.mat[0, a]
        for row in self.mat:
            if row[a] > max:
                max = row[a]
        return max

    def matplotlib_draw_hist(self, d):
        plt.hist(d, bins=1000, normed=0, facecolor="blue",
                 edgecolor="black", alpha=0.7)
        plt.show()

    def seaborn_draw_kde(self, d):
        sb.distplot(d, kde_kws={"label": "KDE"}, color="y")
        plt.show()

    def print_quantile(self, d):
        print("quantile :\n", d.describe())

    def collect_colA_where_colB_eq_C(self, a, b, c):
        l = []
        for row in self.mat:
            if row[b] == c:
                l.append(row[a])
        return l


"""
剩余需求：

3.用第二列数据 对30个电影画时间序列图 曲线图 就电影一那种 找到三个最像的就行
4.对30个电影进行两两的相关系数分析 就是按照他的时间序列 000100200003这种的
对上面三个最像的图像求相关有个举例
比如corr（电影1，电影2）
corr（电影1，电影3）这种
然后这30个电影 想要一个30x30的矩阵
"""


if __name__ == "__main__":
    als = Analysis('newratinglist20.mat')

    known_film = {}  # known_film = {电影：评价数}

    for row in als.mat:
        if row[1] not in known_film:
            known_film[row[1]] = 1
        else:
            known_film[row[1]] += 1

    # 需求 求出评价数2000以上的电影有多少吗
    # morethan2000 = 0
    # for i in known_film:
    #     if known_film[i] > 2000:
    #         morethan2000 += 1
    # print("评价数多于2000的电影有：", morethan2000)

    # 需求 评价低于2000的数据行全扔掉
    del_keys = []
    for i in known_film:
        if known_film[i] < 2000:
            del_keys.append(i)
    for d in del_keys:
        known_film.pop(d)

    # 需求 对3000个电影的评价数的画分布图  （每个电影的评价数先加和）横轴是评价数  纵轴是频率
    # commentNums = pd.Series(list(known_film.values()))
    # sb.distplot(commentNums, kde_kws={"label": "KDE"}, color="y")
    # plt.show()

    # 需求 取四分位数 就是那些评价多的
    # als.print_quantile(commentNums)

    # 对每个电影的评价时间作kde图
    # for n in known_film:
    #     l = pd.Series(als.collect_colA_where_colB_eq_C(2, 1, n))
    #     sb.distplot(l, kde_kws={"label": "KDE"}, color="y")
    #     arg_name = str(n)
    #     plt.savefig(arg_name+".png")
    #     plt.clf()

    max_time = als.get_max_of_colA(2)
    size_time = max_time + 1  # 0 1 2 3 4 5 ... n  一共n+1个
    print("the maximum month is : ", max_time)
    max_film = als.get_max_of_colA(1)
    print("the maximum film number is : ", max_film)

    t = [0 for t in range(0, size_time)]
    out = []
    for n in known_film:
        film = t.copy()
        for i in als.collect_colA_where_colB_eq_C(2, 1, n):
            film[i] += 1
        film.insert(0, n)
        out.append(film)

    for l in out:
        for i in l:
            print(str(i)+",", end="")
        print('\n')
