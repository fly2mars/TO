'''
rule:

In order to bridge the mathematical variables and logical rules, We must design a scheme that 
describe "rules" in text mode and deduce if the current variables are match with the rules
during the run time. That means the data of program and knowlegement are seperated. A knowlege
engine should be used to apply the knowlege to the data.

example:
   [rules]
   (total < 2 or total > 3) and state = ON -> state=OFF
   (total == 3) -> state=ON

   [facts/variables]
   total = 3
   status = X

How to make a decision by state varibles and rules?

The solution is:
- use @decrator to define fact and rules[easy to formulate]
- use sensor to convert varible and value to fact[eg. sensor(total)]

example:
    ke = KnowlegeEngine()
    ke.add_fact(total= 2)
    ke.add_fact(state=ON)
    @Rule(
      AND(
        OR(
        TEST(total, lambda x: x < 2),
        TEST(total, lambda x, > 3)
        ),
        Fact(state = ON)
      )
      agent.act_xxx:
          pass   

'''

class KnowlegeEngine():
    '''    
    1. Hold an knowlege base (eg. rules and facts) for application
    2. Help agents to make a decision.
    '''
    def __init__(self):
        self.rules = {}
        self.facts = {}
        return
    def reset(self):
        '''
        Unlike with CLIPs, our knowlege engine must hold some consistant status, so 
        we prefer to adopt "update" instead of "reset" 
        '''
        return

    def add_rules(self, *rule):
        '''
        f(agent,env)
        '''
        idx = len(self.rules.keys())
        rules[idx] = rule
        return
    def add_fact(self, **kwargs):
        f = dict(kwargs)
        self.facts.update(f)
        return
    def inference(self):

        return
    def status(self):
        print("Facts:")
        i = 0
        for k, v in self.facts.items():
            msg = "<f-{}> {} = {}".format(i, k, v)
            print(msg)
            i += 1
