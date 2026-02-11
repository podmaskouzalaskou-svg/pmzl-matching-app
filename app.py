import streamlit as st
import pandas as pd

st.set_page_config(page_title="Speed Date Matcher", layout="wide")

st.title("🏆 Speed Dating: Organizátor")

# --- ADMIN SEKCIJA PRE MENÁ ---
# Použijeme expander, aby nastavenia nezaberali miesto na mobile
with st.expander("⚙️ Nastavenia hostí (Uprav mená tu)"):
    st.write("Sem napíš alebo skopíruj mená (každé meno na nový riadok).")
    col_a, col_b = st.columns(2)
    with col_a:
        # Predvolené mená môžeš v kóde zmazať alebo nahradiť
        zoznam_muzi = st.text_area("♂️ Muži:", value="Peter\nMichal\nJakub\nMarek\nJozef", height=200)
    with col_b:
        zoznam_zeny = st.text_area("♀️ Ženy:", value="Simona\nLucia\nEma\nKatarina\nTereza", height=200)
    
    # Spracovanie textu na zoznamy
    muzi = [m.strip() for m in zoznam_muzi.split("\n") if m.strip()]
    zeny = [z.strip() for z in zoznam_zeny.split("\n") if z.strip()]

# Inicializácia pamäte pre lajky
if 'likes' not in st.session_state:
    st.session_state.likes = {}

# --- ZADÁVANIE ÚDAJOV ---
st.header("📍 Zadaj voľby účastníkov")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Páni vybrali:")
    for m in muzi:
        st.session_state.likes[m] = st.multiselect(f"{m} označil:", zeny, key=f"m_{m}")

with col2:
    st.subheader("Dámy vybrali:")
    for z in zeny:
        st.session_state.likes[z] = st.multiselect(f"{z} označila:", muzi, key=f"z_{z}")

# --- VYHODNOTENIE ---
st.divider()
if st.button("🔥 VYHODNOTIŤ ZHODY", use_container_width=True, type="primary"):
    matches = []
    for m in muzi:
        # Pozrieme sa, koho označil muž
        for z in st.session_state.likes.get(m, []):
            # Skontrolujeme, či aj táto žena označila daného muža
            if m in st.session_state.likes.get(z, []):
                matches.append({"Muž": m, "Žena": z})

    if matches:
        st.success(f"Nájdených {len(matches)} zhôd!")
        df = pd.DataFrame(matches)
        st.table(df)
        
        # Možnosť stiahnuť výsledky
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Stiahnuť výsledky (CSV)", data=csv, file_name="zhody_speed_dating.csv", mime="text/csv")
    else:
        st.info("Zatiaľ neboli nájdené žiadne vzájomné zhody.")
