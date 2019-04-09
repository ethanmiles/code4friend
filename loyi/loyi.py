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
        mat[:, 2] = mat[:, 2] / (24*30)   # hours2month
        self.mat = mat

    def get_frequency_of_A(self, a):
        return self.mat[:, a]

    def get_frequency_of_colC_where_colA_is_B(self, a, b, c):
        return self.mat[self.mat[:, a] == b][:, c]

    def paint_frequency_of_A_hist(self, a):
        col = self.get_frequency_of_A(a)
        plt.hist(col, bins=1000, normed=0, facecolor="blue",
                 edgecolor="black", alpha=0.7)
        plt.show()

    def paint_colC_when_colA_is_B_hist(self, a, b, c):
        col = self.get_frequency_of_colC_where_colA_is_B(a, b, c)
        plt.hist(col, bins=25, normed=0, facecolor="blue",
                 edgecolor="black", alpha=0.7)
        plt.show()

    def print_colA_Quantile(self, a):
        col = self.get_frequency_of_A(a)
        c = pd.DataFrame(col).describe()
        print(c)

    def print_colC_when_colA_is_B_Quantile(self, a, b, c):
        col = self.get_frequency_of_colC_where_colA_is_B(a, b, c)
        c = pd.DataFrame(col).describe()
        print(c)

    def sbpaint_colC_when_colA_is_B_kde(self, a, b, c):
        col = self.get_frequency_of_colC_where_colA_is_B(a, b, c)
        sb.distplot(col, kde_kws={"label": "KDE"}, color="y")
        plt.show()

    def sbpaint_frequency_of_A_kde(self, a):
        col = self.get_frequency_of_A(a)
        sb.distplot(col, kde_kws={"label": "KDE"}, color="y")
        plt.show()


if __name__ == "__main__":
    als = Analysis('newratinglist20.mat')
    als.sbpaint_frequency_of_A_kde(1)
