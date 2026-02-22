import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Sunu Course Elite | Partout à Dakar", page_icon="🚕", layout="wide")

# Initialisation Admin
if 'prix_km' not in st.session_state: st.session_state.prix_km = 450
if 'codes_promo' not in st.session_state: st.session_state.codes_promo = {"SUNU2026": 0.10}

# --- 2. STYLE CSS (Ajout de badges zones) ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background: #0b0f19; color: white; }
    .glass-card { 
        background: rgba(255, 255, 255, 0.03); border-radius: 20px; 
        padding: 25px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px;
    }
    .zone-badge {
        background: rgba(59, 130, 246, 0.2); color: #60a5fa;
        padding: 5px 15px; border-radius: 50px; border: 1px solid #3b82f6;
        display: inline-block; margin: 5px; font-size: 12px; font-weight: bold;
    }
    .price-tag { font-size: 40px; color: #10b981; font-weight: 900; text-align: center; }
    .stButton>button { background: linear-gradient(90deg, #25D366 0%, #128C7E 100%); border: none; height: 55px; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
st.sidebar.title("🚀 Menu")
page = st.sidebar.selectbox("Choisir une page", ["🏠 Accueil & Réservation", "✈️ Radar des Vols", "🔑 Administration"])

# --- PAGE ACCUEIL ---
if page == "🏠 Accueil & Réservation":
    # BANNIÈRE "PARTOUT À DAKAR"
    st.title("⚡ Sunu Course Elite")
    st.subheader("Votre VTC de confiance partout dans la région de Dakar")
    
    # Affichage des zones pour rassurer le client
    st.markdown("""
        <div style="margin-bottom: 20px;">
            <span class="zone-badge">📍 Plateau</span> <span class="zone-badge">📍 Almadies</span> 
            <span class="zone-badge">📍 Pikine</span> <span class="zone-badge">📍 Guédiawaye</span> 
            <span class="zone-badge">📍 Rufisque</span> <span class="zone-badge">📍 Keur Massar</span>
            <span class="zone-badge">📍 Diamniadio</span> <span class="zone-badge">✈️ AIBD</span>
        </div>
    """, unsafe_allow_html=True)

    col_form, col_info = st.columns([1.5, 1])

    with col_form:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📋 Réserver une course instantanée")
        
        nom = st.text_input("Nom complet")
        
        c1, c2 = st.columns(2)
        with c1:
            # Message clair sur le type de trajet
            type_course = st.radio("Type de déplacement", ["🏙️ Course Urbaine (Dakar City)", "✈️ Transfert AIBD", "🛣️ Hors Dakar (Mbour, Thiès...)"])
            depart = st.text_input("📍 Point de prise en charge exact", placeholder="Ex: Boutique x, Rue y, Quartier z")
        with c2:
            destination = st.text_input("🏁 Destination finale", placeholder="Où allez-vous ?")
            gamme = st.selectbox("Véhicule souhaité", ["Standard (Éco)", "Affaire (SUV)", "Luxe (Van)"])
            tel = st.text_input("WhatsApp (77XXXXXXX)")

        # LOGIQUE DE CALCUL
        # Si c'est AIBD ou Hors Dakar, on met une distance plus longue
        dist_simulee = 58 if type_course != "🏙️ Course Urbaine (Dakar City)" else 12
        tarif = st.session_state.prix_km
        if gamme == "Affaire": tarif += 300
        
        prix_final = 1500 + (dist_simulee * tarif)
        
        st.markdown(f'<div class="price-tag">{int(prix_final):,} FCFA</div>', unsafe_allow_html=True)
        st.caption("🚀 Prix fixe garanti : inclut carburant, chauffeur et climatisation.")

        if st.button("🚀 COMMANDER MAINTENANT"):
            if nom and tel and depart:
                gps = f"https://www.google.com/maps/dir/?api=1&origin={depart.replace(' ','+')}&destination={destination.replace(' ','+')}"
                msg = f"🚕 *COMMANDE SUNU COURSE*\n👤 Nom: {nom}\n🛣️ Type: {type_course}\n📍 De: {depart}\n🏁 À: {destination}\n💰 Prix: {int(prix_final)} FCFA\n🗺️ Itinéraire: {gps}"
                wa_url = f"https://wa.me/221775797998?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
                st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%; cursor:pointer;">📲 Envoyer sur WhatsApp</button></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_info:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("✅ Pourquoi nous ?")
        st.write("✔️ **Disponibilité 24h/7j**")
        st.write("✔️ **Partout à Dakar** : De la Pointe des Almadies à la sortie de Rufisque.")
        st.write("✔️ **Sécurité** : Chauffeurs vérifiés et suivi GPS en temps réel.")
        st.write("---")
        st.subheader("🗺️ Zone de couverture")
        st.markdown('<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d123485.45265553062!2d-17.494793!3d14.731034!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xec172f5b3c5bb71%3A0x552ef32a583725b!2sDakar!5e0!3m2!1sfr!2ssn!4v1700000000000" width="100%" height="300" style="border:0;" allowfullscreen=""></iframe>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# (Les autres pages Radar et Admin restent identiques au code précédent)