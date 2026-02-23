import streamlit as st

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Sunu Course Elite | Calculateur & Radar", page_icon="🚕", layout="wide")

# Paramètres de prix (Imbattables)
if 'tarif_base' not in st.session_state: st.session_state.tarif_base = 500  
if 'tarif_km' not in st.session_state: st.session_state.tarif_km = 300      

# --- 2. BASE DE DONNÉES DE DISTANCES (Dakar) ---
distances_dakar = {
    ("PIKINE", "PLATEAU"): 15,
    ("PIKINE", "ALMADIES"): 22,
    ("GUEDIAWAYE", "PLATEAU"): 18,
    ("PARCELLES", "PLATEAU"): 12,
    ("PLATEAU", "AIBD"): 55,
    ("ALMADIES", "AIBD"): 62,
    ("GRAND YOFF", "PLATEAU"): 10,
    ("PIKINE", "AIBD"): 48,
    ("RUFISQUE", "AIBD"): 28,
}

def estimer_distance_auto(dep, dest):
    dep, dest = dep.upper(), dest.upper()
    for (d1, d2), dist in distances_dakar.items():
        if (d1 in dep and d2 in dest) or (d2 in dep and d1 in dest):
            return dist
    return 55 if "AIBD" in dep+dest else 12

# --- 3. INTERFACE PRINCIPALE ---
st.title("⚡ Sunu Course Elite")
st.markdown(f'''
    <a href="tel:+221704576459" style="text-decoration:none;">
        <div style="background:#3b82f6;color:white;padding:12px;border-radius:12px;text-align:center;font-weight:bold;margin-bottom:15px;">
            📞 URGENCE : 70 457 64 59 (Appel Direct)
        </div>
    </a>
''', unsafe_allow_html=True)

# Onglets pour séparer la réservation et le radar
tab1, tab2 = st.tabs(["🚕 Réserver une Course", "✈️ Radar de Vols AIBD"])

with tab1:
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown('<div style="background:rgba(255,255,255,0.05);padding:25px;border-radius:20px;border:1px solid rgba(255,255,255,0.1);">', unsafe_allow_html=True)
        st.subheader("📍 Calculateur d'itinéraire")
        nom = st.text_input("Nom du passager")
        
        c1, c2 = st.columns(2)
        with c1:
            depart = st.text_input("📍 Point de départ", placeholder="Ex: Pikine Tally Bou Mack")
            gamme = st.selectbox("Véhicule", ["Standard", "Affaire (SUV)", "Luxe"])
        with c2:
            destination = st.text_input("🏁 Point d'arrivée", placeholder="Ex: Plateau ou AIBD")
            tel = st.text_input("WhatsApp (70 457 64 59)")

        # LOGIQUE DE CALCUL
        dist_reelle = estimer_distance_auto(depart, destination)
        prix_calcule = st.session_state.tarif_base + (dist_reelle * st.session_state.tarif_km)
        
        if gamme == "Affaire (SUV)": prix_calcule += 2500
        if "AIBD" in (depart + destination).upper(): prix_calcule += 3000 # Ajout péage automatique

        st.markdown(f'<div style="font-size:50px;color:#10b981;font-weight:900;text-align:center;">{int(prix_calcule):,} FCFA</div>', unsafe_allow_html=True)
        st.caption(f"📏 Distance estimée : {dist_reelle} km | 💰 Tarif : {st.session_state.tarif_km}F/km")

        if st.button("🚀 CONFIRMER LA RÉSERVATION"):
            gps = f"https://www.google.com/maps/dir/?api=1&origin={depart.replace(' ','+')}&destination={destination.replace(' ','+')}"
            msg = f"🚕 *COMMANDE SUNU COURSE*\n👤 Nom: {nom}\n📍 De: {depart}\n🏁 À: {destination}\n📏 Trajet: {dist_reelle}km\n💰 Prix: {int(prix_calcule)} FCFA\n🧭 GPS Chauffeur: {gps}"
            wa_url = f"https://wa.me/221704576459?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
            st.markdown(f'<a href="{wa_url}" target="_blank"><button style="width:100%;height:60px;background:#25D366;color:white;border:none;border-radius:15px;font-weight:bold;cursor:pointer;">📲 Commander via WhatsApp</button></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("🗺️ Carte")
        st.info("Prix ajusté en temps réel selon l'itinéraire.")
        # Carte statique de Dakar (remplaçable par une carte dynamique plus tard)
        st.markdown('<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d123475.2982846153!2d-17.42!3d14.72!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sfr!2ssn!4v1620000000000" width="100%" height="350" style="border:0;border-radius:15px;"></iframe>', unsafe_allow_html=True)

with tab2:
    st.subheader("✈️ Suivi des vols en direct (AIBD - DSS)")
    st.write("Idéal pour vérifier si l'avion de votre client est à l'heure avant le transfert.")
    # Radar de vol centré sur le Sénégal
    st.components.v1.iframe("https://www.flightradar24.com/multiview/14.67,-17.07/11", height=600, scrolling=True)

# --- 4. BAS DE PAGE ---
st.markdown("---")
st.caption("© 2026 Sunu Course Elite - Partout à Dakar au meilleur prix.")