# -*- coding: utf-8 -*-


import numpy as np
import openturns as ot
import pytest
from smt.surrogate_models import LS
from smt.sampling_methods import LHS
from smt.problems import Sphere    
import otsmt
# Construction of the DOE
fun = Sphere(ndim=2)

ot.RandomGenerator.SetSeed(0)
experiment = ot.LHSExperiment(ot.ComposedDistribution([ot.Uniform(-10,10.),ot.Uniform(-10,10)]), 40, False, True)
xt = np.array(experiment.generate())
yt = fun(xt)
# Compute the gradient
for i in range(2):
    yd = fun(xt, kx=i)
    yt = np.concatenate((yt, yd), axis=1)
    
xv= np.array([[0.,0.]])


"""
Test for Least Squares Model
"""

def test_LS():
    sm_ls = LS()
    sm_ls.set_training_values(xt, yt[:,0])
    sm_ls.train()
    
    
    otls = otsmt.smt2ot(sm_ls)
    otlsprediction = otls.getPredictionFunction()
    yv = otlsprediction(xv)
    assert yv[0][0]== pytest.approx(66.6975,abs=1e-4)
