import numpy as np
from lib.suAgent import *
from lib.suKnowlegeEngine import *
vals = [ON, OFF]

class Environment:
    def __init__(self,ke):
        self.grid = np.zeros(0)
        self.ke = ke
        
        ## properties list
        self.grid_prop_stress= np.zeros(0)
        self.grid_prop_compliance= np.zeros(0)
        self.grid_prop_dc= np.zeros(0)
        self.step = 0
        return
    def set_dim(self, row,col,height=0):
        '''
        init a grid with dimention of (row, col, height)
        '''
        self.H = row
        self.W = col                
        ### init constraints
        # F, Fix, Support
        
        ### end  constraints
        if height==0:  # todo: extend to 3D
            self.grid = np.random.choice(vals, row*col, p=[0.2, 0.8]).reshape(row, col)
            self.grid_prop_stress = np.zeros([row,col])
            ##init properties...
        return
    
    def bind_agent(self):    
        H = self.H
        W = self.W
        agents = []

        for i in range(H):
            for j in range(W):
                agt = Agent(self.ke, self)
                agt.bind_pos([i,j])
                agents.append(agt)
        return agents
    
    def update_state(self):
         #use tools such as FEA to update properties list
        #self.grid_prop_stress = FEA()
        return
