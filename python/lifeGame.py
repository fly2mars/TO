"""
A simple life game writed in a multi-agent pattern
"""
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation


ON = 255
OFF = 0
vals = [ON, OFF]


class KnowlegeEngine():
    ''' 
    Only a prototype
    todo:
    1. Hold an knowlege base (eg. rules and facts) for application
    2. Help agents to make a decision.
    '''
    def __init__(self):
        self.rules = {}
        self.facts = {}
        return
    def reset(self):
        pass
    
    def add_rules(self, *rule):
        pass
    def add_fact(self, **kwargs):
        pass
    def inference(self):
        
        return
    def status(self):
        print("Facts:")
        i = 0
        for k, v in self.facts.items():
            msg = "<f-{}> {} = {}".format(i, k, v)
            print(msg)
            i += 1


class Agent:
    def __init__(self, ke, env):
        #set global KB engine and enviorment
        self.ke = ke
        self.env = env
        
        self.pos = [0,0]
        self.total = 0
        
        return
    def bind_pos(self, pos):
        self.pos = pos
    def sense(self, grid):
        '''
        In order to map Fact to system variables,
        there will be many type of sense functions.
        '''
        i = self.pos[0]
        j = self.pos[1]
        [H, W] = grid.shape
        total = int((grid[i, (j-1)%W] + grid[i, (j+1)%W] + 
                             grid[(i-1)%H, j] + grid[(i+1)%H, j] + 
                             grid[(i-1)%H, j] + grid[(i-1)%H, (j+1)%W] + 
                             grid[(i+1)%H, (j-1)%W] + grid[(i+1)%H, (j+1)%W])/255)        
        return total, grid[i,j] 
    def make_decision(self, **fact):
        '''
        To make decisions and do actions by current knowledge
        The fundamental process will be:
           - sensation: 
           - declare fact
           - inference
           - act
        Todo: representation of rules and facts
        Todo: done by KnowlegeEngine
        '''
        facts = dict(**fact)
        """
        Conway's rule: B3/S23
          - (total < 2 or total > 3) and state = ON -> state=OFF
          - (total == 3) -> state=ON
        """
        if (facts.get('total') < 2 or facts.get('total') > 3 ) and (facts.get('state') == ON):
            self.act_OFF()
        if (facts.get('total') == 3 ):
            self.act_ON()
        """
        Conway's rule: B6/S16
          - (total != 6 and total != 1) and state = ON -> state=OFF
          - (total == 6) -> state=ON
        """
        #if (facts.get('total') != 6 and facts.get('total') != 1 ) and (facts.get('state') == ON):
            #self.act_OFF()
        #if (facts.get('total') == 6 ):
            #self.act_ON()        
        
        return
    
    def update(self,grid):
        total, state = self.sense(grid)   # todo: bind sense to fact
        self.make_decision(total = total, state = state)
        return
    def act_OFF(self):
        pos = self.pos
        self.env.grid[pos[0],pos[1]] = OFF 
    def act_ON(self):
        pos = self.pos
        self.env.grid[pos[0],pos[1]] = ON     
   
      

class Environment:
    def __init__(self):
        self.grid = np.zeros(0)
        self.step = 0
        return
    def set_dim(self, row,col,height=0):
        '''
        init a grid with dimention of (H = row, W = col)
        '''
        self.H = row
        self.W = col
        if height==0:
            self.grid = np.random.choice(vals, row*col, p=[0.2, 0.8]).reshape(row, col)
        return
    
    def bind_agent(self):
        global ke
        H = self.H
        W = self.W
        agents = []

        for i in range(H):
            for j in range(W):
                agt = Agent(ke, self)
                agt.bind_pos([i,j])
                agents.append(agt)
        return agents
   
    def update(self):
        pass
     
def test_MAS():
    global ke
    ke = KnowlegeEngine()
    env = Environment()
    env.set_dim(40,60)
    #init agent for environment
    agts = env.bind_agent()
    
    def agent_update(frame_number, img):
        nonlocal env
        cur_grid = env.grid.copy() # sense from cur_grid and update to env.grid
        for a in agts:
            a.update(cur_grid)     # actions from agents
        img.set_data(env.grid)    
        env.update()               # update status by environment(eg. FEA, some feedbacks)
        return img
        
  
    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(env.grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, agent_update, fargs=(img,),
                                  frames = 10,
                                  interval=50,
                                  save_count=50)    
    plt.show()   
    
    
if __name__ == '__main__':
    test_MAS()


 
