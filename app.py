import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Pressione Sanguigna", layout="centered")
st.title("📊 Monitoraggio Pressione Sanguigna")

# Inizializza dati se non presenti
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["DataOra", "Sistolica", "Diastolica", "Pulsazioni"])

# Form inserimento dati
st.subheader("➕ Inserisci nuova rilevazione")
with st.form("inserimento_dati"):
    col1, col2 = st.columns(2)
    sistolica = col1.number_input("Pressione Massima (Sistolica)", min_value=50, max_value=250, step=1)
    diastolica = col2.number_input("Pressione Minima (Diastolica)", min_value=30, max_value=150, step=1)
    pulsazioni = st.number_input("Pulsazioni", min_value=30, max_value=200, step=1)
    data_ora = st.datetime_input("Data e ora rilevazione", value=datetime.now())
    submitted = st.form_submit_button("Aggiungi")

    if submitted:
        nuova_riga = {
            "DataOra": data_ora,
            "Sistolica": sistolica,
            "Diastolica": diastolica,
            "Pulsazioni": pulsazioni
        }
        st.session_state.data = pd.concat(
            [st.session_state.data, pd.DataFrame([nuova_riga])],
            ignore_index=True
        )
        st.success("✅ Dati aggiunti con successo!")

# Conversione sicura di DataOra
st.session_state.data["DataOra"] = pd.to_datetime(st.session_state.data["DataOra"])

# Filtro per periodo
st.subheader("📅 Filtra per intervallo di date")
data_inizio = st.date_input("Da", value=datetime.now().date())
data_fine = st.date_input("A", value=datetime.now().date())

dati_filtrati = st.session_state.data[
    (st.session_state.data["DataOra"].dt.date >= data_inizio) &
    (st.session_state.data["DataOra"].dt.date <= data_fine)
]

# Grafico
if not dati_filtrati.empty:
    st.subheader("📈 Grafico pressione nel tempo")
    fig, ax = plt.subplots()
    ax.plot(dati_filtrati["DataOra"], dati_filtrati["Sistolica"], label="Sistolica (max)", color="red", marker="o")
    ax.plot(dati_filtrati["DataOra"], dati_filtrati["Diastolica"], label="Diastolica (min)", color="blue", marker="o")
    ax.set_xlabel("Data e ora")
    ax.set_ylabel("mmHg")
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Medie
    media_sistolica = dati_filtrati["Sistolica"].mean()
    media_diastolica = dati_filtrati["Diastolica"].mean()
    st.markdown(f"🟥 **Media pressione massima (sistolica):** {media_sistolica:.1f} mmHg")
    st.markdown(f"🟦 **Media pressione minima (diastolica):** {media_diastolica:.1f} mmHg")
else:
    st.warning("⚠️ Nessun dato trovato nel periodo selezionato.")

# Tabella dati
st.subheader("📋 Storico dati inseriti")
st.dataframe(st.session_state.data.sort_values(by="DataOra", ascending=False))
