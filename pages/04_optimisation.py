import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils.optimization import optimize_parameters
from utils.simulation import ProcessSimulator

st.set_page_config(page_title="Optimisation", page_icon="⚡")

def render_optimisation():
    st.title("⚡ Optimisation Multi-objectifs")
    
    # Optimization parameters
    st.sidebar.subheader("Paramètres d'Optimisation")
    
    # Objective weights
    st.sidebar.write("Poids des Objectifs")
    quality_weight = st.sidebar.slider("Qualité", 0.0, 1.0, 0.4)
    yield_weight = st.sidebar.slider("Rendement", 0.0, 1.0, 0.4)
    energy_weight = st.sidebar.slider("Énergie", 0.0, 1.0, 0.2)
    
    # Normalize weights
    total_weight = quality_weight + yield_weight + energy_weight
    weights = [
        quality_weight/total_weight,
        yield_weight/total_weight,
        energy_weight/total_weight
    ]
    
    # Initial conditions
    st.subheader("Conditions Initiales")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        initial_temp = st.number_input("Température (°C)", 100.0, 200.0, 150.0)
    with col2:
        initial_pressure = st.number_input("Pression (bar)", 1.5, 3.5, 2.5)
    with col3:
        initial_flow = st.number_input("Débit (m³/h)", 80.0, 120.0, 100.0)
    
    initial_guess = [initial_temp, initial_pressure, initial_flow]
    
    if st.button("Optimiser"):
        # Run optimization
        result = optimize_parameters(initial_guess, weights)
        
        if result['success']:
            st.success("Optimisation réussie!")
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Paramètres Optimaux")
                
                # Parameters comparison
                params_comparison = pd.DataFrame({
                    'Paramètre': ['Température', 'Pression', 'Débit'],
                    'Initial': initial_guess,
                    'Optimal': [
                        result['optimal_parameters']['temperature'],
                        result['optimal_parameters']['pressure'],
                        result['optimal_parameters']['flow_rate']
                    ]
                })
                
                fig = go.Figure(data=[
                    go.Bar(name='Initial', x=params_comparison['Paramètre'], y=params_comparison['Initial']),
                    go.Bar(name='Optimal', x=params_comparison['Paramètre'], y=params_comparison['Optimal'])
                ])
                fig.update_layout(barmode='group', title="Comparaison des Paramètres")
                st.plotly_chart(fig)
            
            with col2:
                st.subheader("Performance Prédite")
                
                # Simulate with optimal parameters
                simulator = ProcessSimulator()
                optimal_simulation = simulator.simulate_process(result['optimal_parameters'])
                optimal_kpis = simulator.predict_kpis(optimal_simulation)
                
                # Display KPIs
                for kpi_name, value in optimal_kpis.items():
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = value,
                        title = {'text': kpi_name.replace('_', ' ').title()},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "#0066cc"},
                            'steps': [
                                {'range': [0, 60], 'color': "lightgray"},
                                {'range': [60, 80], 'color': "gray"},
                                {'range': [80, 100], 'color': "darkgray"}
                            ]
                        }
                    ))
                    fig.update_layout(height=200)
                    st.plotly_chart(fig)
        
        else:
            st.error("L'optimisation n'a pas convergé. Veuillez ajuster les paramètres initiaux.")

if __name__ == "__main__":
    render_optimisation()
