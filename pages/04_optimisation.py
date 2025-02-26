import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils.optimization import optimize_parameters
from utils.simulation import ProcessSimulator
import io
from datetime import datetime

st.set_page_config(page_title="Optimisation", page_icon="⚡")

def render_optimisation():
    st.title("⚡ Optimisation Multi-objectifs")

    # CSS pour le design
    st.markdown("""
    <style>
        .optimization-card {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            animation: fadeIn 0.5s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    """, unsafe_allow_html=True)

    # Paramètres d'optimisation dans la page principale
    st.markdown("<div class='optimization-card'>", unsafe_allow_html=True)
    st.subheader("Paramètres d'Optimisation")

    col1, col2, col3 = st.columns(3)

    with col1:
        quality_weight = st.slider("Qualité", 0.0, 1.0, 0.4,
                                 help="Importance accordée à la qualité du produit")
    with col2:
        yield_weight = st.slider("Rendement", 0.0, 1.0, 0.4,
                               help="Importance accordée au rendement de production")
    with col3:
        energy_weight = st.slider("Énergie", 0.0, 1.0, 0.2,
                                help="Importance accordée à l'efficacité énergétique")

    st.markdown("</div>", unsafe_allow_html=True)

    # Normalize weights
    total_weight = quality_weight + yield_weight + energy_weight
    weights = [
        quality_weight/total_weight,
        yield_weight/total_weight,
        energy_weight/total_weight
    ]

    # Initial conditions
    st.markdown("<div class='optimization-card'>", unsafe_allow_html=True)
    st.subheader("Conditions Initiales")
    col1, col2, col3 = st.columns(3)

    with col1:
        initial_temp = st.number_input("Température (°C)", 100.0, 200.0, 150.0)
    with col2:
        initial_pressure = st.number_input("Pression (bar)", 1.5, 3.5, 2.5)
    with col3:
        initial_flow = st.number_input("Débit (m³/h)", 80.0, 120.0, 100.0)

    st.markdown("</div>", unsafe_allow_html=True)

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

                # Add export buttons
                col1, col2 = st.columns(2)
                with col1:
                    csv = params_comparison.to_csv(index=False)
                    st.download_button(
                        label="📥 Exporter en CSV",
                        data=csv,
                        file_name=f"parametres_optimaux_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )

                with col2:
                    # Export to Excel
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                        params_comparison.to_excel(writer, index=False, sheet_name='Paramètres')
                    excel_data = excel_buffer.getvalue()

                    st.download_button(
                        label="📊 Exporter en Excel",
                        data=excel_data,
                        file_name=f"parametres_optimaux_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

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