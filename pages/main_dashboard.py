import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from utils.data_generator import generate_sample_data
from utils.kpi_calculator import calculate_all_kpis

# Configuration de la page
st.set_page_config(
    page_title="Tableau de Bord Principal",
    page_icon="📊",
    layout="wide"
)

# Verify industry type is selected
if 'industry_type' not in st.session_state:
    st.switch_page("home.py")

def get_industry_info(industry_type):
    """Retourne les informations spécifiques à chaque industrie"""
    if industry_type == 'petrol':
        return {
            'title': "Pétrole et Gaz",
            'units': ["Raffinerie Skikda", "Terminal GNL Arzew", "Hassi R'Mel"],
            'kpis': {
                'performance': ["Efficacité énergétique", "Consommation par baril"],
                'environnement': ["Émissions CO2", "Gestion des effluents"],
                'production': ["Taux de récupération", "Qualité du produit"]
            }
        }
    elif industry_type == 'agro':
        return {
            'title': "Agroalimentaire",
            'units': ["Cevital Béjaïa", "Groupe Amor Benamor", "Candia Algérie"],
            'kpis': {
                'qualite': ["Conformité alimentaire", "Traçabilité"],
                'production': ["Rendement de production", "Gestion des stocks"],
                'environnement': ["Consommation d'eau", "Gestion des déchets"]
            }
        }
    else:  # pharma
        return {
            'title': "Pharmaceutique",
            'units': ["Saidal Constantine", "Biopharm", "LPA Production"],
            'kpis': {
                'qualite': ["Conformité GMP", "Pureté du produit"],
                'production': ["Rendement par lot", "Temps de cycle"],
                'controle': ["Tests de qualité", "Validation des processus"]
            }
        }

# Get industry specific information
industry_info = get_industry_info(st.session_state.industry_type)

# Main dashboard content
st.title(f"📊 Tableau de Bord - {industry_info['title']}")

# Unit selection
selected_unit = st.selectbox(
    "Sélectionner l'unité",
    industry_info['units']
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
        mode="gauge+number",
        value=kpis['performance_energetique']['efficacite_energetique'],
        title={'text': "Efficacité Globale"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#0066cc"},
            'steps': [
                {'range': [0, 60], 'color': "lightgray"},
                {'range': [60, 80], 'color': "gray"},
                {'range': [80, 100], 'color': "darkgray"}
            ]
        }
    ))
    st.plotly_chart(fig)

    # Export options
    st.subheader("Exporter les Données")
    df_kpis = pd.DataFrame({
        'KPI': list(industry_info['kpis'].keys()),
        'Valeur': [85, 92, 78]  # Example values
    })
    
    csv = df_kpis.to_csv(index=False)
    st.download_button(
        label="📥 Exporter en CSV",
        data=csv,
        file_name=f"kpis_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col2:
    st.subheader("Alertes et Notifications")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.info(f"Dernière mise à jour: {current_time}")
    
    # Industry-specific alerts
    if st.session_state.industry_type == 'petrol':
        st.warning("⚠️ Pression du système au-dessus du seuil normal")
        st.success("✅ Qualité du produit conforme aux spécifications")
    elif st.session_state.industry_type == 'agro':
        st.warning("⚠️ Température de stockage proche de la limite")
        st.success("✅ Traçabilité des lots validée")
    else:
        st.warning("⚠️ Maintenance préventive requise sur ligne 2")
        st.success("✅ Tests de qualité conformes aux normes GMP")

# Navigation
st.subheader("Navigation")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 Analyse des Besoins"):
        st.switch_page("pages/01_analyse_besoins.py")
with col2:
    if st.button("🔄 Jumeau Numérique"):
        st.switch_page("pages/02_jumeau_numerique.py")
with col3:
    if st.button("📈 Monitoring KPI"):
        st.switch_page("pages/03_kpi_monitoring.py")
with col4:
    if st.button("⚡ Optimisation"):
        st.switch_page("pages/04_optimisation.py")
