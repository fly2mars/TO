"""
A simple multi-agent evolution design demo

TODO:

1. knowlegment presentation
2. rule deduce
3. decision and action
4. evaluation and selection scheme.


Reference:
1. CLIPs http://pyclips.sourceforge.net/web/
2. Life game https://github.com/electronut/pp/blob/master/conway/conway.py
3. pyKnow https://pyknow.readthedocs.io/en/stable/introduction.html

"""
import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

from lib import suFuncStack


ON = 255
OFF = 0
vals = [ON, OFF]

'''
Tool functions
'''
import collections
class Convergence_data():
    def __init__(N):
        self.d = collections.deque()

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
        # todo: decision must be made by KB engine.
        facts = dict(**fact)
        ##(total < 2 or total > 3) and state = ON -> state=OFF
        ##(total == 3) -> state=ON
        if (facts.get('total') < 2 or facts.get('total') > 3 ) and (facts.get('state') == ON):
            self.act_OFF()
        if (facts.get('total') == 3 ):
            self.act_ON()
        
        return
    
    def act(self,grid):
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
    
    def update_state(self):
         #use tools such as FEA to update properties list
        #self.grid_prop_stress = FEA()
        return

def evolve_by_agents(x,y,ke):
    # Variables used for convergence test
    nItem = 0
    N = 100    
    total_dense = x * y * (ON - OFF)    
    convg = suFuncStack.convergence(5)
    ## init
    #1. setup up environment(constriants: load, fix, support; properties: density, dc, stress)
    env = Environment()
    env.set_dim(y,x)    
    
    #2. bind agents for environment
    agts = env.bind_agent()
    
    ## evolve
    def agent_update(frame_number, img, line):
        nonlocal env
        nonlocal nItem                
        nonlocal total_dense
        nonlocal convg
        env.update_state()
        newGrid = env.grid.copy() 
        last_grid = newGrid.copy()
        for a in agts:
            #env.update()
            a.act(newGrid)  # (1)sense (2)decite (3)act
        #showing environment    
        img.set_data(env.grid)          
        #showing convergence
        nItem += 1       
        convg.add_data(nItem, env.grid, total_dense)        
        line.set_data(convg.get_data())                        
        return img, line        
    
    total = 4
    Fact(total=total, state=ON, pos=0)
    Fact(total=total, state=ON, pos=1)
    #ke.add_fact(total=total, state=ON, pos=0)
    
    ke.status()   
    # set up animation
    fig, (ax1,ax2) = plt.subplots(2,1)
    img = ax1.imshow(env.grid, interpolation='nearest')
    ax2.set_ylim(0, 0.4)
    ax2.set_xlim(0, N)  
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Change')
    line, = ax2.plot([], [], lw=2, color='r')
    
    
    ani = animation.FuncAnimation(fig, agent_update, fargs=(img,line,),
                                  frames = 10,
                                  interval=50,
                                  save_count=50)    
    plt.show()   
    
    
    
    
if __name__ == '__main__':
    #parameters:    --x 50   --y 40  --KB r:/rule.txt
    parser = argparse.ArgumentParser(description="A multi agenter toplogy optimizer.")
    parser.add_argument('--x', dest='x', required=True)
    parser.add_argument('--y', dest='y', required=True)
    parser.add_argument('--KB', dest='KB', required=False)      #Knowlege base from txt file. In the first version, we cancle it.
    args = parser.parse_args()
    
    x = 60
    y = 20
    
    if args.x:
        x = int(args.x)
    if args.y:
        y = int(args.y)   
    
    ke = KnowlegeEngine()
    evolve_by_agents(x,y,ke)


 