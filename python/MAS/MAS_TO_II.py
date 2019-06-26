"""
A simple multi-agent evolution design demo

TODO:

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
from env.envShell import *
from ke.ke_shell import *
from ke.worker import *

#TODO:
# Add evaluator
# Add global variable to env.params


#Global object
knowledge_engine = KE_shell()
environment      = ENV_Shell_2D()
agent            = Shell_Agent()

agent.set_knowledge_engine(knowledge_engine)
agent.set_environment(environment)

#Global setting
environment.add_param("max_pixel", 255)
environment.add_param("scale_para", 1)
environment.add_param("thickness", 2)


#Evolve procedure
def evolve_by_agents(W, H, knowledge_engine, environment, agent):
    # Variables used for convergence test
    nItem = 0
    N = 100    
    total_dense = W * H * (W + H)/4   
    convg = suFuncStack.convergence(3)
    agt = agent
    ke = knowledge_engine
    
    ## init
    #1. setup up environment(constriants: load, fix, support; properties: density, dc, stress)    
    env = environment
    env.set_dim([H, W]) 
    
    #2. bind agents for environment
    agts = env.bind_agent(agt)
    
    env.update_state()
    convg.add_data(nItem, env.grid_prop_pos_energy, total_dense)
    ## evolve algorithm
    def agent_update(frame_number, img, line):
        nonlocal env
        nonlocal nItem                
        nonlocal total_dense
        nonlocal convg
        nonlocal ani
        
        ## evolve
        for a in agts.values():
            a.act()  # (1)sense (2)decite (3)act
        
        #showing environment    
        img.set_data(env.grid_prop_pos_energy * environment.get_param('scale_para'))
        
        #showing convergence
        nItem += 1       
        
        ## update          
        env.update_state()
        convg.add_data(nItem, env.grid_prop_pos_energy, total_dense)  
        env.dump()
        line.set_data(convg.get_data())  
        
        #test if convergence
        env.set_step(convg.is_convergence())
                  
        if env.step > 3:
            ani.event_source.stop() 
        return img, line        

    # set up animation
    fig, (ax1,ax2) = plt.subplots(2,1)
    img = ax1.imshow(env.grid_prop_pos_energy, interpolation='nearest')
    img.set_clim(vmin=0, vmax=environment.get_param('max_pixel'))           ## reset min max scale for image
    ax2.set_ylim(0, 0.4)
    ax2.set_xlim(0, N)  
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Change')
    line, = ax2.plot([], [], lw=2, color='r')
    
    
    ani = animation.FuncAnimation(fig, agent_update, fargs=(img,line,),
                                  frames = 10,
                                  interval=50,
                                  save_count=20)    
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
    environment.add_param('scale_para', environment.get_param('max_pixel') / (max(x,y) / 2) )
    
    evolve_by_agents(x, y, knowledge_engine, environment, agent)


 