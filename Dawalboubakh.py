import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Sunu Course | Tarifs dès 500F", page_icon="🚕", layout="wide")

# Paramètres de calcul ajustés (Style Yango/Course de quartier)
if 'tarif_base' not in st.session_state: st.session_state.tarif_base = 500  # Prise en charge minimale
if 'tarif_km' not in st.session_state: st.session_state.tarif_km = 300       # Prix par KM ultra bas
if 'tarif_min' not in st.session_state: st.session_state.tarif_min = 500     # Le prix ne descend jamais sous 500

# --- 2. STYLE CSS ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: #0b0f19; color: white; }
    .glass-card { 
        background: rgba(255, 255, 255, 0.03); border-radius: 20px; 
        padding: 25px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px;
    }
    .promo-header {
        background: #10b981; color: white; padding: 10px; border-radius: 10px;
        text-align: center; font-weight: bold; margin-bottom: 15px;
    }
    .price-tag { font-size: 55px; color: #10b981; font-weight: 900; text-align: center; }
    .stButton>button { background: #25D366; color: white; border: none; height: 60px; font-weight: bold; border-radius: 15px; width: 100%; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FONCTION DE CALCUL DYNAMIQUE ---
def calculer_prix_ultra_abordable(distance_km, gamme):
    # Formule : 500 + (Distance x 300)
    total = st.session_state.tarif_base + (distance_km * st.session_state.tarif_km)
    
    # Options de confort
    if gamme == "Affaire (SUV)": total += 2000
    if gamme == "Luxe (Van)": total += 5000
    
    # Frais d'autoroute si trajet vers l'extérieur
    if distance_km > 30:
        total += 3000
        
    return int(max(total, st.session_state.tarif_min))

# --- 4. INTERFACE ---
st.markdown('<div class="promo-header">🚀 LES PRIX LES MOINS CHERS DE DAKAR : DÈS 500 FCFA !</div>', unsafe_allow_html=True)

st.title("⚡ Sunu Course Elite")
st.write("Votre trajet calculé sur mesure au meilleur prix du marché.")

col_form, col_map = st.columns([1.5, 1])

with col_form:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📍 Calculez votre trajet")
    
    nom = st.text_input("Nom du passager")
    
    c1, c2 = st.columns(2)
    with c1:
        depart = st.text_input("📍 Départ", placeholder="Votre position actuelle")
        gamme = st.selectbox("Véhicule", ["Standard (Éco)", "Affaire (SUV)", "Luxe (Van)"])
    with c2:
        destination = st.text_input("🏁 Arrivée", placeholder="Où allez-vous ?")
        tel = st.text_input("WhatsApp (70 457 64 59)")

    # --- ESTIMATION DE LA DISTANCE ---
    dist_estimee = 5 # Par défaut courte distance
    dest_u = (depart + destination).upper()
    if "AIBD" in dest_u: dist_estimee = 55
    elif "SALY" in dest_u: dist_estimee = 85
    elif "DIAMNIADIO" in dest_u: dist_estimee = 35
    elif "PLATEAU" in dest_u and "ALMADIES" in dest_u: dist_estimee = 18
    
    prix_final = calculer_prix_ultra_abordable(dist_estimee, gamme)
    
    st.markdown(f'<div class="price-tag">{prix_final:,} <small style="font-size:18px">FCFA</small></div>', unsafe_allow_html=True)
    st.caption(f"📏 Distance estimée : ~{dist_estimee} km | Tarif basé sur l'itinéraire")

    if st.button("🚀 RÉSERVER MAINTENANT"):
        if nom and depart and destination:
            # Itinéraire GPS pour le chauffeur
            gps = f"https://www.google.com/maps/dir/?api=1&origin={depart.replace(' ','+')}&destination={destination.replace(' ','+')}&travelmode=driving"
            
            # Position en direct du client (Lien pour que le client partage sa position)
            partage_pos = "https://www.google.com/maps/search/?api=1&query=Ma+Position"

            message = (
                f"🚕 *COMMANDE SUNU COURSE (PRIX MINI)*\n\n"
                f"👤 *Client:* {nom}\n"
                f"📍 *Départ:* {depart}\n"
                f"🏁 *Arrivée:* {destination}\n"
                f"💰 *PRIX CALCULÉ:* {prix_final:,} FCFA\n\n"
                f"🧭 *GPS CHAUFFEUR:* \n{gps}\n\n"
                f"📍 *POSITION CLIENT:* \n{partage_pos}"
            )
            
            # TON NUMÉRO : 70 457 64 59
            wa_url = f"https://wa.me/221704576459?text={message.replace(' ', '%20').replace('\n', '%0A')}"
            st.markdown(f'<a href="{wa_url}" target="_blank"><button>📲 Envoyer au chauffeur</button></a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_map:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🗺️ Carte du trajet")
    st.markdown('<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d123445.!2d-17.4!3d14.7!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sfr!2ssn!4v1" width="100%" height="450" style="border:0;"></iframe>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. ADMIN ---
st.sidebar.title("🔐 Admin")
if st.sidebar.text_input("Pass", type="password") == "Elite221":
    st.session_state.tarif_base = st.sidebar.number_input("Base (Prix mini)", value=st.session_state.tarif_base)
    st.session_state.tarif_km = st.sidebar.number_input("Prix au KM", value=st.session_state.tarif_km)