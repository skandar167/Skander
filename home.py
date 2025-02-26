import streamlit as st

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
</style>
""", unsafe_allow_html=True)

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
