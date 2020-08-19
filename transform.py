# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 12:30:58 2020

@author: csunj
"""


try:
 
    import os
    import pandas as pd
      
except Exception as e:
    print("Some Modules are Missing {}".format(e))


class Path():            
    def __init__(self, root=None, folder=None):
       self.root = os.path.dirname(os.path.abspath(__file__))
       self.folder = os.path.join(self.root,'data')

    def pathItems(self):
        return self.root, self.folder


class Data():  
    def __init__(self):
        self.data = 'Id'
        
    def getData(self, __data):
        root, folder = Path().pathItems()
        data = pd.read_csv(os.path.join(root,folder, __data))
        
        return data
    
    def normalize(self, data):
        
        inputs = data
        
        def norm_water (row):
            if row['Water'] == 'Poor':
                return 0.4
            if row['Water'] == 'Good':
                return 0.6
            if row['Water'] == 'Excellent':
                return 1
            return 0
    
        def norm_endangered (row):
            if row['Endangered'] <= 40:
                return row['Endangered']*0.005
            if row['Endangered'] > 60:
                return (row['Endangered']-60)*0.005+.8
            return (row['Endangered']-40)*0.03+0.2
                
        def norm_reserve (row):
            if row['NaturalReserve'] <= 7:
                return ((-0.5/7)*row['NaturalReserve'])+1
            return (-0.5/3)*(row['NaturalReserve']-7)+0.5
            
        
        inputs['Area'] = inputs['Area']*0.2
        inputs['Trees'] = inputs['Trees']*1/200
        inputs['Water'] = inputs.apply(lambda row: norm_water (row),axis=1)
        inputs['Endangered'] = inputs.apply(lambda row: norm_endangered (row),axis=1)
        inputs['NaturalReserve'] = inputs.apply(lambda row: norm_reserve (row),axis=1)
        return inputs

    
