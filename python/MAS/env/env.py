class Environment(object):
    def __init__(self):
        self.grid = []
        self.agents = []
        self.dim = ()
        self.params = {}
    
    def set_dim(self, dim):
        pass
    def get_dim(self):
        return self.dim
    
    def update_state(self):
        pass
    
    def bind_agent(self, agent):
        pass
    
    ## knowledges management
    def add_param(self, key, value):
        self.params[key] = value
    
    def get_param(self, key):
        return self.params[key]
        