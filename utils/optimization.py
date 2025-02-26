import numpy as np
from scipy.optimize import minimize

def objective_function(x, weights):
    """
    Multi-objective function combining different KPIs
    x: array of process parameters
    weights: importance weights for different objectives
    """
    temperature, pressure, flow_rate = x
    
    # Simulate process outcomes
    energy_consumption = 0.5 * temperature + 0.3 * pressure + 0.2 * flow_rate
    product_quality = -0.2 * (temperature - 150)**2 - 0.3 * (pressure - 2.5)**2 - 0.1 * (flow_rate - 100)**2 + 100
    yield_rate = -0.1 * (temperature - 160)**2 - 0.2 * (pressure - 2.7)**2 - 0.1 * (flow_rate - 95)**2 + 95
    
    # Combine objectives (negative because we want to maximize)
    return -(weights[0] * product_quality + 
            weights[1] * yield_rate - 
            weights[2] * energy_consumption)

def optimize_parameters(initial_guess, weights, bounds=None):
    """
    Optimize process parameters using multi-objective optimization
    """
    if bounds is None:
        bounds = [(100, 200),  # Temperature bounds
                 (1.5, 3.5),   # Pressure bounds
                 (80, 120)]    # Flow rate bounds
    
    result = minimize(
        objective_function,
        initial_guess,
        args=(weights,),
        bounds=bounds,
        method='SLSQP'
    )
    
    return {
        'success': result.success,
        'optimal_parameters': {
            'temperature': result.x[0],
            'pressure': result.x[1],
            'flow_rate': result.x[2]
        },
        'optimal_value': -result.fun  # Negative because we minimized negative objective
    }
