# first.py
# first-order linear ODE
# Dec. 2017 by Kenji Doya

import numpy as np

# Right-hand-side function of the ODE
def dynamics(y, t, a, b):
    """first-order linear ODE: dy/dt = a*y + b"""
    return(a*y + b)

# Name of the system
name = 'first'

# A standard initial state
initial_state = 1

# Default parameters
parameters = (-0.1, 0)

# For adding to the system list
name_state_parameters = [name, initial_state, parameters]
