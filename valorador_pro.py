import yfinance as yf
from datetime import datetime, timedelta

def obtener_precio(info, obj):
    precio = info.get("currentPrice", None)
    if not precio:
        data = obj.history(period="1d")
        if not data.empty:
            precio = round(data["Close"].iloc[-1], 2)
    return precio


def obtener_dividend_yield(obj, precio, info):
    try:
        # 1. Método principal (dividendos reales)
        dividends = obj.dividends

        if not dividends.empty and precio:
            from datetime import datetime, timedelta
            hoy = datetime.now()
            hace_1y = hoy - timedelta(days=365)

            ultimos = dividends.loc[dividends.index >= hace_1y]
            total_div = ultimos.sum()

            if total_div > 0:
                return total_div / precio

        # 2. Fallback Yahoo directo
        dy = info.get("dividendYield", None)
        if dy:
            return dy

        # 3. Fallback manual
        div_rate = info.get("trailingAnnualDividendRate", None)
        if div_rate and precio:
            return div_rate / precio

        return None

    except:
        return None

def obtener_cagr(ticker):
    try:
        data = yf.Ticker(ticker).history(period="5y")["Close"]
        inicio = data.iloc[0]
        fin = data.iloc[-1]
        return round(((fin / inicio) ** (1/5) - 1) * 100, 2)
    except:
        return None


def obtener_ytd(ticker):
    try:
        data = yf.Ticker(ticker).history(period="ytd")["Close"]
        return round(((data.iloc[-1] / data.iloc[0]) - 1) * 100, 2)
    except:
        return None


def obtener_edad(ticker):
    try:
        data = yf.Ticker(ticker).history(period="max")
        if data.empty:
            return None
        años = (data.index[-1] - data.index[0]).days / 365
        return round(años, 1)
    except:
        return None


def clasificar_etf(info, dividend, cagr):
    nombre = info.get("longName", "").lower()

    if "momentum" in nombre:
        return "Factor - Momentum"
    if "value" in nombre:
        return "Factor - Value"
    if "quality" in nombre:
        return "Factor - Quality"

    if dividend and dividend > 0.025:
        return "Dividendos"

    if cagr and cagr > 12:
        return "Crecimiento"

    return "Blend / Core"


def score_inteligente(ticker):
    obj = yf.Ticker(ticker)
    info = obj.info
    nombre = info.get("longName", ticker)
    low_52 = info.get("fiftyTwoWeekLow", None)
    high_52 = info.get("fiftyTwoWeekHigh", None)

    pe = info.get("trailingPE", None)
    beta = info.get("beta", 1)

    precio = obtener_precio(info, obj)
    dividend = obtener_dividend_yield(obj, precio, info)
    cagr = obtener_cagr(ticker)
    ytd = obtener_ytd(ticker)
    edad = obtener_edad(ticker)

    tipo = clasificar_etf(info, dividend, cagr)

    rent = 5 if cagr and cagr > 12 else 4 if cagr and cagr > 8 else 3 if cagr and cagr > 5 else 2
    growth = 5 if cagr and cagr > 15 else 4 if cagr and cagr > 10 else 3 if cagr and cagr > 6 else 2
    dura = 5 if beta < 0.9 else 4 if beta < 1.1 else 3

    if dividend:
        div = 5 if dividend > 0.03 else 4 if dividend > 0.02 else 3 if dividend > 0.01 else 1
    else:
        div = 1

    if edad:
        hist = 5 if edad > 15 else 4 if edad > 10 else 3 if edad > 5 else 2
    else:
        hist = 3

    if pe and cagr:
        peg = pe / cagr
        val = 5 if peg < 1 else 4 if peg < 1.5 else 3 if peg < 2 else 2
    else:
        val = 3

    score = round(
        rent * 0.25 + growth * 0.20 + dura * 0.20 +
        div * 0.10 + hist * 0.15 + val * 0.10, 2
    )

    return {
        "precio": precio,
        "edad": edad,
        "cagr": cagr,
        "ytd": ytd,
        "pe": pe,
        "beta": beta,
        "dividend": dividend,
        "tipo": tipo,
        "rent": rent,
        "growth": growth,
        "dura": dura,
        "div": div,
        "hist": hist,
        "val": val,
        "score": score,
        "nombre": nombre,
        "low_52": low_52,
        "high_52": high_52,
    }


def recomendacion(score, val, growth):
    if score >= 4 and val >= 3:
        return "🟢 COMPRAR"
    elif score >= 3.5 and growth >= 4:
        return "🟡 COMPRAR EN CAÍDAS"
    elif val <= 2:
        return "🔴 CARO / ESPERAR"
    else:
        return "⚪ MANTENER"
