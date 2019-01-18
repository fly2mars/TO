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

ON = 255
OFF = 0
vals = [ON, OFF]


class ruleEngine():
    '''    
    1. Hold an knowlege base (eg. rules and facts) for application
    2. Help agents to make a decision.
    '''
    def __init__(self):
        self.rules = {}
        return
    def add_rules(rule):
        '''
        f(agent,env)
        '''
        idx = len(self.rules.keys())
        rules[idx] = rule
        return
    def add_fact(fact):
        return


class agent:
    def __init__(self):
        self.pos = [0,0,0]
        self.total = 0
        return
    def set_pos(self, pos):
        self.pos = pos
    def get_state(self, name, env):
        
        return 
    def make_decision(self):
        return
    
    def act(self):
        return
        

class environment:
    def __init__(self):
        self.dim = 2
        self.grid = np.zeros(0)
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
        return
       
  
def test_mas():
    rule_engine = ruleEngine()
    #rule_engine.add_rules()
    env = environment()
    
    env.set_dim(40,60)
    
    def update(frame_number, img):
        return env.update(img)
        
    
    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(env.grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img,),
                                  frames = 10,
                                  interval=50,
                                  save_count=50)
    plt.show()
    return
    

# call main
if __name__ == '__main__':
    #main()
    test_mas()