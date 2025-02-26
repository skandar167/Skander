import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io

st.set_page_config(page_title="Analyse des Besoins", page_icon="📊")

# Initialize session state for custom industries if not already done in home.py
if 'custom_industries' not in st.session_state:
    st.session_state.custom_industries = {
        'Pétrole et Gaz': {},
        'Agroalimentaire': {},
        'Pharmaceutique': {}
    }

def save_configuration(selected_industry, selected_unit, selected_needs, selected_sources, selected_frequency, selected_kpis):
    """Sauvegarder la configuration actuelle"""
    config_data = {
        'industry_type': selected_industry,
        'unit': selected_unit,
        'needs': ', '.join(selected_needs),
        'data_sources': ', '.join(selected_sources),
        'frequency': selected_frequency,
        'kpis': ', '.join(selected_kpis),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Convert to DataFrame for export
    df = pd.DataFrame([config_data])
    return df

def add_new_unit(industry_type, unit_name, unit_details):
    """Ajouter une nouvelle unité avec ses détails"""
    if industry_type not in st.session_state.custom_industries:
        st.session_state.custom_industries[industry_type] = {}

    st.session_state.custom_industries[industry_type][unit_name] = {
        **unit_details,
        'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def render_analyse_besoins():
    st.title("📊 Analyse des Besoins et Collecte des Données")

    # Industry selection
    col1, col2 = st.columns(2)

    with col1:
        selected_industry = st.selectbox(
            "Type d'Industrie",
            ["Pétrole et Gaz", "Agroalimentaire", "Pharmaceutique"]
        )

    with col2:
        # Combine default and custom units
        default_units = {
            "Pétrole et Gaz": ["Raffinerie Skikda", "Terminal GNL Arzew", "Hassi R'Mel"],
            "Agroalimentaire": ["Cevital Béjaïa", "Groupe Amor Benamor", "Candia Algérie"],
            "Pharmaceutique": ["Saidal Constantine", "Biopharm", "LPA Production"]
        }

        custom_units = list(st.session_state.custom_industries.get(selected_industry, {}).keys())
        all_units = default_units[selected_industry] + custom_units

        selected_unit = st.selectbox(
            "Unité Industrielle",
            all_units
        )

    # Add new unit
    with st.expander("Ajouter une nouvelle unité"):
        with st.form("new_unit_form"):
            new_unit_name = st.text_input("Nom de l'unité")
            new_unit_address = st.text_input("Adresse")
            new_unit_capacity = st.number_input("Capacité de production (tonnes/jour)", min_value=0.0)
            new_unit_employees = st.number_input("Nombre d'employés", min_value=0)
            new_unit_certification = st.multiselect(
                "Certifications",
                ["ISO 9001", "ISO 14001", "OHSAS 18001", "GMP", "HACCP"]
            )
            new_unit_description = st.text_area("Description de l'unité")

            submitted = st.form_submit_button("Ajouter l'unité")
            if submitted and new_unit_name:
                unit_details = {
                    'address': new_unit_address,
                    'capacity': new_unit_capacity,
                    'employees': new_unit_employees,
                    'certifications': new_unit_certification,
                    'description': new_unit_description
                }
                add_new_unit(selected_industry, new_unit_name, unit_details)
                st.success(f"Unité '{new_unit_name}' ajoutée avec succès!")
                st.rerun()

    # Rest of the analysis tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Identification des Besoins",
        "Collecte des Données",
        "Contraintes",
        "KPIs"
    ])

    selected_needs = []
    selected_sources = []
    selected_frequency = None
    selected_kpis = []

    with tab1:
        st.subheader("Identification des Besoins")

        # Industry-specific needs
        needs = {
            "Pétrole et Gaz": [
                "Optimisation de la consommation énergétique",
                "Réduction des émissions",
                "Amélioration du rendement de production",
                "Maintenance prédictive"
            ],
            "Agroalimentaire": [
                "Contrôle qualité",
                "Traçabilité des lots",
                "Optimisation des cycles de production",
                "Gestion des stocks"
            ],
            "Pharmaceutique": [
                "Contrôle qualité",
                "Traçabilité des lots",
                "Optimisation des cycles de production",
                "Gestion des stocks"
            ]
        }

        for need in needs[selected_industry]:
            if st.checkbox(need, key=f"need_{need}"):
                selected_needs.append(need)

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
                if st.checkbox(source, key=f"source_{source}"):
                    selected_sources.append(source)

        with col2:
            st.write("Fréquence de Collecte")
            selected_frequency = st.selectbox(
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
                if st.checkbox(kpi, key=f"kpi_{kpi}"):
                    selected_kpis.append(kpi)

    # Save configuration
    st.subheader("Sauvegarder la Configuration")
    if st.button("💾 Sauvegarder les modifications"):
        config_df = save_configuration(
            selected_industry,
            selected_unit,
            selected_needs,
            selected_sources,
            selected_frequency,
            selected_kpis
        )

        # Export options
        col1, col2 = st.columns(2)
        with col1:
            csv = config_df.to_csv(index=False)
            st.download_button(
                label="📥 Exporter en CSV",
                data=csv,
                file_name=f"configuration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        with col2:
            # Convert to Excel
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                config_df.to_excel(writer, index=False, sheet_name='Configuration')
            excel_data = excel_buffer.getvalue()

            st.download_button(
                label="📊 Exporter en Excel",
                data=excel_data,
                file_name=f"configuration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        st.success("Configuration sauvegardée avec succès!")

if __name__ == "__main__":
    render_analyse_besoins()