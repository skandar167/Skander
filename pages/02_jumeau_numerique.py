import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.simulation import ProcessSimulator

st.set_page_config(page_title="Jumeau Numérique", page_icon="🔄")

def render_digital_twin():
    st.title("🔄 Jumeau Numérique")
    
    # Initialize simulator
    simulator = ProcessSimulator()
    
    # Parameters input
    st.sidebar.subheader("Paramètres de Simulation")
    
    parameters = {
        'temperature': st.sidebar.slider("Température (°C)", 100, 200, 150),
        'pressure': st.sidebar.slider("Pression (bar)", 1.0, 5.0, 2.5),
        'flow_rate': st.sidebar.slider("Débit (m³/h)", 50, 150, 100),
        'heat_input': st.sidebar.slider("Apport de chaleur (kW)", 500, 2000, 1000),
        'inlet_temperature': st.sidebar.slider("Température d'entrée (°C)", 20, 50, 25)
    }
    
    # Simulation duration
    duration = st.sidebar.selectbox(
        "Durée de simulation",
        [1, 2, 4, 8, 12, 24],
        format_func=lambda x: f"{x} heures"
    ) * 3600
    
    if st.sidebar.button("Lancer la Simulation"):
        # Run simulation
        results = simulator.simulate_process(parameters, duration)
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            # Temperature evolution
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(
                x=results['time']/3600,
                y=results['temperature'],
                name="Température"
            ))
            fig_temp.update_layout(
                title="Évolution de la Température",
                xaxis_title="Temps (heures)",
                yaxis_title="Température (°C)"
            )
            st.plotly_chart(fig_temp)
        
        with col2:
            # KPI predictions
            kpis = simulator.predict_kpis(results)
            
            # KPI gauges
            for kpi_name, value in kpis.items():
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
        
        # Additional metrics
        st.subheader("Métriques de Performance")
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        
        with metrics_col1:
            st.metric(
                "Consommation Énergétique",
                f"{results['energy_consumption']:.1f} kWh"
            )
        
        with metrics_col2:
            st.metric(
                "Production",
                f"{results['product_output']:.1f} m³"
            )
        
        with metrics_col3:
            efficiency = (results['product_output'] / results['energy_consumption']) * 100
            st.metric(
                "Efficacité",
                f"{efficiency:.1f}%"
            )

if __name__ == "__main__":
    render_digital_twin()
