import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import io
from datetime import datetime
from utils.data_generator import generate_historical_data
from utils.kpi_calculator import calculate_all_kpis

st.set_page_config(page_title="Monitoring KPI", page_icon="📈")

def export_kpi_data(kpi_data, category):
    """Export KPI data to Excel with multiple sheets"""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Données brutes
        kpi_data.to_excel(writer, sheet_name='Données brutes', index=False)

        # Statistiques
        stats = kpi_data.describe()
        stats.to_excel(writer, sheet_name='Statistiques')

        # Dernière valeur
        latest = kpi_data.iloc[-1:].T
        latest.to_excel(writer, sheet_name='Dernier relevé')

    return buffer.getvalue()

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

        # Export data
        excel_data = export_kpi_data(energy_data, "Performance_Energetique")
        st.download_button(
            label="📊 Exporter en Excel",
            data=excel_data,
            file_name=f"performance_energetique_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with tabs[1]:
        st.subheader("Rendement Production")

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

        excel_data = export_kpi_data(prod_data, "Rendement_Production")
        st.download_button(
            label="📊 Exporter en Excel",
            data=excel_data,
            file_name=f"rendement_production_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with tabs[2]:
        st.subheader("Qualité Production")

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

        excel_data = export_kpi_data(quality_data, "Qualite_Production")
        st.download_button(
            label="📊 Exporter en Excel",
            data=excel_data,
            file_name=f"qualite_production_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with tabs[3]:
        st.subheader("Maintenance")

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

        excel_data = export_kpi_data(maint_data, "Maintenance")
        st.download_button(
            label="📊 Exporter en Excel",
            data=excel_data,
            file_name=f"maintenance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with tabs[4]:
        st.subheader("Environnement")

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

        excel_data = export_kpi_data(env_data, "Environnement")
        st.download_button(
            label="📊 Exporter en Excel",
            data=excel_data,
            file_name=f"environnement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with tabs[5]:
        st.subheader("Coûts")

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

        excel_data = export_kpi_data(cost_data, "Coûts")
        st.download_button(
            label="📊 Exporter en Excel",
            data=excel_data,
            file_name=f"couts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Export global
    st.subheader("Export Global des KPIs")

    # Prepare global export
    all_data = pd.DataFrame([
        {
            'timestamp': kpi['timestamp'],
            'efficacite_energetique': kpi['performance_energetique']['efficacite_energetique'],
            'rendement_matiere': kpi['rendement_production']['rendement_matiere'],
            'qualite': kpi['qualite_production']['taux_conformite'],
            'maintenance_mtbf': kpi['maintenance']['mtbf'],
            'emissions_co2': kpi['environnement']['emissions_co2'],
            'cout_unitaire': kpi['couts']['cout_unitaire']
        }
        for kpi in kpis_over_time
    ])

    # Export all data
    excel_data = export_kpi_data(all_data, "Tous_les_KPIs")
    st.download_button(
        label="📊 Exporter tous les KPIs",
        data=excel_data,
        file_name=f"tous_les_kpis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    render_kpi_monitoring()