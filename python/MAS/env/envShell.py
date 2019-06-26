import numpy as np
import copy
   
from env.env import *

class ENV_Shell_2D(Environment):
    def __init__(self):
        Environment.__init__(self)
                
        ## properties list
        self.grid_prop_pos_energy= np.zeros(0)   
        self.step = 0
        self.is_convergence = False
        self.agents = {}
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
        ##init design variables...
        self.grid = (np.zeros(dim)+255).astype(int)    #set wite
        ##init properties...
        self.grid_prop_pos_energy = (np.zeros(dim) - 1).astype(int)  
        self.grid_prop_pos_energy_copy = self.grid_prop_pos_energy.copy()
        return
    
    def bind_agent(self, agent):    
        self.agents = {}
        H, W = self.dim
        for i in range(H):
            for j in range(W):
                agt = copy.copy(agent)  # copy an agent
                agt.bind_pos((i,j))
                self.agents[(i,j)] = agt
        
        #set up neighbours
        for a in self.agents.values():
            a.setup_neighbours()
        
        return self.agents
    
    def update_state(self):
         #use tools such as FEA to update properties list
        #self.grid_prop_stress = FEA()
        self.grid_prop_pos_energy = self.grid_prop_pos_energy_copy.copy()
        return
    
    def set_step(self, is_convergence):
        if is_convergence:
            self.step += 1
        return 
    
    def get_step(self):        
        return self.step
    
    def dump(self):
        print(self.grid_prop_pos_energy)
        print(self.grid_prop_pos_energy_copy)

if __name__ == '__main__':
    env = ENV_MBB2D()
    env.set_dim([3,3])
    env.dump()