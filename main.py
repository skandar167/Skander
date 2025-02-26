import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from utils.data_generator import generate_sample_data
from utils.kpi_calculator import calculate_all_kpis

st.set_page_config(
    page_title="Plateforme d'Optimisation Industrielle",
    page_icon="🏭",
    layout="wide"
)

def main():
    st.title("🏭 Plateforme d'Optimisation Industrielle IA")
    
    # Sidebar for global controls
    st.sidebar.title("Configuration")
    selected_unit = st.sidebar.selectbox(
        "Unité industrielle",
        ["Raffinerie Skikda", "Production Pharmaceutique Constantine"]
    )
    
    # Main dashboard layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Vue d'ensemble des KPIs")
        # Generate sample data
        current_data = generate_sample_data()
        kpis = calculate_all_kpis(current_data)
        
        # Create gauge chart for overall efficiency
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = kpis['performance_energetique']['efficacite_energetique'],
            title = {'text': "Efficacité Globale"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#0066cc"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "gray"},
                    {'range': [75, 100], 'color': "darkgray"}
                ]
            }
        ))
        st.plotly_chart(fig)

    with col2:
        st.subheader("Alertes et Notifications")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.info(f"Dernière mise à jour: {current_time}")
        
        # Sample alerts
        st.warning("⚠️ Rendement matière en dessous du seuil optimal (85%)")
        st.success("✅ Consommation énergétique dans les normes")

    # Quick access to main features
    st.subheader("Accès Rapide")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.button("Analyse des Besoins", on_click=lambda: st.switch_page("pages/01_analyse_besoins.py"))
    with col2:
        st.button("Jumeau Numérique", on_click=lambda: st.switch_page("pages/02_jumeau_numerique.py"))
    with col3:
        st.button("Monitoring KPI", on_click=lambda: st.switch_page("pages/03_kpi_monitoring.py"))
    with col4:
        st.button("Optimisation", on_click=lambda: st.switch_page("pages/04_optimisation.py"))

if __name__ == "__main__":
    main()
