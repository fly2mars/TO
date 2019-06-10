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
from lib.suKnowlegeEngine import *
from lib.suAgent import *
from lib.suEnvironment import *
#TODO:
# Add evaluator
# Add sensor
def evolve_by_agents(x,y,ke):
    # Variables used for convergence test
    nItem = 0
    N = 100    
    total_dense = x * y * (ON - OFF)    
    convg = suFuncStack.convergence(5)
    ## init
    #1. setup up environment(constriants: load, fix, support; properties: density, dc, stress)    
    env = Environment(ke)
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
    #Fact(total=total, state=ON, pos=0)
    #Fact(total=total, state=ON, pos=1)
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


 