import streamlit as st
import yfinance as yf
from valorador_pro import score_inteligente, recomendacion

# Configuración de página
st.set_page_config(page_title="Valorador ETF", layout="centered")

st.title("📊 Valorador Inteligente de ETFs")

# Input
ticker = st.text_input("Ingresa el ticker (VOO, QQQ, VT...)")

if ticker:
    ticker = ticker.upper()
    r = score_inteligente(ticker)

    # 🧠 NOMBRE
    st.title(f"📊 {r['nombre']}")

    # 📊 DATOS PRINCIPALES
    st.subheader("📌 Datos principales")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("💰 Precio", f"${r['precio']}")
        st.metric("📅 Edad", f"{r['edad']} años")
        st.metric("📈 CAGR 5Y", f"{r['cagr']}%")

    with col2:
        st.metric("📊 YTD", f"{r['ytd']}%")
        st.metric("📉 P/E", f"{round(r['pe'],2) if r['pe'] else 'N/A'}")
        st.metric("⚡ Beta", f"{r['beta']}")


    # 📊 52 WEEK RANGE
    if r["low_52"] and r["high_52"]:
        st.subheader("📊 52 Week Range")
        st.write(f"${round(r['low_52'],2)}  →  ${round(r['high_52'],2)}")

    # ⭐ SCORE
    st.subheader("⭐ Score")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rentabilidad", r["rent"])
    col2.metric("Crecimiento", r["growth"])
    col3.metric("Durabilidad", r["dura"])

    col1.metric("Dividendo", r["div"])
    col2.metric("Historial", r["hist"])
    col3.metric("Valoración", r["val"])

    st.success(f"⭐ Score Final: {r['score']} / 5")

    # 🧠 TIPO
    st.subheader("🧠 Tipo de ETF")
    st.info(r["tipo"])

    # 🎯 DECISIÓN
    st.subheader("🎯 Decisión")

    decision = recomendacion(r['score'], r['val'], r['growth'])

    if "COMPRAR" in decision:
        st.success(decision)
    elif "CAÍDAS" in decision:
        st.warning(decision)
    else:
        st.error(decision)

    # 📈 GRÁFICO
    st.subheader("📈 Precio (último año)")

    data = yf.Ticker(ticker).history(period="1y")

    if not data.empty:
        st.line_chart(data["Close"])
    else:
        st.write("No hay datos disponibles")
