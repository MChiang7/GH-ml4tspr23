import numpy as np
import math

class DTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose

    def author(self):
        return 'mchiang30'

    def get_best_feature(self, data_x, data_y):
        index = -1
        best_corr = -1

        for i in range(data_x.shape[1]):
            if 0 >= np.std(data_x[:, i]):
                temp_corr = 0
            else:
                temp_corr = np.corrcoef(data_x[:, i], data_y)[0, 1]
            if best_corr < temp_corr:
                index = i
                best_corr = temp_corr

        return index

    def build_tree(self, data_x, data_y):
        if self.leaf_size >= data_x.shape[0]:
            return np.array([np.nan, np.mean(data_y), np.nan, np.nan])

        if len(set(data_y)) == 1:
            return np.array([np.nan, data_y[0], np.nan, np.nan])

        index = self.get_best_feature(data_x, data_y)

        masks = [np.median(data_x[:, index]) < data_x[:, index], np.median(data_x[:, index]) >= data_x[:, index]]

        for i in range(len(masks)):
            if i == 0:
                data_y_right = data_y[masks[i]]
                data_x_right = data_x[masks[i]]
            if i == 1:
                data_y_left = data_y[masks[i]]
                data_x_left = data_x[masks[i]]

        if (data_x_right.shape[0] == 0) or (len(set(masks[1])) == 1):
            return np.array([np.nan, np.mean(data_y), np.nan, np.nan])

        right_tree = self.build_tree(data_x_right, data_y_right)
        left_tree = self.build_tree(data_x_left, data_y_left)

        if 1 != left_tree.ndim:
            root = np.asarray([index, np.median(data_x[:, index]), 1, left_tree.shape[0] + 1])
        else:
            root = np.asarray([index, np.median(data_x[:, index]), 1, 2])

        return np.vstack((root, left_tree, right_tree))


    def add_evidence(self, data_x, data_y):
        self.tree = self.build_tree(data_x, data_y)

    def query(self, samples):
        res = []
        for temp in samples:
            cursor = 0
            while ~np.isnan(self.tree[cursor][0]):
                if self.tree[cursor][1] < temp[int(self.tree[cursor][0])]:
                    cursor += int(self.tree[cursor][3])
                else:
                    cursor += int(self.tree[cursor][2])
            res.append(self.tree[cursor][1])
        return res

if __name__=='__main__':
    print("the secret clue is 'zzyzx'")