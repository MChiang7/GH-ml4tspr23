import BagLearner as bl
import LinRegLearner as lrl

class InsaneLearner(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.learners = []
        for i in range(20):
            self.learners.append(bl.BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=20, boost=False, verbose=False))


    def author(self):
        return 'mchiang30'

    def add_evidence(self, data_x, data_y):
        for temp in self.learners:
            temp.add_evidence(data_x, data_y)

    def query(self, samples):
        res = []
        for temp in self.learners:
            res.append(temp.query(samples))
            return sum(res) / len(res)

if __name__=='__main__':
    print("the secret clue is 'zzyzx'")