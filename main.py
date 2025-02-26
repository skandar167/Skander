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
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
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

    .config-section {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        animation: slideIn 0.5s ease-out;
    }

    .university-info {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 5px solid #0066cc;
        animation: fadeIn 1s ease-in;
    }
</style>
""", unsafe_allow_html=True)

def get_industry_kpis(industry_type):
    """Retourne les KPIs spécifiques à chaque industrie"""
    kpis = {
        "Pétrole et Gaz": {
            "performance_energetique": ["Efficacité énergétique", "Consommation par baril"],
            "environnement": ["Émissions CO2", "Gestion des effluents"],
            "production": ["Taux de récupération", "Qualité du produit"]
        },
        "Agroalimentaire": {
            "qualite": ["Conformité aux normes alimentaires", "Traçabilité"],
            "production": ["Rendement de production", "Gestion des stocks"],
            "environnement": ["Consommation d'eau", "Gestion des déchets"]
        },
        "Pharmaceutique": {
            "qualite": ["Conformité GMP", "Pureté du produit"],
            "production": ["Rendement par lot", "Temps de cycle"],
            "controle": ["Tests de qualité", "Validation des processus"]
        }
    }
    return kpis.get(industry_type, {})

def main():
    # En-tête avec logo et titre
    st.markdown('<h1 class="main-title">🏭 Plateforme d\'Optimisation Industrielle IA</h1>', unsafe_allow_html=True)

    # Configuration en haut de page
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    config_col1, config_col2 = st.columns(2)

    with config_col1:
        selected_industry = st.selectbox(
            "Type d'Industrie",
            ["Pétrole et Gaz", "Agroalimentaire", "Pharmaceutique"]
        )

    with config_col2:
        if selected_industry == "Pétrole et Gaz":
            selected_unit = st.selectbox(
                "Unité industrielle",
                ["Raffinerie Skikda", "Terminal GNL Arzew", "Hassi R'Mel"]
            )
        elif selected_industry == "Agroalimentaire":
            selected_unit = st.selectbox(
                "Unité industrielle",
                ["Cevital Béjaïa", "Groupe Amor Benamor", "Candia Algérie"]
            )
        else:
            selected_unit = st.selectbox(
                "Unité industrielle",
                ["Saidal Constantine", "Biopharm", "LPA Production"]
            )
    st.markdown('</div>', unsafe_allow_html=True)

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

    # Main dashboard layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Vue d'ensemble des KPIs")

        # Generate sample data and get industry-specific KPIs
        current_data = generate_sample_data()
        kpis = calculate_all_kpis(current_data)
        industry_kpis = get_industry_kpis(selected_industry)

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

        # Sample alerts based on industry
        if selected_industry == "Pétrole et Gaz":
            st.warning("⚠️ Pression du système au-dessus du seuil normal")
            st.success("✅ Qualité du produit conforme aux spécifications")
        elif selected_industry == "Agroalimentaire":
            st.warning("⚠️ Température de stockage proche de la limite")
            st.success("✅ Traçabilité des lots validée")
        else:
            st.warning("⚠️ Maintenance préventive requise sur ligne 2")
            st.success("✅ Tests de qualité conformes aux normes GMP")

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

if __name__ == "__main__":
    main()