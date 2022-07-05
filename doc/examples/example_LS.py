"""
Example 3: Use of AK - SS on four branch function
-------------------------------------------------
"""

# %%

from smt.sampling_methods import LHS
from smt.problems import Sphere

import smt2ot


# %%
# | Definition of Input distribution

       
# Construction of the DOE
fun = Sphere(ndim=2)
sampling = LHS(xlimits=fun.xlimits, criterion="m")
xt = sampling(40)
yt = fun(xt)
# Compute the gradient
for i in range(2):
    yd = fun(xt, kx=i)
    yt = np.concatenate((yt, yd), axis=1)
       
xv= sampling(10)
    
# %%
# | Training of smt model for Least Squares
sm_ls = LS()
sm_ls.set_training_values(xt, yt[:,0])
sm_ls.train()

# %%
# | Creation of OpenTurns PythonFunction for prediction
otls = smt2ot.smt2ot(sm_ls)
otlsprediction = otls.getPredictionFunction()

print('Predicted values by LS:',otlsprediction(xv))