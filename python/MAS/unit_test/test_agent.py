# coding=gbk
"""
"""
import copy
import unittest
if __name__ == '__main__':
    import sys
    sys.path.append("..")

from env.envMBB import *
from env.envShell import *
from ke.agent import *
from ke.worker import *


class TestAgent(unittest.TestCase):
    
    def test_with_global_KE_and_ENV(self):
        agt = Agent()
        env = ENV_MBB2D()
        env.set_dim([100,30])
        agents = []
        
        agt.set_environment(env)
        for i in range(10):
            a = copy.copy(agt)
            agents.append(a)
            print("agt.id: {} agents[i].id".format('等于' if id(agt) == id(agents[i]) else '不等于'))
            print("agt.ke: {} agents[i].ke".format('等于' if id(agt.ke) == id(agents[i].ke) else '不等于'))
            print("agt.env {} agents[i].env".format('等于' if id(agt.env) == id(agents[i].env) else '不等于'))
            
    def test_neighbours(self):
        agt = Shell_Agent()
        env = ENV_Shell_2D()
        dim = [100,300]
        env.set_dim(dim)
        
        agt.set_environment(env)
        env.bind_agent(agt) 
        
        i = 0
        ab = []
        for a in env.agents.values():
            if i > 0:
                aa = a.neighbours
                print("agents[i].neighbours {} agents[j].neighbours".format('is' if id(ab) == id(aa) else 'is not'))
            ab = a.neighbours
            i += 1

if __name__ == '__main__':
    unittest.main()