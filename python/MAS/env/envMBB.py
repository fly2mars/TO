import numpy as np
import copy
   
from env.env import *

vals = [255, 0]
ACT_NO = [0,1,2,3,4,5] #N types of operations

class ENV_MBB2D(Environment):
    def __init__(self):
        super(Environment).__init__()
                
        ## properties list
        self.grid_prop_stress= np.zeros(0)
        self.grid_prop_compliance= np.zeros(0)
        self.grid_prop_dc= np.zeros(0)
        self.step = 0
        return
    
    def set_dim(self, dim):
        '''
        init a grid with dimention of (row, col, height)
        '''
        self.dim = dim
        ### init constraints
        # F, Fix, Support        
        ### end  constraints
        if len(dim) != 2:
            raise Exception("Wrong dimension!")
        
        self.grid = np.random.choice(vals, dim[0]*dim[1], p=[0.2, 0.8]).reshape(dim[0], dim[1])
        self.grid_prop_stress = np.zeros([dim[0], dim[1]])
           
            ##init properties...
        return
    
    def bind_agent(self, agent):    
        self.agents = []

        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                agt = copy.copy(agent)  # copy an agent
                agt.bind_pos([i,j])
                self.agents.append(agt)
        return self.agents
    
    def update_state(self):
         #use tools such as FEA to update properties list
        #self.grid_prop_stress = FEA()
        return
    
    def dump(self):
        print(self.grid)

if __name__ == '__main__':
    env = ENV_MBB2D()
    env.set_dim([3,3])
    env.dump()