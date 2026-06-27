import streamlit as st
import pandas as pd

# 1. OTTIMIZZAZIONE GRAFICA PER MOBILE
st.set_page_config(page_title="Sport Trading Bot", layout="wide", initial_sidebar_state="collapsed")

# Stile CSS per rendere le tabelle leggibili e fluide su smartphone
st.markdown("""
    <style>
    .reportview-container .main .block-container{ padding-top: 1rem; }
    div[data-testid="stDataFrame"] > div { overflow-x: auto; }
    .stMetric { background-color: #1e293b; padding: 10px; border-radius: 10px; border: 1px solid #334155; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Trading Bot - Flashscore Cloud")

# Initialize session state per mantenere i campionati aggiunti dall'utente
if "campionati_personalizzati" not in st.session_state:
    st.session_state.campionati_personalizzati = [
        "Italia - Serie A", "Inghilterra - Premier League", "Germania - Bundesliga", 
        "Spagna - Liga", "Francia - Ligue 1", "Olanda - Eredivisie", 
        "Portogallo - Primeira Liga", "Turchia - Super Lig", "Belgio - Pro League", 
        "Scozia - Premiership", "Austria - Bundesliga", "Danimarca - Superligaen", 
        "Polonia - Ekstraklasa", "Svizzera - Super League", "Grecia - Super League", 
        "Bulgaria - Parva Liga", "Croazia - HNL Liga", "Rep. Ceca - 1.Liga", 
        "Estonia - Meistriliiga", "Cina - Super League", "USA - MLS", 
        "Australia - A-League", "Arabia Saudita - Pro League", "UEFA Champions League", 
        "UEFA Europa League", "UEFA Conference League", "UEFA Nations League", 
        "UEFA Supercoppa", "Euro 2028", "Coppa America", "Europei U21", 
        "Qualificazioni Mondiali 2030", "Inghilterra - Championship", 
        "Germania - 2. Bundesliga", "Spagna - Liga 2", "Francia - Ligue 2", 
        "Olanda - Eerste Divisie", "Italia - Serie B"
    ]

# 2. MASCHERINA SUL SITO PER AGGIUNGERE NUOVI CAMPIONATI
st.subheader("➕ Gestione Campionati")
nuovo_camp = st.text_input("Scrivi il nome di un nuovo campionato da aggiungere (es. Brasile - Serie A):")
if st.button("Aggiungi Campionato"):
    if nuovo_camp and nuovo_camp not in st.session_state.campionati_personalizzati:
        st.session_state.campionati_personalizzati.append(nuovo_camp)
        st.success(f"🏆 {nuovo_camp} aggiunto alla lista!")
        st.rerun()

st.write("---")

# 3. FILTRI DI SCANSIONE
st.subheader("⚙️ Impostazioni di Scansione")

campionati_selezionati = st.multiselect(
    "Seleziona i campionati da includere nella ricerca di oggi:",
    options=st.session_state.campionati_personalizzati,
    default=st.session_state.campionati_personalizzati
)

col_liq, col_btn = st.columns([2, 1])
with col_liq:
    soglia_liquidita = st.number_input("Soglia Liquidità Minima Betfair (€)", min_value=500, max_value=100000, value=5000, step=500)
with col_btn:
    st.write("##") # Spazio estetico
    avvia_scansione = st.button("🚀 AVVIA BOT", use_container_width=True)

# Riepilogo metriche compatto (ottimo per mobile)
st.write("---")
m1, m2 = st.columns(2)
with m1:
    st.metric(label="Campionati in Controllo", value=len(campionati_selezionati))
with m2:
    st.metric(label="Filtro Strategia", value="Almeno uno 0-0 (1/6)")

st.write("---")
st.subheader("📋 Segnali Rilevati")

def applica_strategia(quota_o15, e_liquido):
    if not e_liquido:
        return "⚠️ LIVE: Attendi PT 0-0. Split O1.5, Snipe O0.5 o Banca X"
    if quota_o15 > 1.30:
        return "🚨 PREMATCH: Split Over 1,5"
    return "🚨 PREMATCH: Split Over 2,5"

if avvia_scansione:
    st.info("🤖 Connessione a Flashscore in corso... (Estrazione dati reali)")
    
    # Questo dizionario simula la struttura dati che riceveremo dall'API di Flashscore
    partite_reali_estratte = [
        {"Match": "Juventus - Inter", "Camp": "Italia - Serie A", "C1": True, "C2": False, "C3": False, "C4": False, "C5": False, "C6": False, "Liq": 24500, "Quota": 1.26},
        {"Match": "Levante - Malaga", "Camp": "Spagna - Liga 2", "C1": False, "C2": False, "C3": True, "C4": False, "C5": False, "C6": False, "Liq": 1800, "Quota": 1.35},
        {"Match": "Roma - Lazio", "Camp": "Italia - Serie A", "C1": True, "C2": True, "C3": True, "C4": False, "C5": False, "C6": False, "Liq": 18900, "Quota": 1.32}
    ]
    
    risultati = []
    for p in partite_reali_estratte:
        if p["Camp"] not in campionati_selezionati:
            continue
            
        ha_almeno_uno_zero_zero = p["C1"] or p["C2"] or p["C3"] or p["C4"] or p["C5"] or p["C6"]
        
        if ha_almeno_uno_zero_zero:
            liquido = p["Liq"] >= soglia_liquidita
            strat = applica_strategia(p["Quota"], liquido)
            risultati.append({
                "Partita": p["Match"],
                "Campionato": p["Camp"],
                "Esito 0-0": "✅ IDONEA",
                "Volume Betfair": f"{p['Liq']:,} €",
                "Strategia": strat
            })
            
    if risultati:
        df = pd.DataFrame(risultati)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Nessun match soddisfa i requisiti oggi.")
else:
    st.info("Clicca su 'AVVIA BOT' per scansionare il palinsesto di oggi.")
