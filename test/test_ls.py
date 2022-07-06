# -*- coding: utf-8 -*-


import numpy as np
import pytest
from smt.surrogate_models import LS
from smt.sampling_methods import LHS
from smt.problems import Sphere    
import otsmt
# Construction of the DOE
fun = Sphere(ndim=2)
sampling = LHS(xlimits=fun.xlimits, criterion="m")
xt = sampling(40)
yt = fun(xt)
# Compute the gradient
for i in range(2):
    yd = fun(xt, kx=i)
    yt = np.concatenate((yt, yd), axis=1)
    
xv= sampling(2)


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
    assert yv[0][0]== pytest.approx(56.9874,abs=1e-4)
