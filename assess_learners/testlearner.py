""""""  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
Test a learner.  (c) 2015 Tucker Balch  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
"""  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import math  		  	   		  		 			  		 			     			  	 
import sys  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import numpy as np  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import LinRegLearner as lrl
import DTLearner as dtl
import RTLearner as rtl
import BagLearner as bl
import InsaneLearner as il
import matplotlib.pyplot as plt
import time

def plot_helper(fig, runs, res_in, res_out, label1='', label2='', title = '', xlabel = '', ylabel = '', multiple=False, t3 = None, t4 = None, label3='', label4=''):
    if multiple:
        plt.plot(range(1, runs + 1), res_in, label=label1)
        plt.plot(range(1, runs + 1), res_out, label=label2)
        plt.plot(range(1, runs + 1), t3, label=label3)
        plt.plot(range(1, runs + 1), t4, label=label4)
    else:
        plt.plot(range(1, runs + 1), res_in, label=label1)
        plt.plot(range(1, runs + 1), res_out, label=label2)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    plt.savefig('./images/figure{}.png'.format(fig))
    plt.clf()
  		  	   		  		 			  		 			     			  	 
def experiment(train_x, train_y, test_x, test_y, expfig):
    runs = 100
    res_in = []
    res_out = []
    res_in_dt = []
    res_out_dt = []
    res_in_rt = []
    res_out_rt = []
    if expfig == 11:
        for i in range(1, runs + 1):
            learner = dtl.DTLearner(leaf_size=i, verbose=False)
            learner.add_evidence(train_x, train_y)
            pred_y_in = learner.query(train_x)
            rmse_in = math.sqrt(((train_y - pred_y_in) ** 2).sum() / train_y.shape[0])
            res_in.append(rmse_in)
            pred_y_out = learner.query(test_x)
            rmse_out = math.sqrt(((test_y - pred_y_out) ** 2).sum() / test_y.shape[0])
            res_out.append(rmse_out)
        plot_helper(1, runs, res_in, res_out, 'In Sample RMSE', 'Out Sample RMSE', 'Overfitting and Leaf Size - DTLearner on Istanbul Data Set', 'Leaf Size',
                    'Root Mean Squared Error')
    elif expfig == 12:
        for i in range(1, runs + 1):
            learner = bl.BagLearner(learner=dtl.DTLearner, kwargs={'leaf_size':i}, bags=20, boost=False, verbose=False)
            learner.add_evidence(train_x, train_y)
            pred_y_in = learner.query(train_x)
            rmse_in = math.sqrt(((train_y - pred_y_in) ** 2).sum() / train_y.shape[0])
            res_in.append(rmse_in)
            pred_y_out = learner.query(test_x)
            rmse_out = math.sqrt(((test_y - pred_y_out) ** 2).sum() / test_y.shape[0])
            res_out.append(rmse_out)
        plot_helper(2, runs, res_in, res_out, 'In Sample RMSE', 'Out Sample RMSE', 'Overfitting and Leaf Size - BagLearner with DTLearner on Istanbul Data Set with 20 Bags', 'Leaf Size',
                    'Root Mean Squared Error')
    elif expfig == 31:
        for i in range(1, runs + 1):
            learner = dtl.DTLearner(leaf_size=i, verbose=False)
            learner.add_evidence(train_x, train_y)
            pred_y_in = learner.query(train_x)
            mae_in_dt = np.mean(np.abs(train_y - pred_y_in))
            res_in_dt.append(mae_in_dt)
            pred_y_out = learner.query(test_x)
            mae_out_dt = np.mean(np.abs(test_y - pred_y_out))
            res_out_dt.append(mae_out_dt)

            learner = rtl.RTLearner(leaf_size=i, verbose=False)
            learner.add_evidence(train_x, train_y)
            pred_y_in = learner.query(train_x)
            mae_in_rt = np.mean(np.abs(train_y - pred_y_in))
            res_in_rt.append(mae_in_rt)
            pred_y_out = learner.query(test_x)
            mae_out_rt = np.mean(np.abs(test_y - pred_y_out))
            res_out_rt.append(mae_out_rt)
        plot_helper(3, runs, res_in_dt, res_in_rt, 'MAE In Sample DTLearner', 'MAE In Sample RTLearner', 'DT vs RT Learner - MAE', 'Leaf Size',
                    'Mean Absolute Error', True, res_out_dt, res_out_rt, 'MAE Out Sample DTLearner', 'MAE Out Sample RTLearner')
    elif expfig == 32:
        for i in range(1, runs + 1):
            learner = dtl.DTLearner(leaf_size=i, verbose=False)
            learner.add_evidence(train_x, train_y)
            pred_y_in = learner.query(train_x)
            r2_in_dt = np.corrcoef(pred_y_in, y=train_y)[0, 1] ** 2
            res_in_dt.append(r2_in_dt)
            pred_y_out = learner.query(test_x)
            r2_out_dt = np.corrcoef(pred_y_out, y=test_y)[0, 1] ** 2
            res_out_dt.append(r2_out_dt)

            learner = rtl.RTLearner(leaf_size=i, verbose=False)
            learner.add_evidence(train_x, train_y)
            pred_y_in = learner.query(train_x)
            r2_in_rt = np.corrcoef(pred_y_in, y=train_y)[0, 1] ** 2
            res_in_rt.append(r2_in_rt)
            pred_y_out = learner.query(test_x)
            r2_out_rt = np.corrcoef(pred_y_out, y=test_y)[0, 1] ** 2
            res_out_rt.append(r2_out_rt)
        plot_helper(4, runs, res_in_dt, res_in_rt, 'R-Squared In Sample DTLearner', 'R-Squared In Sample RTLearner',
                    'DT vs RT Learner - R-Squared', 'Leaf Size',
                    'R-Squared', True, res_out_dt, res_out_rt, 'R-Squared Out Sample DTLearner',
                    'R-Squared Out Sample RTLearner')
if __name__ == "__main__":
    if len(sys.argv) != 2:  		  	   		  		 			  		 			     			  	 
        #print("Usage: python testlearner.py <filename>")
        sys.exit(1)  		  	   		  		 			  		 			     			  	 
    inf = open(sys.argv[1])  		  	   		  		 			  		 			     			  	 
    #data = np.array(
    #    [list(map(float, s.strip().split(","))) for s in inf.readlines()]
    #)
    data = np.array(
        [list(map(str, s.strip().split(","))) for s in inf.readlines()]
    )
    if sys.argv[1] == 'Data/Istanbul.csv':
        data = data[1:, 1:]
    data = data.astype('float')
    np.random.shuffle(data)
    # compute how much of the data is training and testing  		  	   		  		 			  		 			     			  	 
    train_rows = int(0.6 * data.shape[0])  		  	   		  		 			  		 			     			  	 
    test_rows = data.shape[0] - train_rows  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # separate out training and testing data  		  	   		  		 			  		 			     			  	 
    train_x = data[:train_rows, 0:-1]  		  	   		  		 			  		 			     			  	 
    train_y = data[:train_rows, -1]  		  	   		  		 			  		 			     			  	 
    test_x = data[train_rows:, 0:-1]  		  	   		  		 			  		 			     			  	 
    test_y = data[train_rows:, -1]  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    #print(f"{test_x.shape}")
    #print(f"{test_y.shape}")
  		  	   		  		 			  		 			     			  	 
    # create a learner and train it  		  	   		  		 			  		 			     			  	 
    #learner = lrl.LinRegLearner(verbose=True)  # create a LinRegLearner
    #learner.add_evidence(train_x, train_y)  # train it
    #print(learner.author())

    # evaluate in sample  		  	   		  		 			  		 			     			  	 
    #pred_y = learner.query(train_x)  # get the predictions
    #rmse = math.sqrt(((train_y - pred_y) ** 2).sum() / train_y.shape[0])
    #print()
    #print("In sample results")
    #print(f"RMSE: {rmse}")
    #c = np.corrcoef(pred_y, y=train_y)
    #print(f"corr: {c[0,1]}")
  		  	   		  		 			  		 			     			  	 
    # evaluate out of sample  		  	   		  		 			  		 			     			  	 
    #pred_y = learner.query(test_x)  # get the predictions
    #rmse = math.sqrt(((test_y - pred_y) ** 2).sum() / test_y.shape[0])
    #print()
    #print("Out of sample results")
    #print(f"RMSE: {rmse}")
    #c = np.corrcoef(pred_y, y=test_y)
    #print(f"corr: {c[0,1]}")

    experiment(train_x, train_y, test_x, test_y, 11)
    experiment(train_x, train_y, test_x, test_y, 21)
    experiment(train_x, train_y, test_x, test_y, 31)
    experiment(train_x, train_y, test_x, test_y, 32)