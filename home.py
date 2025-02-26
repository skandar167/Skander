import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Sélection de l'Industrie",
    page_icon="🏭",
    layout="wide"
)

# CSS personnalisé pour les animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;500;700&display=swap');

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .industry-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        margin: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        animation: fadeIn 0.5s ease-out;
    }

    .industry-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }

    .main-title {
        font-family: 'Roboto', sans-serif;
        font-weight: 700;
        color: #1E3D59;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-in;
    }

    .university-info {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 5px solid #0066cc;
        animation: fadeIn 1s ease-in;
    }

    .form-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for custom industries and their details
if 'custom_industries' not in st.session_state:
    st.session_state.custom_industries = {
        'Pétrole et Gaz': {},
        'Agroalimentaire': {},
        'Pharmaceutique': {}
    }

# Titre principal
st.markdown('<h1 class="main-title">🏭 Plateforme d\'Optimisation Industrielle IA</h1>', unsafe_allow_html=True)

# Information sur l'université
st.markdown("""
<div class="university-info">
    <h3>À propos du Projet</h3>
    <p>Développé par les étudiants du Département de Génie des Procédés<br>
    Université Constantine 3 - Salah Boubnider</p>
    <p>Ce projet utilise l'intelligence artificielle et la simulation numérique pour optimiser 
    les processus industriels dans différents secteurs.</p>
</div>
""", unsafe_allow_html=True)

# Sélection de l'industrie
st.markdown("### Sélectionnez votre Secteur Industriel")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="industry-card" onclick="handleClick('petrol')">
        <h3>🛢️ Pétrole et Gaz</h3>
        <p>Optimisation des processus de raffinage et de production</p>
        <ul>
            <li>Raffinerie de Skikda</li>
            <li>Terminal GNL Arzew</li>
            <li>Hassi R'Mel</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Sélectionner Pétrole et Gaz"):
        st.session_state['industry_type'] = 'petrol'
        st.switch_page("pages/main_dashboard.py")

with col2:
    st.markdown("""
    <div class="industry-card" onclick="handleClick('agro')">
        <h3>🌾 Agroalimentaire</h3>
        <p>Gestion de la production alimentaire</p>
        <ul>
            <li>Cevital Béjaïa</li>
            <li>Groupe Amor Benamor</li>
            <li>Candia Algérie</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Sélectionner Agroalimentaire"):
        st.session_state['industry_type'] = 'agro'
        st.switch_page("pages/main_dashboard.py")

with col3:
    st.markdown("""
    <div class="industry-card" onclick="handleClick('pharma')">
        <h3>💊 Pharmaceutique</h3>
        <p>Production et contrôle qualité pharmaceutique</p>
        <ul>
            <li>Saidal Constantine</li>
            <li>Biopharm</li>
            <li>LPA Production</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Sélectionner Pharmaceutique"):
        st.session_state['industry_type'] = 'pharma'
        st.switch_page("pages/main_dashboard.py")

# Add new unit
st.markdown("### Ajouter une Nouvelle Unité")
with st.expander("Cliquez pour ajouter une nouvelle unité"):
    selected_industry_type = st.selectbox(
        "Type d'Industrie",
        ["Pétrole et Gaz", "Agroalimentaire", "Pharmaceutique"]
    )

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
            # Save unit details
            st.session_state.custom_industries[selected_industry_type][new_unit_name] = {
                'address': new_unit_address,
                'capacity': new_unit_capacity,
                'employees': new_unit_employees,
                'certifications': new_unit_certification,
                'description': new_unit_description,
                'date_added': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.success(f"Unité '{new_unit_name}' ajoutée avec succès!")

# Display existing custom units
if any(units for units in st.session_state.custom_industries.values()):
    st.markdown("### Unités Personnalisées")
    for industry, units in st.session_state.custom_industries.items():
        if units:
            st.subheader(industry)
            for unit_name, details in units.items():
                with st.expander(f"{unit_name}"):
                    st.write(f"**Adresse:** {details['address']}")
                    st.write(f"**Capacité:** {details['capacity']} tonnes/jour")
                    st.write(f"**Employés:** {details['employees']}")
                    st.write(f"**Certifications:** {', '.join(details['certifications'])}")
                    st.write(f"**Description:** {details['description']}")
                    st.write(f"**Date d'ajout:** {details['date_added']}")