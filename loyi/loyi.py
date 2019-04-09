import h5py
import numpy as np
import collections
import matplotlib.pyplot as plt
import pandas as pd
import re
path = 'newratinglist20.mat'
np.set_printoptions(precision=0, suppress=True)


class Analysis:
    def __init__(self, path):
        f = h5py.File(path, "r")
        name = re.findall(r"'(.*)'", str(f.keys()))[0]
        mat_t = f[name]
        mat = np.transpose(mat_t)
        mat = mat.astype(np.int32)  # float2int
        mat[:, 2] = mat[:, 2] / (24*30)   # hours2day
        self.mat = mat

    def 打印A的频数(self, a):
        col = self.mat[:, a]
        plt.hist(col, bins=1000, normed=0, facecolor="blue",
                 edgecolor="black", alpha=0.7)
        plt.show()

    def 打印A列等于B时C列的频数(self, a, b, c):
        col = self.mat[self.mat[:, a] == b][:, c]
        plt.hist(col, bins=25, normed=0, facecolor="blue",
                 edgecolor="black", alpha=0.7)
        plt.show()

    def A列分位数(self, a):
        col = self.mat[:, a]
        a = round(np.mean(col), 2)
        b = np.median(col)
        c = pd.DataFrame(col).describe()
        print(c)

    def 打印A列等于B时C列的分位数(self, a, b, c):
        col = self.mat[self.mat[:, a] == b][:, c]
        a = round(np.mean(col), 2)
        b = np.median(col)
        c = pd.DataFrame(col).describe()
        print(c)


if __name__ == "__main__":
    als = Analysis('newratinglist20.mat')
    als.打印A列等于B时C列的频数(1, 1, 2)
