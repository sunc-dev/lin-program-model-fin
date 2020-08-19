# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 07:59:21 2020

@author: csunj
"""



try:
    import pulp as pl
    import sys
    import pandas as pd
    
    sys.path.append('.')
    from transform import Data as nm
    
except Exception as e:
    print("Some Modules are Missing {}".format(e))

class Contraints():
   def __init__(self, budget=None, proximity=None, endangerment=None, trees=None, water=None, area=None):
        
        self.budget = 7500
        self.proximity = 20
        self.endangerment = 15
        self.trees = 10
        self.water = 22
        self.area = 15


class Model(object):
    def __init__(self, name=None):    
        self.modelName = name
    
    def load(self):
        tr = nm()
        data = tr.getData('input.csv')
        inputs = tr.normalize(data)
        return inputs

    def init_model(self,inputs):
        
        self.modelName = 'porfolio-opt'
        
        decisions = []
        objective = []
        eq = []
        
        try:    
            model = pl.LpProblem(self.modelName, pl.LpMaximize)

            decisions = [pl.LpVariable(str('x'+str(index)),
                                       lowBound=0,
                                       upBound=1, 
                                       cat='Binary') for index in inputs.index]
            print('Decision vector: ')
            for decision in decisions:
                print(decision)

            eq = pl.lpSum([(inputs.Area[i]+
                          inputs.Trees[i]+
                          inputs.Water[i]+
                          inputs.Endangered[i]+
                          inputs.NaturalReserve[i])*decisions[j]
                           for i in inputs.index for j,decision in enumerate(decisions) if i==j])
                        
            objective += eq
            model += objective
            print("Objective Function: "+ str(objective))

        except:
            print("Model initalize failed")
        return model, decisions
    
    def constraints(self,model,inputs,decisions):
        
        props = Contraints()
        budget = ''
        proximity = ''
        endangerment = ''
        trees = ''
        water = ''
        area = ''
        
        try:
            for index, row in inputs.iterrows():
                for i, decision in enumerate(decisions):
                    if index==i:
                        
                        budget += row.Price*decision
                        proximity += row.NaturalReserve*decision
                        endangerment += row.Endangered*decision
                        trees += row.Trees*decision
                        water += row.Water*decision
                        area += row.Area*decision
                        
    
            #Constraint inequalities
            model += (budget <= props.budget, 'budget_constraint')
            model += (proximity <= props.proximity, 'proximity_constraint')
            model += (endangerment >= props.endangerment, 'endangered_constraint')
            model += (trees >= props.trees, 'trees_constraint')
            model += (water >= props.water, 'water_constraint')
            model += (area >= props.area, 'area_constraint')
        
        except:
            print('Constraint setup failed')
            
        print("Optimization function: "+ str(model))
        return model

    def solve(self, model, inputs):
        solver = pl.PULP_CBC_CMD(msg=True, warmStart=True)
        result = model.solve(solver)  
        
        print("Model status: " + pl.constants.LpStatus[result])
        print("Optimal solution output: ", pl.value(model.objective))
        for variable in model.variables():
            print('Decision: '+variable.name, "=", variable.varValue)
    
        decisions = [(int(i.name.strip('x')), i.varValue) for i in model.variables()]
        decisions = pd.DataFrame(list(decisions), columns=['id','Decision'])
        
        inputs = inputs.merge(decisions[['id',
                                        'Decision']], 
                              how='left',
                              left_on= inputs.index,
                              right_on=['id']
                              )


        inputs = inputs.drop(['id'],axis=1)
        return inputs



