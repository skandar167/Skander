import numpy as np
from datetime import datetime, timedelta

def generate_sample_data():
    """Generate sample industrial data for demonstration"""
    return {
        'timestamp': datetime.now(),
        'temperature': np.random.normal(150, 10),  # °C
        'pressure': np.random.normal(2.5, 0.2),    # bar
        'flow_rate': np.random.normal(100, 5),     # m³/h
        'energy_consumption': np.random.normal(500, 50),  # kWh
        'product_quality': np.random.normal(0.95, 0.02),  # %
        'raw_material_input': np.random.normal(1000, 50),  # kg
        'product_output': np.random.normal(950, 45),      # kg
        'waste_generated': np.random.normal(50, 5),       # kg
        'co2_emissions': np.random.normal(200, 20),       # kg
        'water_consumption': np.random.normal(5000, 500), # L
        'maintenance_hours': np.random.normal(8, 1),      # hours
        'production_cost': np.random.normal(1000, 100),   # €
    }

def generate_historical_data(days=30):
    """Generate historical data for trend analysis"""
    data = []
    start_date = datetime.now() - timedelta(days=days)
    
    for i in range(days * 24):  # Hourly data
        timestamp = start_date + timedelta(hours=i)
        sample = generate_sample_data()
        sample['timestamp'] = timestamp
        data.append(sample)
    
    return data
