import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analyse des Besoins", page_icon="📊")

def render_analyse_besoins():
    st.title("📊 Analyse des Besoins et Collecte des Données")
    
    # Industry selection
    industry_type = st.selectbox(
        "Sélectionner l'industrie",
        ["Raffinerie de Skikda", "Production Pharmaceutique Constantine"]
    )
    
    # Tabs for different analysis aspects
    tab1, tab2, tab3, tab4 = st.tabs([
        "Identification des Besoins",
        "Collecte des Données",
        "Contraintes",
        "KPIs"
    ])
    
    with tab1:
        st.subheader("Identification des Besoins")
        
        # Industry-specific needs
        needs = {
            "Raffinerie de Skikda": [
                "Optimisation de la consommation énergétique",
                "Réduction des émissions",
                "Amélioration du rendement de production",
                "Maintenance prédictive"
            ],
            "Production Pharmaceutique Constantine": [
                "Contrôle qualité",
                "Traçabilité des lots",
                "Optimisation des cycles de production",
                "Gestion des stocks"
            ]
        }
        
        for need in needs[industry_type]:
            st.checkbox(need, value=True)
            
    with tab2:
        st.subheader("Collecte des Données")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Sources de Données")
            data_sources = [
                "Capteurs IoT",
                "Historique de production",
                "Rapports de maintenance",
                "Données de qualité"
            ]
            for source in data_sources:
                st.checkbox(source, value=True)
                
        with col2:
            st.write("Fréquence de Collecte")
            st.selectbox(
                "Fréquence",
                ["Temps réel", "Horaire", "Quotidien", "Hebdomadaire"]
            )
            
    with tab3:
        st.subheader("Contraintes Technico-économiques")
        
        # Sample constraints visualization
        constraints_data = pd.DataFrame({
            'Contrainte': ['Budget', 'Temps', 'Ressources', 'Technique'],
            'Niveau': [80, 60, 70, 90]
        })
        
        fig = px.bar(constraints_data, x='Contrainte', y='Niveau',
                    title="Niveau de Contraintes",
                    color='Niveau',
                    color_continuous_scale='Viridis')
        st.plotly_chart(fig)
        
    with tab4:
        st.subheader("Sélection des KPIs")
        
        # KPI categories
        kpi_categories = {
            "Performance Énergétique": ["Efficacité énergétique", "Consommation par unité"],
            "Production": ["Rendement matière", "Temps de cycle"],
            "Qualité": ["Taux de conformité", "Taux de déchets"],
            "Maintenance": ["MTBF", "MTTR"],
            "Environnement": ["Émissions CO2", "Consommation d'eau"],
            "Coûts": ["Coût unitaire", "Coût énergétique"]
        }
        
        for category, kpis in kpi_categories.items():
            st.write(f"**{category}**")
            for kpi in kpis:
                st.checkbox(kpi, value=True)

if __name__ == "__main__":
    render_analyse_besoins()
