################################################
#A data structure for computing time serias, 
#  eg. convergence.
################################################
import collections
import numpy as np
import copy

class data_stack():
    def __init__(self,max_len):
        self.max_len = max_len
        self.data = collections.deque()
    def len(self):
        return len(self.data)
    def add_data(self,d):        
        if(len(self.data) > self.max_len):
            self.data.popleft()        
        self.data.append(copy.deepcopy(d))        
    def mean(self):
        s = 0
        if self.len() > 0:
            s = self.data[0] * 0
        else:
            return 0
        for v in self.data:
            s += v          
        return s / self.len()
    def flush(self):
        print(self.data)
class convergence():
    '''
    return line data for showing a convergence trend with iteration times
    @max_len is used to compute a mean value
    '''
    def __init__(self, max_len):
        self.diffs = data_stack(max_len)
        self.data  = data_stack(2)
        self.listx = []
        self.listy = []
    def add_data(self, x, y, total_max):
        '''
        total_max is the max sum of input data, eg. for np.ones([3,3]), the sum_total = 9.
        '''                      
        self.data.add_data(y)
        congv = self.compute_convergence(total_max)
        self.diffs.add_data(congv)
        self.listy.append(self.diffs.mean())
        self.listx.append(x)  
        
    def get_data(self):
        return self.listx, self.listy
    def compute_convergence(self, total_max):        
        if self.data.len() == 0:
            return 0
        if self.data.len() < 2:
            return np.sum(self.data.data[0]) / total_max
        diff = np.sum(abs(self.data.data[1] - self.data.data[0])) / total_max
        
        return diff

if __name__ == "__main__":
    d = data_stack(3)
    for i in range(10):
        d.add_data(i)
        
        d.flush()
        print(d.mean())
        