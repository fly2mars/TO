"""
Knowledge engine for A shell problem
Making shell in 3 steps.
Facts:
   step = {number}
   pos_energy = {number} -1: not init   0: edge   >0: inside
   if_edge = {bool}  True: is edge  False: not edge
   thickness = {val} val is the thickness of the shell [unit is the voxel]
   
Rules:
   rules for step 0:
    - step==edge(0) && pos energy=-1 && is edge  -> set pos energy to 0
   rules for step 1:
    - step==pos energy(1) && not edge && pos energy=-1 -> pos energy = min(neibghour) + 1
    - is convergence -> set step = shell(1)
   rules for step 2:
    - step==shell(2) && pos energy > thickness -> set pos energy to -1
"""
from pyknow import *
from ke.ke import KnowledgeEngineBase

class KE_shell(KnowledgeEngineBase, KnowledgeEngine):
    '''    
    1. Hold an knowlege base (eg. rules and facts) for application
    2. Help agents to make a decision.
    '''
    def __init__(self):
        KnowledgeEngineBase.__init__(self)
        KnowledgeEngine.__init__(self)
    
    def reset(self):
        super().reset()
        self.answers = []
    @DefFacts()
    def __init_facts(self):
        yield(Fact(method='shell'))
        return
    
    @Rule(Fact(if_edge = True),
          Fact(pos_energy = -1),
          Fact(step = 0)
          )
    def set_edge(self):
        self.answers.append( 'set_edge')
    
    @Rule(NOT (Fact(if_edge = True)),
          Fact(pos_energy = -1),
          Fact(step = 1)
          )
    def pe_inc(self):
        self.answers.append('pe_inc')
        
    @Rule(Fact(step = 2),
          NOT (Fact(if_edge = True)),
          Fact(pos_energy = MATCH.pos_energy),
          Fact(thickness = MATCH.thickness),
          TEST(lambda pos_energy, thickness: pos_energy > thickness)
          )
    def make_shell(self):
        self.answers.append('make_shell')
    
    #@Rule ( Fact(step = 0),
            #AS.f << Fact(step = 0),
            #Fact(is_convergence = True)
          #)
    #def change_status(self):
        #self.modify(f, step = 1)
        
    def add_facts(self, facts):
        self.declare(*facts)
    def status(self):
        print(self.facts)
