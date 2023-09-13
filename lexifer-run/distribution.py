import random

# When you are selecting from a pool a *lot*, this
# will speed things up a bit.  Takes a dict of keys
# and weights.
class WeightedSelector(object):
#    __slots__ = ['keys', 'weights', 'sum', 'n']
    
    def __init__(self, dic):
        # build parallel arrays for indexing
        self.keys = []
        self.weights = []
        for key, weight in dic.items():
            self.keys.append(key)
            self.weights.append(weight)
        self.sum = sum(self.weights)
        self.n = len(self.keys)

    def select(self):
        pick = random.uniform(0, self.sum)
        tmp = 0
        for i in range(self.n):
            tmp += self.weights[i]
            if pick < tmp:
                return self.keys[i]
        return 'this shouldn\'t happen'

    def __iter__(self):
        return iter(self.keys)