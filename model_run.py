# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 10:03:31 2020

@author: csunj
"""


try:
    import sys
    sys.path.append('.')
    
    from model import Model as md
    
except Exception as e:
    print("Some Modules are Missing {}".format(e))


if __name__ == '__main__':    

    try:
        modelize = md()
        inputs = modelize.load()
        model, decisions = modelize.init_model(inputs)
        model = modelize.constraints(model, inputs, decisions)
        inputs = modelize.solve(model, inputs)  
        
        print('Model run successful')
        
    except:
        print('Model run fail')
    