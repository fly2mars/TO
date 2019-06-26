'''

'''
from ke.agent import Agent
from ke.ke_shell import *
from pyknow import Fact

def position_energy_inc(env, pos):
    vals = []
    nn = env.agents[pos].neighbours
    for a in nn:
        vals.append( env.grid_prop_pos_energy[a.pos]  )
    v = [x for x in vals if x != -1]
    if len(v) == 0:
        return
    v_min = min(v)
    env.grid_prop_pos_energy_copy[pos] = v_min + 1
    
    return

def set_energy(env, pos, val):
    env.grid_prop_pos_energy_copy[pos[0]][pos[1]] = val
    return      
        
class Shell_Agent(Agent):
    def __init__(self):
        #set global KB engine and enviorment
        super().__init__()
        
        return
    
    def sense(self, name):
        # get knowlegement about environment
        if name == 'if_edge':
            H, W = self.env.get_dim()
            y, x = self.pos
            v = False
            if x == W-1 or x == 0 or y == H-1 or y == 0:
                v = True
            return Fact(if_edge=v)
        if name == 'pos_energy':
            i = self.pos[0]
            j = self.pos[1]
            v = self.env.grid_prop_pos_energy[i][j]
            return Fact(pos_energy = v)
        #if name == 'is_convergence':    
            #v = self.env.is_convergence
            #return Fact(is_convergence = v)
        if name == 'step':
            v = self.env.get_step()
            return Fact(step = v)
        if name == 'thickness':
            v = self.env.get_param('thickness')
            return Fact(thickness = v)
        
        return
   
    def make_decision(self): 
        # sense environment
        fs = []
        fs.append(self.sense('if_edge'))
        fs.append(self.sense('pos_energy'))
        fs.append(self.sense('thickness'))
        fs.append(self.sense('step'))
        
        self.ke.reset()
        self.ke.add_facts(fs)
        #print(self.ke.facts)
        self.ke.run()
        return
    
    def setup_neighbours(self):
        self.neighbours = []
        H, W = self.env.get_dim()
        neighbours = lambda y, x : [(y2, x2) for x2 in range(x-1, x+2) for y2 in range(y-1, y+2) 
                           if (-1 < x < W and
                           -1 < y <=H and
                           (x != x2 or y != y2) and
                           (0 <= x2 < W) and
                           (0 <= y2 < H))]
        
        i,j = self.pos
        for pos in neighbours(i,j):
            self.neighbours.append(self.env.agents[pos])
    
        
    def act(self):        
        self.make_decision()
        for a in self.ke.answers:
            if a == "set_edge":
                set_energy(self.env, self.pos, 0)
            if a == "pe_inc":
                position_energy_inc(self.env, self.pos)
            if a == "make_shell":
                set_energy(self.env, self.pos, self.env.get_param('max_pixel')/ self.env.get_param('scale_para'))
                

        #print(self.pos)
        #print(self.ke.answers)
        #print(self.env.grid_prop_pos_energy)
        return