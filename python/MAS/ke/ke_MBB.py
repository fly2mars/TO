"""
Knowledge engine for MBB optimization
TODO: many many things...
"""
from pyknow import *
from ke.ke import KnowledgeEngineBase

class KE_MBB(KnowledgeEngineBase, KnowledgeEngine):
    '''    
    1. Hold an knowlege base (eg. rules and facts) for application
    2. Help agents to make a decision.
    '''
    def __init__(self):
        super().__init__()
        
    @DefFacts()
    def __init_facts(self):
        yield(Fact(status='init'))
        return
    
    @Rule
    
    
    def status(self):
        print(self.Facts)
