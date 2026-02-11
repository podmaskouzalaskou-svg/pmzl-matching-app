import streamlit as st
import pandas as pd

st.set_page_config(page_title="Speed Date Matcher", layout="wide")

# --- ZOZNAMY (Tu si dopíš mená pred akciou) ---
muzi = ["Peter", "Michal", "Jakub", "Marek", "Jozef"]
zeny = ["Simona", "Lucia", "Ema", "Katarina", "Tereza"]

st.title("🏆 Speed Dating: Organizátor")

if 'likes' not in st.session_state:
    st.session_state.likes = {}

# --- ZADÁVANIE ÚDAJOV ---
col1, col2 = st.columns(2)
with col1:
    st.header("♂️ Voľby mužov")
    for m in muzi:
        st.session_state.likes[m] = st.multiselect(f"{m} označil:", zeny, key=f"m_{m}")

with col2:
    st.header("♀️ Voľby žien")
    for z in zeny:
        st.session_state.likes[z] = st.multiselect(f"{z} označila:", muzi, key=f"z_{z}")

# --- VYHODNOTENIE ---
st.divider()
if st.button("🔥 UKÁŽ ZHODY", use_container_width=True, type="primary"):
    matches = []
    for m in muzi:
        for z in st.session_state.likes.get(m, []):
            if m in st.session_state.likes.get(z, []):
                matches.append({"Muž": m, "Žena": z})

    if matches:
        st.header("💘 Nájdené zhody")
        df = pd.DataFrame(matches)
        st.table(df)

        # Tlačidlo na stiahnutie do Excelu/CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Stiahnuť tabuľku zhôd", data=csv, file_name="zhody.csv", mime="text/csv")
    else:
        st.warning("Zatiaľ žiadna zhoda.")
