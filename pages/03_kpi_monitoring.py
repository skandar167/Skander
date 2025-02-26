import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_generator import generate_historical_data
from utils.kpi_calculator import calculate_all_kpis

st.set_page_config(page_title="Monitoring KPI", page_icon="📈")

def render_kpi_monitoring():
    st.title("📈 Monitoring des KPI")
    
    # Get historical data
    historical_data = generate_historical_data(30)  # 30 days of data
    
    # Convert to DataFrame
    df = pd.DataFrame(historical_data)
    
    # Calculate KPIs for each timestamp
    kpis_over_time = []
    for _, row in df.iterrows():
        kpis = calculate_all_kpis(row)
        kpis['timestamp'] = row['timestamp']
        kpis_over_time.append(kpis)
    
    # Create tabs for different KPI categories
    tabs = st.tabs([
        "Performance Énergétique",
        "Rendement Production",
        "Qualité Production",
        "Maintenance",
        "Environnement",
        "Coûts"
    ])
    
    with tabs[0]:
        st.subheader("Performance Énergétique")
        
        # Energy efficiency trend
        energy_data = pd.DataFrame([
            {
                'timestamp': kpi['timestamp'],
                'efficacite': kpi['performance_energetique']['efficacite_energetique'],
                'consommation': kpi['performance_energetique']['consommation_unitaire']
            }
            for kpi in kpis_over_time
        ])
        
        fig = px.line(energy_data, x='timestamp', y=['efficacite', 'consommation'],
                     title="Évolution de la Performance Énergétique")
        st.plotly_chart(fig)
    
    with tabs[1]:
        st.subheader("Rendement Production")
        
        # Production yield trend
        prod_data = pd.DataFrame([
            {
                'timestamp': kpi['timestamp'],
                'rendement': kpi['rendement_production']['rendement_matiere'],
                'productivite': kpi['rendement_production']['productivite']
            }
            for kpi in kpis_over_time
        ])
        
        fig = px.line(prod_data, x='timestamp', y=['rendement', 'productivite'],
                     title="Évolution du Rendement de Production")
        st.plotly_chart(fig)
    
    with tabs[2]:
        st.subheader("Qualité Production")
        
        # Quality metrics trend
        quality_data = pd.DataFrame([
            {
                'timestamp': kpi['timestamp'],
                'conformite': kpi['qualite_production']['taux_conformite'],
                'dechets': kpi['qualite_production']['taux_dechets']
            }
            for kpi in kpis_over_time
        ])
        
        fig = px.line(quality_data, x='timestamp', y=['conformite', 'dechets'],
                     title="Évolution des Métriques de Qualité")
        st.plotly_chart(fig)
    
    with tabs[3]:
        st.subheader("Maintenance")
        
        # Maintenance metrics trend
        maint_data = pd.DataFrame([
            {
                'timestamp': kpi['timestamp'],
                'MTBF': kpi['maintenance']['mtbf'],
                'MTTR': kpi['maintenance']['mttr']
            }
            for kpi in kpis_over_time
        ])
        
        fig = px.line(maint_data, x='timestamp', y=['MTBF', 'MTTR'],
                     title="Évolution des Métriques de Maintenance")
        st.plotly_chart(fig)
    
    with tabs[4]:
        st.subheader("Environnement")
        
        # Environmental metrics trend
        env_data = pd.DataFrame([
            {
                'timestamp': kpi['timestamp'],
                'emissions_CO2': kpi['environnement']['emissions_co2'],
                'cons_eau': kpi['environnement']['consommation_eau']
            }
            for kpi in kpis_over_time
        ])
        
        fig = px.line(env_data, x='timestamp', y=['emissions_CO2', 'cons_eau'],
                     title="Évolution des Métriques Environnementales")
        st.plotly_chart(fig)
    
    with tabs[5]:
        st.subheader("Coûts")
        
        # Cost metrics trend
        cost_data = pd.DataFrame([
            {
                'timestamp': kpi['timestamp'],
                'cout_unitaire': kpi['couts']['cout_unitaire'],
                'cout_energetique': kpi['couts']['cout_energetique']
            }
            for kpi in kpis_over_time
        ])
        
        fig = px.line(cost_data, x='timestamp', y=['cout_unitaire', 'cout_energetique'],
                     title="Évolution des Coûts")
        st.plotly_chart(fig)

if __name__ == "__main__":
    render_kpi_monitoring()
