class FactOperator(object):
    def __init__(self):
        pass
    
    def func_larger_than(self, var, val=None):
        return var > val
    
    def func_equal(self, var, val=None):
        return var == val
    
    def func_less_than(self, var, val=None):
        return var < val   
    
    def func_larger_than_neighbors(self, var, val=None):
        return 
    
    def make_fact(self, func_name, var, val=None):
        if hasattr(self, "func_" + func_name):
            return getattr(self, "func_" + func_name)(var, val)
        
    def get_operators(self):
        attributes = dir(self)
        substr = 'func_'
        operators = [ i.replace(substr, '') for i in attributes if substr in i]
        return operators 
    
    
if __name__ == '__main__':
    fo = FactOperator()
    print(fo.make_fact('larger_than', 3, -1) )
    print(fo.get_operators())