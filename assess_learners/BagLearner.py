import numpy as np

class BagLearner(object):
    def __init__(self, learner, kwargs={}, bags=20, boost=False, verbose=False):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.learners = []
        for i in range(self.bags):
            self.learners.append(self.learner(**kwargs))

    def author(self):
        return 'mchiang30'

    def add_evidence(self, data_x, data_y):
        index = np.random.choice(range(data_x.shape[0]), data_x.shape[0], replace=True)
        for temp in self.learners:
            temp.add_evidence(data_x[index], data_y[index])

    def query(self, samples):
        res = []
        for temp in self.learners:
            res.append(temp.query(samples))
        return sum(np.asarray(res)) / len(np.asarray(res))

if __name__=='__main__':
    print("the secret clue is 'zzyzx'")