import numpy as np
import random

class RTLearner(object):

    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        random.seed(903216278)

    def author(self):
        return 'mchian30'

    def build_tree(self, data_x, data_y):
        if self.leaf_size >= data_x.shape[0]:
            return np.array([np.nan, np.mean(data_y), np.nan, np.nan])

        if len(set(data_y)) == 1:
            return np.array([np.nan, data_y[0], np.nan, np.nan])

        index = random.randrange(data_x.shape[1])
        temp1, temp2 = random.sample(range(data_x.shape[0]), 2)

        masks = [(data_x[temp1][index] + data_x[temp2][index]) / 2 < data_x[:, index], (data_x[temp1][index] + data_x[temp2][index]) / 2 >= data_x[:, index]]

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
            root = np.asarray([index, (data_x[temp1][index] + data_x[temp2][index]) / 2, 1, left_tree.shape[0] + 1])
        else:
            root = np.asarray([index, (data_x[temp1][index] + data_x[temp2][index]) / 2, 1, 2])

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

if __name__ == '__main__':
    print("the secret clue is 'zzyzx'")