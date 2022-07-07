# -*- coding: utf-8 -*-
# Copyright 2022 ONERA. 

"""
    SMT metamodels algorithm
    =================================
    Interpret smt algorithms as openturns Functions
"""


import openturns as ot
import numpy as np


class smt2ot(object):
    """
    Define a OpenTURNS class using Machine learning algorithms from smt.
    
    Parameters
    ----------
    model : a trained smt model
        model for response surface, already trained/validated      
    """
    
    def __init__(self,model):
        
        # input dimension
        if hasattr(model,"AVAILABLE_EXPERTS"): #check if model is moe
            self.inputDimension = model.ndim
        elif model.name == 'MixedIntegerKriging':
            self.inputDimension = len(model._xtypes)     
        else:
            self.inputDimension = model.nx
        
        # smt model
        self.smtModel = model
        


    def getPredictionFunction(self):
        """
        Function retrieving PredictionFunction for  smt model
        
        """

        # definition of ot PythonFunction for predicted responses
        smtMean = lambda x:self.smtModel.predict_values(np.array(x))
        PredictionFunction = ot.PythonFunction(self.inputDimension,1,func_sample=smtMean)

        return PredictionFunction

    
    def getConditionalVarianceFunction(self):
        """
        Function retrieving ConditionalVarianceFunction for  smt model (when available) 
        
        """


        # definition of ot PythonFunction for predicted response variances
        smtVariance = lambda x:self.smtModel.predict_variances(np.array(x))
        ConditionalVarianceFunction = ot.PythonFunction(self.inputDimension,1,func_sample=smtVariance)

        return ConditionalVarianceFunction
    
    
    def getPredictionDerivativesFunction(self,indexDerivatives):
        """
        Function retrieving predicted  derivatives function  of smt model (when available)

		:indexDerivatives: integer, coordinate of the derivative to be computed
        
        """

        # definition of ot PythonFunction for predicted response variances
        smtMeanDerivatives = lambda x:self.smtModel.predict_derivatives(np.array(x),indexDerivatives)
        PredictionDerivativesFunction = ot.PythonFunction(self.inputDimension,1,func_sample=smtMeanDerivatives)

        return PredictionDerivativesFunction
            