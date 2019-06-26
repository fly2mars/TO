ON = 200
OFF = 0

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
