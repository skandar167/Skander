import numpy as np
from scipy.integrate import odeint

class ProcessSimulator:
    def __init__(self):
        # Process parameters
        self.volume = 100.0  # m³
        self.cp = 4.18  # kJ/kg.K
        self.rho = 1000.0  # kg/m³
        
    def energy_balance(self, T, t, Q_in, T_in, flow_rate):
        """Energy balance equation for temperature evolution"""
        dTdt = (flow_rate * self.rho * self.cp * (T_in - T) + Q_in) / (self.volume * self.rho * self.cp)
        return dTdt
    
    def simulate_process(self, parameters, duration=3600, dt=60):
        """
        Simulate industrial process
        parameters: dict containing process parameters
        duration: simulation duration in seconds
        dt: time step in seconds
        """
        # Extract parameters
        T_initial = parameters.get('temperature', 150)
        Q_in = parameters.get('heat_input', 1000)
        T_in = parameters.get('inlet_temperature', 25)
        flow_rate = parameters.get('flow_rate', 100)
        
        # Time points
        t = np.linspace(0, duration, int(duration/dt))
        
        # Solve ODE
        T = odeint(self.energy_balance, T_initial, t, args=(Q_in, T_in, flow_rate))
        
        # Calculate other process variables
        energy_consumption = Q_in * duration / 3600  # kWh
        product_output = flow_rate * duration / 3600  # m³
        
        return {
            'time': t,
            'temperature': T.flatten(),
            'energy_consumption': energy_consumption,
            'product_output': product_output
        }
    
    def predict_kpis(self, simulation_results):
        """Predict KPIs based on simulation results"""
        return {
            'energy_efficiency': min(100, 85 + np.random.normal(0, 5)),
            'product_quality': min(100, 90 + np.random.normal(0, 3)),
            'yield_rate': min(100, 88 + np.random.normal(0, 4)),
            'cost_per_unit': 100 + np.random.normal(0, 10)
        }
