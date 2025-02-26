import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
from utils.simulation import ProcessSimulator
import pandas as pd

st.set_page_config(page_title="Jumeau Numérique", page_icon="🔄")

# CSS personnalisé pour le design
st.markdown("""
<style>
    .parameter-card {
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

    .timer {
        font-size: 24px;
        font-weight: bold;
        color: #0066cc;
        text-align: center;
        padding: 10px;
        background: #f0f2f6;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def render_digital_twin():
    st.title("🔄 Jumeau Numérique")

    # Initialize session state for timer
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'elapsed_time' not in st.session_state:
        st.session_state.elapsed_time = timedelta()

    # Parameters input in main content area
    st.markdown("<div class='parameter-card'>", unsafe_allow_html=True)
    st.subheader("Paramètres de Simulation")

    col1, col2, col3 = st.columns(3)

    with col1:
        parameters = {
            'temperature': st.number_input("Température (°C)", 100, 200, 150)
        }
    with col2:
        parameters['pressure'] = st.number_input("Pression (bar)", 1.0, 5.0, 2.5)
    with col3:
        parameters['flow_rate'] = st.number_input("Débit (m³/h)", 50, 150, 100)

    col4, col5 = st.columns(2)
    with col4:
        parameters['heat_input'] = st.number_input("Apport de chaleur (kW)", 500, 2000, 1000)
    with col5:
        parameters['inlet_temperature'] = st.number_input("Température d'entrée (°C)", 20, 50, 25)

    st.markdown("</div>", unsafe_allow_html=True)

    # Simulation duration
    duration = st.selectbox(
        "Durée de simulation",
        [1, 2, 4, 8, 12, 24],
        format_func=lambda x: f"{x} heures"
    ) * 3600

    # Initialize simulator
    simulator = ProcessSimulator()

    if st.button("Lancer la Simulation"):
        # Start timer
        if not st.session_state.start_time:
            st.session_state.start_time = datetime.now()

        # Run simulation
        results = simulator.simulate_process(parameters, duration)

        # Display timer
        st.markdown("<div class='timer'>", unsafe_allow_html=True)
        elapsed = datetime.now() - st.session_state.start_time
        st.session_state.elapsed_time = elapsed
        st.write(f"⏱️ Temps écoulé: {elapsed.seconds//3600}h {(elapsed.seconds//60)%60}m {elapsed.seconds%60}s")
        st.markdown("</div>", unsafe_allow_html=True)

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

        # Additional metrics with export option
        st.subheader("Métriques de Performance")
        metrics_df = pd.DataFrame({
            'Métrique': ['Consommation Énergétique', 'Production', 'Efficacité'],
            'Valeur': [
                f"{results['energy_consumption']:.1f} kWh",
                f"{results['product_output']:.1f} m³",
                f"{(results['product_output'] / results['energy_consumption']) * 100:.1f}%"
            ]
        })

        st.dataframe(metrics_df)
        csv = metrics_df.to_csv(index=False)
        st.download_button(
            label="📥 Exporter les métriques (CSV)",
            data=csv,
            file_name=f"simulation_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    render_digital_twin()