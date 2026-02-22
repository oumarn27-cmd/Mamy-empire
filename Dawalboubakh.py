import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Sunu Course Pro | Navigation Live", page_icon="🧭", layout="wide")

# Initialisation Admin
if 'prix_km' not in st.session_state: st.session_state.prix_km = 450
if 'codes_promo' not in st.session_state: st.session_state.codes_promo = {"SUNU2026": 0.10}

# --- 2. STYLE CSS ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: #0b0f19; color: white; }
    .glass-card { 
        background: rgba(255, 255, 255, 0.03); border-radius: 20px; 
        padding: 25px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px;
    }
    .nav-box { background: #1e293b; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; margin-top: 10px; }
    .price-tag { font-size: 40px; color: #10b981; font-weight: 900; text-align: center; }
    .stButton>button { background: linear-gradient(90deg, #25D366 0%, #128C7E 100%); border: none; height: 55px; font-weight: bold; border-radius: 12px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. NAVIGATION ---
st.sidebar.title("🚀 Sunu Course")
page = st.sidebar.selectbox("Navigation", ["🏠 Accueil & Réservation", "✈️ Radar des Vols", "🔑 Administration"])

if page == "🏠 Accueil & Réservation":
    st.title("⚡ Sunu Course Elite")
    st.subheader("Transport Premium - Navigation GPS en temps réel")

    col_form, col_map = st.columns([1.5, 1])

    with col_form:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📋 Commander une course")
        
        nom = st.text_input("Nom du passager")
        tel_cli = st.text_input("WhatsApp du passager")
        
        c1, c2 = st.columns(2)
        with c1:
            depart = st.text_input("📍 Lieu de prise en charge", placeholder="Ex: Grand Yoff, Villa 123")
            gamme = st.selectbox("Véhicule", ["Standard", "Affaire", "Luxe"])
        with c2:
            destination = st.text_input("🏁 Lieu de destination", placeholder="Ex: AIBD ou Plateau")
            code_promo = st.text_input("🎟️ Code Promo").upper()

        # LOGIQUE DE PRIX
        dist_est = 58 if "AIBD" in (depart + destination).upper() else 15
        prix_final = 1500 + (dist_est * st.session_state.prix_km)
        
        st.markdown(f'<div class="price-tag">{int(prix_final):,} FCFA</div>', unsafe_allow_html=True)

        if st.button("🚀 CONFIRMER ET ENVOYER AU CHAUFFEUR"):
            if nom and tel_cli and depart:
                # GÉNÉRATION DES LIENS DE NAVIGATION TEMPS RÉEL
                # Lien 1 : Pour que le chauffeur aille chercher le client (Source: Position Chauffeur -> Client)
                nav_vers_client = f"https://www.google.com/maps/dir/?api=1&destination={depart.replace(' ','+')}&travelmode=driving"
                
                # Lien 2 : Itinéraire complet de la course (Source: Client -> Destination)
                itineraire_course = f"https://www.google.com/maps/dir/?api=1&origin={depart.replace(' ','+')}&destination={destination.replace(' ','+')}&travelmode=driving"

                message = (
                    f"🚕 *MISSION SUNU COURSE*\n\n"
                    f"👤 *Client:* {nom}\n"
                    f"📱 *Tel Client:* {tel_cli}\n"
                    f"💰 *Prix à percevoir:* {int(prix_final):,} FCFA\n\n"
                    f"📍 *1. ALLER CHERCHER LE CLIENT:* \n{nav_vers_client}\n\n"
                    f"🏁 *2. TRAJET DE LA COURSE:* \n{itineraire_course}\n\n"
                    f"⚠️ *Note:* Cliquez sur les liens pour lancer la navigation GPS Google Maps."
                )
                
                # TON NUMÉRO : 70 457 64 59
                wa_url = f"https://wa.me/221704576459?text={message.replace(' ', '%20').replace('\n', '%0A')}"
                st.success("✅ Liens de navigation générés !")
                st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; cursor:pointer;">📲 Transmettre au chauffeur via WhatsApp</button></a>', unsafe_allow_html=True)
            else:
                st.error("Champs manquants")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_map:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🛰️ Aperçu de l'Itinéraire")
        # Carte dynamique
        st.markdown('<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d123473.5358941031!2d-17.43!3d14.72!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sfr!2ssn!4v1700000000000" width="100%" height="450" style="border:0;"></iframe>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# (Les pages Radar et Admin restent les mêmes)