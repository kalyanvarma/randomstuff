import re
import ConfigParser, os
from configobj import ConfigObj

class Constraint:
    
    def isTrue():
        pass

class Action:

    def act():
        pass

class Rule:
    constraints = []
    actions = []

    def __init__(self, constraints=None, actions=None):
        self.constraints = []
        if constraints:
            self.addConstraints(constraints)

        self.actions = []
        if actions:
            self.addActions(actions)

    def addConstraints(self, constraints):
        if constraints is not None:
            if type(constraints) == list:
                for constraint in constraints:
                    if isinstance(constraint, Constraint):
                        self.constraints.append(constraint)
                    else:
                        print "Given constraint [" +str(constraint)+ "] is not of type 'Constraint'"
            elif isinstance(constraints, Constraint):
                self.constraints.append(constraints)
            else:
                print "Unable to add constraints. Constraints have to be of type 'Constraint'"

    def addActions(self, actions):
        if actions is not None:
            if type(actions) == list:
                for action in actions:
                    if isinstance(action, Action):
                        self.actions.append(action)
                    else:
                        print "Given action [" +str(action)+ "] is not a action"
            elif isinstance(actions, Action):
                self.actions.append(actions)
            else:
                print "Unable to add actions. Actions have to be of type 'Action'"

    def execute(self, params):
        for constraint in self.constraints:
            if not constraint.isTrue(params):
                return False
        #If all constraints pass
        for action in self.actions:
            action.act(params)
        return True

class MatchRegEx(Constraint):
    expression = ''
    
    def __init__(self, expression):
        self.expression = expression
        
    def isTrue(self, params):
        matches = re.match(self.expression, params['word'])
        if matches:
            return True
        else:
            return False

class MatchString(Constraint):
    matchstring = ''

    def __init__(self, matchstring):
        self.matchstring = matchstring

    def isTrue(self, params):
        if self.matchstring == params['word']:
            return True
        else:
            return False

class DoesNotMatchString(Constraint):
    matchstring = ''

    def __init__(self, matchstring):
        self.matchstring = matchstring

    def isTrue(self, params):
        if self.matchstring == params['word']:
            return False
        else:
            return True

class PrevWordDoesNotMatchString(Constraint):
    matchstring = ''

    def __init__(self, matchstring):
        self.matchstring = matchstring

    def isTrue(self, params):
        if self.matchstring == params['prevword']:
            return False
        else:
            return True

class NumberWithinRange(Constraint):
    min = None
    max = None

    def __init__(self, rangepattern):
        try:
            (self.min, self.max) = rangepattern.split('-')
            self.min=int(self.min)
            self.max=int(self.max)
        except ValueError:
            print "Could not initialize NumberWithinRange constraint. Given range string is not the correct format. Correct format example: 123-456"

    def isTrue(self, params):
        try:
            number = int(params['word'])
            if(number>=self.min and number<=self.max):
                return True
            else:
                return False
        except ValueError:
            #Not an integer number, so the constraint should evaluate to False
            return False

class NumberWithinPriceRange(Constraint):
    deviation = 0

    def __init__(self, devpercent):
        try:
            self.deviation = int(devpercent.split('%')[0])
        except ValueError:
            print "Could not initialize NumberWithinPriceRange constraint. Given deviation string is not the correct format. Correct format example: 20%"

    def isTrue(self, params):
        try:
            number = int(params['word'])
            stockprice = params['stockprice']
            pricedev = (stockprice*self.deviation/100)
            if(number>=(stockprice-pricedev) and number <=(stockprice+pricedev)):
                return True
            else:
                return False
        except ValueError:
            #Not an integer number, so the constraint should evaluate to False
            return False

class ReplaceWithVariable(Action):
    variablename = ''

    def __init__(self, variablename):
        self.variablename = variablename

    def act(self, params):
        params['word'] = self.variablename+"_"+params['word']

class Ignore(Action):

    def act(self, params):
        pass #Do nothing

word = '800'
prevword = 'year'

config = ConfigObj('config.cfg')
for rulegroupname, rulegroupvalue in config.items():
    print "Rule Group: [" +rulegroupname+ "]"
    for rulename, rulevalue in rulegroupvalue.items():
        constraints,actions = [],[]
        params = {}
        print "Rule: [" +rulename+"]"
        if rulevalue['constraints']:
            for consname, consvalue in rulevalue['constraints'].items():
                if consname=='MatchRegEx':
                    constraints.append(MatchRegEx(consvalue['parameter']))
                    params['word'] = word
                elif consname=='PrevWordDoesNotMatchString':
                    constraints.append(PrevWordDoesNotMatchString(consvalue['parameter']))    
                    params['prevword'] = prevword
                elif consname=='NumberWithinRange':
                    constraints.append(NumberWithinRange(consvalue['parameter']))
                elif consname=='NumberWithinPriceRange':
                    constraints.append(NumberWithinPriceRange(consvalue['parameter']))
                    params['stockprice'] = 1000
        
        if rulevalue['actions']:
            for actname, actvalue in rulevalue['actions'].items():
                if actname=='ReplaceWithVariable':
                    actions.append(ReplaceWithVariable(actvalue['parameter']))

        rule = Rule(constraints,actions)
        if rule.execute(params)==True:
            print "String after rule is [" +params['word']+ "]"
        else:
            print "Constraints were not met with params [" +str(params)+ "]"