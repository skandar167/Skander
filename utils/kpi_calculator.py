def calculate_energy_efficiency(data):
    """Calculate energy efficiency KPIs"""
    return {
        'efficacite_energetique': (data['product_output'] / data['energy_consumption']) * 100,
        'consommation_unitaire': data['energy_consumption'] / data['product_output']
    }

def calculate_production_performance(data):
    """Calculate production performance KPIs"""
    return {
        'rendement_matiere': (data['product_output'] / data['raw_material_input']) * 100,
        'productivite': data['product_output'] / 24  # Daily production rate
    }

def calculate_quality_metrics(data):
    """Calculate quality-related KPIs"""
    return {
        'taux_conformite': data['product_quality'] * 100,
        'taux_dechets': (data['waste_generated'] / data['raw_material_input']) * 100
    }

def calculate_maintenance_metrics(data):
    """Calculate maintenance-related KPIs"""
    return {
        'mtbf': 720 / max(1, data['maintenance_hours']),  # Assumed 30 days (720 hours)
        'mttr': data['maintenance_hours']
    }

def calculate_environmental_metrics(data):
    """Calculate environmental KPIs"""
    return {
        'emissions_co2': data['co2_emissions'] / data['product_output'],
        'consommation_eau': data['water_consumption'] / data['product_output']
    }

def calculate_cost_metrics(data):
    """Calculate cost-related KPIs"""
    return {
        'cout_unitaire': data['production_cost'] / data['product_output'],
        'cout_energetique': (data['energy_consumption'] * 0.15) / data['product_output']  # Assumed energy cost 0.15€/kWh
    }

def calculate_all_kpis(data):
    """Calculate all KPIs"""
    return {
        'performance_energetique': calculate_energy_efficiency(data),
        'rendement_production': calculate_production_performance(data),
        'qualite_production': calculate_quality_metrics(data),
        'maintenance': calculate_maintenance_metrics(data),
        'environnement': calculate_environmental_metrics(data),
        'couts': calculate_cost_metrics(data)
    }
