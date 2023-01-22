""""""  		  	   		  		 			  		 			     			  	 
"""Assess a betting strategy.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
  		  	   		  		 			  		 			     			  	 
Student Name: Michael Chiang (replace with your name)  		  	   		  		 			  		 			     			  	 
GT User ID: mchiang30 (replace with your User ID)  		  	   		  		 			  		 			     			  	 
GT ID: 903216278 (replace with your GT ID)  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import numpy as np  		  	   		  		 			  		 			     			  	 
import matplotlib.pyplot as plt
  		  	   		  		 			  		 			     			  	 
def author():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    :return: The GT username of the student  		  	   		  		 			  		 			     			  	 
    :rtype: str  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    return "mchiang30"  # replace tb34 with your Georgia Tech username.
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def gtid():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    :return: The GT ID of the student  		  	   		  		 			  		 			     			  	 
    :rtype: int  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    return 903216278  # replace with your GT ID number
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def get_spin_result(win_prob):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param win_prob: The probability of winning  		  	   		  		 			  		 			     			  	 
    :type win_prob: float  		  	   		  		 			  		 			     			  	 
    :return: The result of the spin.  		  	   		  		 			  		 			     			  	 
    :rtype: bool  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    result = False  		  	   		  		 			  		 			     			  	 
    if np.random.random() <= win_prob:  		  	   		  		 			  		 			     			  	 
        result = True  		  	   		  		 			  		 			     			  	 
    return result  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def test_code():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    Method to test your code  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    win_prob = 18/38  # set appropriately to the probability of a win
    np.random.seed(gtid())  # do this only once  		  	   		  		 			  		 			     			  	 
    # print(get_spin_result(win_prob))  # test the roulette spin
    # add your code here to implement the experiments
    for i in range(11, 16):
        if i > 13:
            exp_num = i + 10
        else:
            exp_num = i

        experiment(win_prob, exp_num)

def strategy(win_prob, realistic = False):
    res = np.empty(1001)
    num_bets = 0
    episode_winnings = 0

    while episode_winnings < 80:
        won = False
        bet_amount = 1

        while not won:
            if num_bets >= 1001:
                return res
            res[num_bets] = episode_winnings
            num_bets += 1
            won = get_spin_result(win_prob)

            if won:
                episode_winnings += bet_amount
                res[num_bets:] = episode_winnings
            else:
                episode_winnings -= bet_amount
                bet_amount *= 2

                if realistic:
                    if bet_amount - 256 > episode_winnings:
                        bet_amount = episode_winnings + 256
                    if 256 == -episode_winnings:
                        res[num_bets:] = episode_winnings
                        return res

    return res

def run_helper(runs, win_prob, realistic = False):
    if runs == 10:
        for i in range(runs):
            temp = strategy(win_prob)
            plt.plot(temp)
    elif runs == 1000:
        res = np.zeros((1000, 1001))
        for i in range(runs):
            temp = strategy(win_prob, realistic)
            res[i] = temp
        return res


def plot_helper(axis = [0, 300, -256, 100], title = '', xlabel = '# of Trials', ylabel = 'Winnings ($)', mm = False, metric = '', m_value = None, std = None):
    plt.axis(axis)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if mm:
        plt.plot(m_value, label = metric)
        plt.plot(m_value - std, label = '{} minus Std.'.format(metric))
        plt.plot(m_value + std, label = '{} plus Std.'.format(metric))
        plt.legend()

def mm_calc(res, metric):
    std = np.std(res, axis = 0)

    if metric == 'mean':
        m_value = np.mean(res, axis = 0)
    elif metric == 'median':
        m_value = np.median(res, axis = 0)

    return m_value, std

def experiment(win_prob, expfig):
    if expfig == 11:
        plot_helper(title = 'Fig. 1 - 10 episodes, unlimited bankroll')
        run_helper(10, win_prob)
        plt.savefig('./images/figure1.png')
        plt.clf()
    elif expfig == 12:
        x = mm_calc(run_helper(1000, win_prob), 'mean')
        plot_helper(title = 'Fig. 2 - mean of 1000 episodes, unlimited bankroll', mm = True, metric = 'mean',
                    m_value = x[0], std = x[1])
        plt.savefig('./images/figure2.png')
        plt.clf()
    elif expfig == 13:
        x = mm_calc(run_helper(1000, win_prob), 'median')
        plot_helper(title =' Fig. 3 - median of 1000 episodes, unlimited bankroll', mm = True, metric = 'median',
                    m_value = x[0], std = x[1])
        plt.savefig('./images/figure3.png')
        plt.clf()
    elif expfig == 24:
        x = mm_calc(run_helper(1000, win_prob, True), 'mean')
        plot_helper(title = ' Fig. 4 - mean of 1000 episodes, $256 bankroll', mm = True, metric = 'mean',
                    m_value = x[0], std = x[1])
        plt.savefig('./images/figure4.png')
        plt.clf()
    elif expfig == 25:
        x = mm_calc(run_helper(1000, win_prob, True), 'median')
        plot_helper(title = ' Fig. 5 - median of 1000 episodes, $256 bankroll', mm = True, metric = 'median',
                    m_value = x[0], std = x[1])
        plt.savefig('./images/figure5.png')
        plt.clf()

if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    test_code()  		  	   		  		 			  		 			     			  	 
