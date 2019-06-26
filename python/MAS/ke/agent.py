class Agent(object):
    def __init__(self):
        #set global KB engine and enviorment
        self.ke = None
        self.env = None
        
        self.pos = []
        self.total = 0  
        self.neighbours = []   # save neighbours. The order will depend on the in heritance class
        return
    
    def set_knowledge_engine(self, ke):
        #avoid deep copy
        self.ke = ke
        
    def set_environment(self, env):
        self.env = env
        
    def bind_pos(self, pos):
        self.pos = pos
        
    def sense(self, name):
        # get knowlegement about environment
        return
   
    def make_decision(self):       
        return
    
    def act(self):
        self.make_decision()
        return
    
    def setup_neighbours(self):
        pass