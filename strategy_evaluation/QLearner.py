""""""
"""  		  	   		  		 			  		 			     			  	 
Template for implementing QLearner  (c) 2015 Tucker Balch  		  	   		  		 			  		 			     			  	 

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

import random as rand

import numpy as np


class QLearner(object):
    """  		  	   		  		 			  		 			     			  	 
    This is a Q learner object.  		  	   		  		 			  		 			     			  	 

    :param num_states: The number of states to consider.  		  	   		  		 			  		 			     			  	 
    :type num_states: int  		  	   		  		 			  		 			     			  	 
    :param num_actions: The number of actions available..  		  	   		  		 			  		 			     			  	 
    :type num_actions: int  		  	   		  		 			  		 			     			  	 
    :param alpha: The learning rate used in the update rule. Should range between 0.0 and 1.0 with 0.2 as a typical value.  		  	   		  		 			  		 			     			  	 
    :type alpha: float  		  	   		  		 			  		 			     			  	 
    :param gamma: The discount rate used in the update rule. Should range between 0.0 and 1.0 with 0.9 as a typical value.  		  	   		  		 			  		 			     			  	 
    :type gamma: float  		  	   		  		 			  		 			     			  	 
    :param rar: Random action rate: the probability of selecting a random action at each step. Should range between 0.0 (no random actions) to 1.0 (always random action) with 0.5 as a typical value.  		  	   		  		 			  		 			     			  	 
    :type rar: float  		  	   		  		 			  		 			     			  	 
    :param radr: Random action decay rate, after each update, rar = rar * radr. Ranges between 0.0 (immediate decay to 0) and 1.0 (no decay). Typically 0.99.  		  	   		  		 			  		 			     			  	 
    :type radr: float  		  	   		  		 			  		 			     			  	 
    :param dyna: The number of dyna updates for each regular update. When Dyna is used, 200 is a typical value.  		  	   		  		 			  		 			     			  	 
    :type dyna: int  		  	   		  		 			  		 			     			  	 
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 			  		 			     			  	 
    :type verbose: bool  		  	   		  		 			  		 			     			  	 
    """

    def __init__(
            self,
            num_states=100,
            num_actions=4,
            alpha=0.2,
            gamma=0.9,
            rar=0.5,
            radr=0.99,
            dyna=0,
            verbose=False,
    ):
        """  		  	   		  		 			  		 			     			  	 
        Constructor method  		  	   		  		 			  		 			     			  	 
        """
        self.verbose = verbose
        self.num_actions = num_actions
        self.s = 0
        self.a = 0

        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.q_table = np.zeros((num_states, num_actions))

        if dyna > 0:
            self.previous = {}
            self.t_table = np.zeros((num_states, num_actions, num_states))
            self.r_table = np.zeros((num_states, num_actions))

    def author(self):
        return 'mchiang30'

    def hallucinate(self):
        temp_state = rand.choice(list(self.previous.keys()))
        temp_action = rand.choice(self.previous[temp_state])

        self.update(temp_state, temp_action, np.argmax(self.t_table[temp_state, temp_action]),
                    self.r_table[temp_state, temp_action], 0)

    def update(self, s, a, s_prime, r, table):
        if table == 0:
            self.q_table[s, a] = (
                        -self.alpha * (np.max(self.q_table[s_prime]) * -self.gamma - r) - self.q_table[s, a] * (
                            self.alpha - 1))
        elif table == 1:
            self.r_table[s, a] = self.alpha * r - (self.alpha - 1) * self.r_table[s, a]

    def querysetstate(self, s):
        """
        Update the state without updating the Q-table

        :param s: The new state
        :type s: int
        :return: The selected action
        :rtype: int
        """

        if self.rar <= rand.random():
            action = np.argmax(self.q_table[s])
        else:
            action = rand.randint(0, (1 - self.num_actions) * -1)

        if self.verbose:
            print(f"s = {s}, a = {action}")

        self.s = s

        return action

    def query(self, s_prime, r):
        """  		  	   		  		 			  		 			     			  	 
        Update the Q table and return an action  		  	   		  		 			  		 			     			  	 

        :param s_prime: The new state  		  	   		  		 			  		 			     			  	 
        :type s_prime: int  		  	   		  		 			  		 			     			  	 
        :param r: The immediate reward  		  	   		  		 			  		 			     			  	 
        :type r: float  		  	   		  		 			  		 			     			  	 
        :return: The selected action  		  	   		  		 			  		 			     			  	 
        :rtype: int  		  	   		  		 			  		 			     			  	 
        """
        self.update(self.s, self.a, s_prime, r, 0)

        if self.dyna > 0:
            self.previous[self.s] = list(set([self.a]) | set(self.previous.get(self.s, [])))

            self.t_table[self.s, self.a, s_prime] += 1
            self.update(self.s, self.a, s_prime, r, 1)

            for i in range(self.dyna):
                self.hallucinate()

        self.rar *= self.radr
        action = self.querysetstate(s_prime)
        self.a = action

        return action


if __name__ == "__main__":
    # print("Remember Q from Star Trek? Well, this isn't him")
    pass
