""""""  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		  	   		  		 			  		 			     			  	 
Note, this is NOT a correct DTLearner; Replace with your own implementation.  		  	   		  		 			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		  		 			  		 			     			  	 
All Rights Reserved  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Template code for CS 4646/7646  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		  		 			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		  		 			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		  		 			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 			  		 			     			  	 
or edited.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		  		 			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		  		 			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 			  		 			     			  	 
GT honor code violation.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
-----do not edit anything above this line---  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Student Name: Tucker Balch (replace with your name)  		  	   		  		 			  		 			     			  	 
GT User ID: tb34 (replace with your User ID)  		  	   		  		 			  		 			     			  	 
GT ID: 900897987 (replace with your GT ID)  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import warnings  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import numpy as np  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
class DTLearner(object):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    This is a decision tree learner object that is implemented incorrectly. You should replace this DTLearner with  		  	   		  		 			  		 			     			  	 
    your own correct DTLearner from Project 3.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param leaf_size: The maximum number of samples to be aggregated at a leaf, defaults to 1.  		  	   		  		 			  		 			     			  	 
    :type leaf_size: int  		  	   		  		 			  		 			     			  	 
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 			  		 			     			  	 
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.  		  	   		  		 			  		 			     			  	 
    :type verbose: bool  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    def __init__(self, leaf_size=1, verbose=False):  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
        Constructor method  		  	   		  		 			  		 			     			  	 
        """
        self.leaf_size = leaf_size
        self.verbose = verbose
  		  	   		  		 			  		 			     			  	 
    def author(self):  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
        :return: The GT username of the student  		  	   		  		 			  		 			     			  	 
        :rtype: str  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
        return "mchiang30"  # replace tb34 with your Georgia Tech username
  		  	   		  		 			  		 			     			  	 
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
        """  		  	   		  		 			  		 			     			  	 
        Add training data to learner  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
        :param data_x: A set of feature values used to train the learner  		  	   		  		 			  		 			     			  	 
        :type data_x: numpy.ndarray  		  	   		  		 			  		 			     			  	 
        :param data_y: The value we are attempting to predict given the X data  		  	   		  		 			  		 			     			  	 
        :type data_y: numpy.ndarray  		  	   		  		 			  		 			     			  	 
        """

        self.tree = self.build_tree(data_x, data_y)
  		  	   		  		 			  		 			     			  	 
    def query(self, samples):
        """  		  	   		  		 			  		 			     			  	 
        Estimate a set of test points given the model we built.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
        :param points: A numpy array with each row corresponding to a specific query.  		  	   		  		 			  		 			     			  	 
        :type points: numpy.ndarray  		  	   		  		 			  		 			     			  	 
        :return: The predicted result of the input data according to the trained model  		  	   		  		 			  		 			     			  	 
        :rtype: numpy.ndarray  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
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
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    print("the secret clue is 'zzyzx'")  		  	   		  		 			  		 			     			  	 
