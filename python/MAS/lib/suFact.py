class Fact():
    '''
    Test version of Fact
    ''' 
    def __init__(self, **kwargs):
        global ke
        ke.add_fact(**kwargs)