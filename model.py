# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 07:59:21 2020

@author: csunj
"""


path = r'C:\Users\csunj\Downloads\Modelling'

try:
    
    import pulp as pl
    import sys, os
    import pandas as pd
        
    
    
    sys.path.append(path)
    from transform import Data as nm

      
except Exception as e:
    print("Some Modules are Missing {}".format(e))



def load_data():
    tr = nm()
    data = tr.getData('input.csv')
    inputs = tr.normalize(data)
    return inputs


inputs = load_data()


model = pl.LpProblem('porfolio-opt', pl.LpMaximize)


#create Decision Variables
decisions = []
for index, row in inputs.iterrows():
    var = str('x' + str(index))
    var = pl.LpVariable(str(var), lowBound = 0, upBound = 1, cat='Integer')
    decisions.append(var)
    
print ("Total number of decisions: " + str(len(decisions)))


#define objective function object
objective_value = ""
for index, row in inputs.iterrows():
    for i, decision in enumerate(decisions):
        if index== i:
            expression = (row.Area + row.Trees + row.Water + row.Endangered + row.ReserveProximity)*decision
            objective_value += expression

#add objective function to model
model += objective_value
print("Objective Function: "+ str(objective_value))


#define constraints object
budget_constraint = 7500
proximity_constraint = 20.00
endangered_constraint = 15.00
trees_constraint = 10.00
water_economy_constraint = 22.00
area_constraint = 15.00

total_budget = ''
proximity = ''
endangered_levels = ''
trees_level = ''
water_economy = ''
area = ''


for index, row in inputs.iterrows():
    for i, decision in enumerate(decisions):
        if index==i:
            
            budget_eq = row.Price*decision
            proximity_eq = row.ReserveProximity*decision
            endangered_eq = row.Endangered*decision
            trees_eq = row.Trees*decision
            water_eq = row.Water*decision
            area_eq = row.Area*decision
            
            total_budget += budget_eq
            proximity += proximity_eq
            endangered_levels += endangered_eq
            trees_level += trees_eq
            water_economy += water_eq
            area += area_eq
            
            
#add contraints to model
model += (total_budget <= budget_constraint, 'budget_constraint')
model += (proximity <= proximity_constraint, 'proximity_constraint')
model += (endangered_levels <= endangered_constraint, 'endangered_constraint')
model += (trees_level <= trees_constraint, 'trees_constraint')
model += (water_economy <= water_economy_constraint, 'water_constraint')
model += (area <= area_constraint, 'area_constraint')

print("Optimization function: "+ str(model))


#run optimization
result = model.solve()
 
assert result == pl.constants.LpStatusOptimal