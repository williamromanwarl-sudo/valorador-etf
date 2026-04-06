import streamlit as st
from valorador_pro import score_inteligente, recomendacion

st.set_page_config(page_title="Valorador ETF", layout="centered")

st.title("📊 Valorador Inteligente de ETFs")

ticker = st.text_input("Ingresa el ticker (VOO, QQQ, VT...)")

if ticker:
    r = score_inteligente(ticker.upper())

    st.subheader("📌 Datos principales")
    st.write(f"Precio: ${r['precio']}")
    st.write(f"Edad: {r['edad']} años")
    st.write(f"Tipo: {r['tipo']}")
    st.write(f"CAGR 5Y: {r['cagr']}%")
    st.write(f"YTD: {r['ytd']}%")
    st.write(f"P/E: {r['pe']}")
    st.write(f"Beta: {r['beta']}")

    if r["dividend"]:
        st.write(f"Dividend Yield: {round(r['dividend']*100,2)}%")
    else:
        st.write("Dividend Yield: No disponible")

    st.subheader("⭐ Score")
    st.write(f"Rentabilidad: {r['rent']} / 5")
    st.write(f"Crecimiento: {r['growth']} / 5")
    st.write(f"Durabilidad: {r['dura']} / 5")
    st.write(f"Dividendo: {r['div']} / 5")
    st.write(f"Historial: {r['hist']} / 5")
    st.write(f"Valoración: {r['val']} / 5")

    st.success(f"⭐ Score Final: {r['score']} / 5")

    st.subheader("🎯 Decisión")
    st.write(recomendacion(r['score'], r['val'], r['growth']))
