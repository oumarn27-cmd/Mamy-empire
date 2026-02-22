import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Sunu Course | Prix Imbattables", page_icon="💰", layout="wide")

# Algorithme de prix ultra-compétitif (Ajusté pour battre Yango)
if 'base_vtc' not in st.session_state: st.session_state.base_vtc = 1000  # Prise en charge basse
if 'prix_km_dakar' not in st.session_state: st.session_state.prix_km_dakar = 300 # Tarif urbain agressif
if 'prix_km_aibd' not in st.session_state: st.session_state.prix_km_aibd = 350 # Tarif aéroport imbattable

# --- 2. STYLE CSS (MODERNE & PRO) ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: #0b0f19; color: white; }
    .glass-card { 
        background: rgba(255, 255, 255, 0.03); border-radius: 20px; 
        padding: 25px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px;
    }
    .promo-banner {
        background: linear-gradient(90deg, #facc15 0%, #fb923c 100%);
        color: #000; padding: 10px; border-radius: 10px; text-align: center;
        font-weight: bold; margin-bottom: 20px;
    }
    .price-tag { font-size: 50px; color: #10b981; font-weight: 900; text-align: center; }
    .stButton>button { background: #25D366; color: white; border: none; height: 60px; font-weight: bold; border-radius: 15px; width: 100%; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIQUE DE CALCUL DYNAMIQUE ---
def calculer_meilleur_prix(depart, destination, gamme):
    # Simulation de distance intelligente
    dep_u, dest_u = depart.upper(), destination.upper()
    
    if "AIBD" in dest_u or "AÉROPORT" in dest_u or "AIBD" in dep_u:
        dist = 55
        tarif = st.session_state.prix_km_aibd
        frais_autoroute = 3000 # Péage AIBD
    elif "SALY" in dest_u or "MBOUR" in dest_u:
        dist = 85
        tarif = 400
        frais_autoroute = 3000
    else:
        dist = 10 # Trajet moyen intra-Dakar
        tarif = st.session_state.prix_km_dakar
        frais_autoroute = 0

    prix_final = st.session_state.base_vtc + (dist * tarif) + frais_autoroute
    
    # Ajustement Gamme
    if gamme == "Affaire (SUV)": prix_final += 3000
    if gamme == "Luxe (Van)": prix_final += 8000
    
    return int(prix_final)

# --- 4. INTERFACE ---
st.markdown('<div class="promo-banner">🔥 TARIFS 10% MOINS CHERS QUE LA CONCURRENCE - QUALITÉ PREMIUM GARANTIE</div>', unsafe_allow_html=True)

st.title("⚡ Sunu Course Elite")
st.write("Le transport le moins cher de Dakar, le confort en plus.")

col_form, col_visual = st.columns([1.5, 1])

with col_form:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📍 Calculez votre prix abordable")
    
    nom = st.text_input("Nom du passager")
    
    c1, c2 = st.columns(2)
    with c1:
        depart = st.text_input("📍 Ma position (Départ)", placeholder="Ex: HLM 5, Villa...")
        gamme = st.selectbox("Catégorie", ["Standard (Éco)", "Affaire (SUV)", "Luxe (Van)"])
    with c2:
        destination = st.text_input("🏁 Ma destination (Arrivée)", placeholder="Ex: Point E ou AIBD")
        tel = st.text_input("WhatsApp (70 457 64 59)")

    # Calcul en temps réel
    prix_estime = calculer_meilleur_prix(depart, destination, gamme)
    
    st.markdown(f'<div class="price-tag">{prix_estime:,} <small style="font-size:15px">FCFA</small></div>', unsafe_allow_html=True)
    st.caption("✅ Prix fixe (Pas de mauvaise surprise à l'arrivée)")

    if st.button("🚀 COMMANDER AU MEILLEUR PRIX"):
        if nom and depart and destination:
            # Lien GPS pour le chauffeur
            gps = f"https://www.google.com/maps/dir/?api=1&origin={depart.replace(' ','+')}&destination={destination.replace(' ','+')}"
            
            message = (
                f"🚕 *COMMANDE PRIX ABORDABLE*\n\n"
                f"👤 *Client:* {nom}\n"
                f"📍 *Départ:* {depart}\n"
                f"🏁 *Arrivée:* {destination}\n"
                f"🚗 *Gamme:* {gamme}\n"
                f"💰 *PRIX FIXE:* {prix_estime:,} FCFA\n\n"
                f"🗺️ *NAVIGATION GPS:* \n{gps}"
            )
            
            # NUMÉRO FINAL : 70 457 64 59
            wa_url = f"https://wa.me/221704576459?text={message.replace(' ', '%20').replace('\n', '%0A')}"
            st.markdown(f'<a href="{wa_url}" target="_blank"><button>📲 Confirmer sur WhatsApp</button></a>', unsafe_allow_html=True)
        else:
            st.error("Veuillez remplir votre itinéraire.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_visual:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🗺️ Votre Trajet")
    st.markdown('<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d12345!2d-17.44!3d14.72!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sfr!2ssn!4v123456789" width="100%" height="350" style="border:0;"></iframe>', unsafe_allow_html=True)
    st.write("---")
    st.write("✈️ **Radar de Vols Live**")
    if st.button("Ouvrir le Radar AIBD"):
        st.info("Suivez l'avion pour ajuster l'heure de prise en charge.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. PAGE ADMIN (POUR RESTER LE MOINS CHER) ---
st.sidebar.title("🔐 Admin")
admin_pwd = st.sidebar.text_input("Mot de passe", type="password")
if admin_pwd == "Elite221":
    st.sidebar.subheader("Réglage des Tarifs")
    st.session_state.prix_km_dakar = st.sidebar.slider("Prix/KM Dakar", 200, 600, 300)
    st.sidebar.write(f"Tarif actuel: {st.session_state.prix_km_dakar} FCFA/KM")