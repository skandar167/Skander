import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from utils.data_generator import generate_sample_data
from utils.kpi_calculator import calculate_all_kpis

# Configuration de la page avec thème personnalisé
st.set_page_config(
    page_title="Plateforme d'Optimisation Industrielle",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour les animations et le style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;500;700&display=swap');

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .stButton>button {
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Style personnalisé */
    .main-title {
        font-family: 'Roboto', sans-serif;
        font-weight: 700;
        color: #1E3D59;
        animation: fadeIn 1s ease-in;
    }

    .subtitle {
        color: #666;
        font-family: 'Roboto', sans-serif;
        font-weight: 300;
    }

    .university-info {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 5px solid #0066cc;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # En-tête avec logo et titre
    st.markdown('<h1 class="main-title">🏭 Plateforme d\'Optimisation Industrielle IA</h1>', unsafe_allow_html=True)

    # Information sur l'université
    st.markdown("""
    <div class="university-info">
        <h3>À propos du Projet</h3>
        <p>Développé par les étudiants du Département de Génie des Procédés<br>
        Université Constantine 3 - Salah Boubnider</p>
        <p>Ce projet vise à optimiser les processus industriels grâce à l'intelligence artificielle 
        et la simulation numérique avancée.</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar pour les contrôles globaux
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

        # Export options
        st.subheader("Exporter les Données")
        df_kpis = pd.DataFrame({
            'KPI': ['Efficacité Énergétique', 'Rendement Matière', 'Qualité'],
            'Valeur': [
                kpis['performance_energetique']['efficacite_energetique'],
                kpis['rendement_production']['rendement_matiere'],
                kpis['qualite_production']['taux_conformite']
            ]
        })

        col1, col2 = st.columns(2)
        with col1:
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

        # Sample alerts
        st.warning("⚠️ Rendement matière en dessous du seuil optimal (85%)")
        st.success("✅ Consommation énergétique dans les normes")

    # Description des fonctionnalités
    st.markdown("""
    <div style='margin-top: 30px'>
        <h3>Fonctionnalités Principales</h3>
        <ul>
            <li>Analyse des besoins et collecte des données industrielles</li>
            <li>Simulation et jumeau numérique en temps réel</li>
            <li>Optimisation multi-objectifs des processus</li>
            <li>Monitoring des KPIs et détection d'anomalies</li>
            <li>Export des données et rapports en plusieurs formats</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Quick access to main features with animated buttons
    st.subheader("Accès Rapide")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.button("📊 Analyse des Besoins", key="btn_analyse")
    with col2:
        st.button("🔄 Jumeau Numérique", key="btn_jumeau")
    with col3:
        st.button("📈 Monitoring KPI", key="btn_kpi")
    with col4:
        st.button("⚡ Optimisation", key="btn_opti")

if __name__ == "__main__":
    main()