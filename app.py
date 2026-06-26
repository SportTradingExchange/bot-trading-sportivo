import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sport Trading Bot - Dashboard", layout="wide")

st.title("⚽ Trading Bot - Pannello Cloud")
st.sidebar.header("⚙️ Impostazioni e Filtri")

# Lista formattata in modo sicuro a prova di copia-incolla
CAMPIONATI_DEFAULT = [
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

campionati_selezionati = st.sidebar.multiselect(
    "🏆 Filtra o Aggiungi Campionati:",
    options=CAMPIONATI_DEFAULT,
    default=CAMPIONATI_DEFAULT
)

soglia_liquidita = st.sidebar.number_input(
    "💰 Soglia Liquidità Minima Betfair (€)", 
    min_value=500, max_value=100000, value=5000, step=500
)

avvia_scansione = st.sidebar.button("🚀 Avvia Scansione Flashscore")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Campionati Attivi", value=len(campionati_selezionati))
with col2:
    st.metric(label="Regola Filtro 0-0", value="Almeno un controllo positivo (1/6)")

st.write("---")
st.subheader("📋 Segnali di Trading Rilevati in Tempo Reale")

def applica_strategia(quota_o15, e_liquido):
    if not e_liquido:
        return "⚠️ LIVE: Attendi PT 0-0. Entra in Split Over 1.5, Snipe 0.5 o Banca Pareggio"
    if quota_o15 > 1.30:
        return "🚨 PREMATCH: Split Over 1,5"
    return "🚨 PREMATCH: Split Over 2,5"

if avvia_scansione:
    st.success("🤖 Scansione completata con successo tramite server Cloud!")
    
    partiti_fake = [
        {"Match": "Juventus - Inter", "Camp": "Italia - Serie A", "C1": True, "C2": False, "C3": False, "C4": False, "C5": False, "C6": False, "Liq": 24500, "Quota": 1.26},
        {"Match": "Levante - Malaga", "Camp": "Spagna - Liga 2", "C1": False, "C2": False, "C3": True, "C4": False, "C5": False, "C6": False, "Liq": 1800, "Quota": 1.35},
        {"Match": "Chelsea - Arsenal", "Camp": "Inghilterra - Premier League", "C1": False, "C2": False, "C3": False, "C4": False, "C5": False, "C6": False, "Liq": 41000, "Quota": 1.22},
        {"Match": "Roma - Lazio", "Camp": "Italia - Serie A", "C1": True, "C2": True, "C3": True, "C4": False, "C5": False, "C6": False, "Liq": 18900, "Quota": 1.32}
    ]
    
    risultati = []
    for p in partiti_fake:
        if p["Camp"] not in campionati_selezionati:
            continue
            
        ha_almeno_uno_zero_zero = p["C1"] or p["C2"] or p["C3"] or p["C4"] or p["C5"] or p["C6"]
        
        if ha_almeno_uno_zero_zero:
            liquido = p["Liq"] >= soglia_liquidita
            strat = applica_strategia(p["Quota"], liquido)
            risultati.append({
                "Partita": p["Match"],
                "Campionato": p["Camp"],
                "Esito Controlli 0-0": "✅ IDONEA (Almeno uno 0-0 trovato)",
                "Volume Betfair": f"{p['Liq']:,} €",
                "Strategia Suggerita": strat
            })
            
    if risultati:
        df = pd.DataFrame(risultati)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Nessuna partita ha superato i criteri di filtraggio oggi.")
else:
    st.info("Clicca sul pulsante a sinistra per far partire l'algoritmo di controllo.")