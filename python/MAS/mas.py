"""
A simple multi-agent evolution design demo

TODO:

knowlegment presentation
rule deduce
decision and action




Reference:
1. CLIPs http://pyclips.sourceforge.net/web/
2. Life game https://github.com/electronut/pp/blob/master/conway/conway.py
3. pyKnow https://pyknow.readthedocs.io/en/stable/introduction.html

"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

from rule import Rule


ON = 255
OFF = 0
vals = [ON, OFF]

'''
rule:

In order to bridge the mathematical variables and logical rules, We must design a scheme that 
describe "rules" in text mode and deduce if the current variables are match with the rules
during the run time. That means the data of program and knowlegement are seperated. A knowlege
engine should be used to apply the knowlege to the data.

example:
   [rules]
   (total < 2 or total > 3) and state = ON -> state=OFF
   (total == 3) -> state=ON
   
   [facts/variables]
   total = 3
   status = X
   
How to make a decision by state varibles and rules?

The solution is:
- use @decrator to define fact and rules[easy to formulate]
- use sensor to convert varible and value to fact[eg. sensor(total)]
   
example:
    ke = KnowlegeEngine()
    ke.add_fact(total= 2)
    ke.add_fact(state=ON)
    @Rule(
      AND(
        OR(
        TEST(total, lambda x: x < 2),
        TEST(total, lambda x, > 3)
        ),
        Fact(state = ON)
      )
      agent.act_xxx:
          pass
    
   
'''

class KnowlegeEngine():
    '''    
    1. Hold an knowlege base (eg. rules and facts) for application
    2. Help agents to make a decision.
    '''
    def __init__(self):
        self.rules = {}
        self.facts = {}
        return
    def reset(self):
        '''
        Unlike with CLIPs, our knowlege engine must hold some consistant status, so 
        we prefer to adopt "update" instead of "reset" 
        '''
        return
    
    def add_rules(self, *rule):
        '''
        f(agent,env)
        '''
        idx = len(self.rules.keys())
        rules[idx] = rule
        return
    def add_fact(self, **kwargs):
        f = dict(kwargs)
        self.facts.update(f)
        return
    def inference(self):
        
        return
    def status(self):
        print("Facts:")
        i = 0
        for k, v in self.facts.items():
            msg = "<f-{}> {} = {}".format(i, k, v)
            print(msg)
            i += 1




ke = KnowlegeEngine()
class Fact():
    '''
    Test version of Fact
    ''' 
    def __init__(self, **kwargs):
        global ke
        ke.add_fact(**kwargs)
   
class Rule(tuple):
    '''
    Test version of Rule
    '''
    def __init__(self, **kwarg):
        global ke
        ke.add_rules()
        return
    def __call__(self, *args, **kwargs):
        
        pass
        
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
        # get knowlegement about environment
        i = self.pos[0]
        j = self.pos[1]
        [H, W] = grid.shape
        total = int((grid[i, (j-1)%W] + grid[i, (j+1)%W] + 
                             grid[(i-1)%H, j] + grid[(i+1)%H, j] + 
                             grid[(i-1)%H, j] + grid[(i-1)%H, (j+1)%W] + 
                             grid[(i+1)%H, (j-1)%W] + grid[(i+1)%H, (j+1)%W])/255)        
        return total, grid[i,j] 
    def make_decision(self, **fact):
        # make decisions and do actions by current knowledge
        facts = dict(**fact)
        ##(total < 2 or total > 3) and state = ON -> state=OFF
        ##(total == 3) -> state=ON
        if (facts.get('total') < 2 or facts.get('total') > 3 ) and (facts.get('state') == ON):
            self.act_OFF()
        if (facts.get('total') == 3 ):
            self.act_ON()
        
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
        init a grid with dimention of (row, col, height)
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
    
    def update(self, img):
        grid = self.grid
        newGrid = grid.copy()   
        H = self.H
        W = self.W
        for i in range(H):
            for j in range(W):
                total = int((grid[i, (j-1)%W] + grid[i, (j+1)%W] + 
                                     grid[(i-1)%H, j] + grid[(i+1)%H, j] + 
                                     grid[(i-1)%H, j] + grid[(i-1)%H, (j+1)%W] + 
                                     grid[(i+1)%H, j-1] + grid[(i+1)%H, (j+1)%W])/255)
                # apply Conway's rules
                if grid[i, j]  == ON:
                    if (total < 2) or (total > 3):
                        newGrid[i, j] = OFF
                else:
                    if total == 3:
                        newGrid[i, j] = ON                
                        # update data
        img.set_data(newGrid)  
        self.grid = newGrid
        print(self.step)
        self.step += 1
        return
       
  
def test_environment():
    ke = KnowlegeEngine()
    #rule_engine.add_rules()
    env = Environment()
    
    env.set_dim(40,60)
    
    def update(frame_number, img):
        env.update(img)
        
    
    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(env.grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img,),
                                  frames = 10,
                                  interval=50,
                                  save_count=50)
    plt.show()
    return
    

def test_agent():
    global ke
    ke = KnowlegeEngine()
    env = Environment()
    env.set_dim(40,60)
    #init agent for environment
    agts = env.bind_agent()
    
    def agent_update(frame_number, img):
        nonlocal env
        newGrid = env.grid.copy() 
        for a in agts:
            a.update(newGrid)
        img.set_data(env.grid)  
         
        return img
        
    
    total = 1
    Fact(total=total, state=ON, pos=0)
    Fact(total=total, state=ON, pos=1)
    #ke.add_fact(total=total, state=ON, pos=0)
    
    ke.status()
    #ke.add_rules()
    #@Rule(
        #AND(
            #OR(User('admin'),
               #User('root')),
            #NOT(Fact('drop-privileges'))
        #)
    #)
    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(env.grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, agent_update, fargs=(img,),
                                  frames = 10,
                                  interval=50,
                                  save_count=50)    
    plt.show()   
    
    
if __name__ == '__main__':
    #test_environment()
    test_agent()


 