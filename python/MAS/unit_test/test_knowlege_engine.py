"""
"""
import copy
import unittest
if __name__ == '__main__':
    import sys
    sys.path.append("..")

from env.envMBB import *
from ke.agent import *
from pyknow import *


class KE_Base(object):
    '''    
    1. Hold an knowlege base (eg. rules and facts) for application
    2. Help agents to make a decision.
    '''
    def __init__(self):
        self.rules = []
        self.facts = []
        self.answers = []
        return
    def update(self):
        '''
        Unlike with CLIPs, our knowlege engine must hold some consistant status, so 
        we prefer to adopt "update" instead of "reset" 
        '''
        return

    def add_rules(self, *rule):
        '''
        f(agent,env)
        '''       
        return
    
    def add_facts(self, *facts):
        pass
        
    def inference(self):

        return
    def status(self):
        print(self.facts)

       
class GetMaximumTest(KnowledgeEngine, KE_Base):
    @DefFacts()
    def __init_fact(self):
        yield(Fact(status='init'))
    
    @Rule(NOT(Fact(max=W())))
    def set_max(self):
        self.declare(Fact(max=0))
    
    @Rule(Fact(val = MATCH.val), 
          AS.m << Fact(max = MATCH.max),
          TEST(lambda max, val: val >= max))
    def get_new_max(self, m, val):
        self.modify(m, max = val)
  
        
    @Rule(AS.v << Fact(val=MATCH.val),
          Fact(max=MATCH.max),
          TEST(lambda max, val: val <= max))
    def remove_val(self, v):
        self.retract(v)  
    
    @Rule(AS.v << Fact(max=W()),
          NOT(Fact(val=W())))
    def print_max(self, v):
        print(self.facts)
        print("Max:", v['max'])    


class ManageFact(KnowledgeEngine, KE_Base):
    @DefFacts()
    def __init_facts(self):
        yield(Fact(status='init'))
    
    def add_facts(self, fact):
        self.declare(*fact)
        
class GetAnswers(KE_Base, KnowledgeEngine):
    def __init__(self):
        KE_Base.__init__(self)
        KnowledgeEngine.__init__(self)
    @DefFacts()
    def __init_facts(self):
        yield(Fact(status='init'))
    
    @Rule(Fact(status = 'init'))
    def get_answer(self):
        self.answers.append('init')
    
class TestKE(unittest.TestCase):    
    def test1(self):
        m = GetMaximumTest()
        m.reset()
        print(m.facts)
        m.declare(*[Fact(val=x) for x in (12, 33, 42, 99, 55, 11, 75)]) 
        print(m.facts)
        m.reset()
        print('---reset-----')
        print(m.facts)
        m.declare(*[Fact(val=x) for x in (12, 33, 42, 99, 55, 11, 75)])
        print('---declare-----')
        print(m.facts)
        m.run()
    
    # change class varibles 
    def test2(self):
        f = [Fact(v=x) for x in range(3)]
        print(f)
        tc = ManageFact()
        tc.reset()
        
        tc.add_facts(f)

        tc.status()
    
    def test3(self):
        tc = GetAnswers()
        tc.reset()
        tc.declare()
        tc.run()
        for s in tc.answers:
            print(s)
if __name__ == '__main__':
    unittest.main()
    