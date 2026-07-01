"""
Project 3: Real-Time Data Analytics Dashboard (Streamlit version)
Run locally with:  streamlit run realtime_dashboard.py

Fetches live weather, crypto, and (optionally) stock data, processes it,
and displays an auto-refreshing dashboard with a simple threshold alert.

Requirements:
    pip install streamlit requests pandas

Notes on API keys:
    - Weather (Open-Meteo): no key required.
    - Crypto (CoinGecko): no key required for the free tier used here.
    - Stocks (Alpha Vantage): requires a free key from alphavantage.co.
      Paste it in the sidebar, or set the ALPHA_VANTAGE_KEY environment
      variable before launching.
"""
import os
import time
from datetime import datetime

import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Live Market & Weather Dashboard", layout="wide")

# ---------------------- SIDEBAR CONTROLS ----------------------
st.sidebar.title("Dashboard Settings")
city = st.sidebar.text_input("City (weather)", "Gurugram")
crypto_ids = st.sidebar.multiselect(
    "Cryptocurrencies", ["bitcoin", "ethereum", "solana", "dogecoin"],
    default=["bitcoin", "ethereum"]
)
alpha_key = st.sidebar.text_input(
    "Alpha Vantage API key (optional, for stocks)",
    value=os.environ.get("ALPHA_VANTAGE_KEY", ""), type="password"
)
stock_symbol = st.sidebar.text_input("Stock symbol (optional)", "AAPL")
refresh_secs = st.sidebar.slider("Auto-refresh every (seconds)", 10, 120, 30)
price_alert = st.sidebar.number_input("Alert me if BTC price crosses ($)", value=0, step=1000)

st.title("Real-Time Data Analytics Dashboard")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# ---------------------- FETCH FUNCTIONS ----------------------
@st.cache_data(ttl=refresh_secs)
def fetch_weather(city_name):
    """Open-Meteo: free, no API key required."""
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city_name, "count": 1}, timeout=10
    ).json()
    if not geo.get("results"):
        return None
    loc = geo["results"][0]
    weather = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": loc["latitude"], "longitude": loc["longitude"],
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        }, timeout=10
    ).json()
    return {
        "city": loc["name"],
        "country": loc.get("country", ""),
        "temp_c": weather["current"]["temperature_2m"],
        "humidity": weather["current"]["relative_humidity_2m"],
        "wind_kmh": weather["current"]["wind_speed_10m"],
        "timestamp": weather["current"]["time"],
    }


@st.cache_data(ttl=refresh_secs)
def fetch_crypto(ids):
    """CoinGecko: free, no API key required for this endpoint."""
    if not ids:
        return pd.DataFrame()
    resp = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": ",".join(ids), "vs_currencies": "usd",
                "include_24hr_change": "true"}, timeout=10
    ).json()
    rows = [{"coin": k, "price_usd": v.get("usd"),
             "change_24h_pct": round(v.get("usd_24h_change", 0), 2)}
            for k, v in resp.items()]
    return pd.DataFrame(rows)


@st.cache_data(ttl=refresh_secs)
def fetch_stock(symbol, key):
    """Alpha Vantage: requires a free API key."""
    if not key:
        return None
    resp = requests.get(
        "https://www.alphavantage.co/query",
        params={"function": "GLOBAL_QUOTE", "symbol": symbol, "apikey": key},
        timeout=10
    ).json()
    quote = resp.get("Global Quote", {})
    if not quote:
        return None
    return {
        "symbol": quote.get("01. symbol"),
        "price": float(quote.get("05. price", 0)),
        "change_pct": quote.get("10. change percent", "0%"),
    }


# ---------------------- LAYOUT ----------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Weather")
    try:
        w = fetch_weather(city)
        if w:
            st.metric(f"{w['city']}, {w['country']}", f"{w['temp_c']} °C")
            st.write(f"Humidity: {w['humidity']}%  |  Wind: {w['wind_kmh']} km/h")
            st.caption(f"As of {w['timestamp']}")
        else:
            st.warning("City not found.")
    except Exception as e:
        st.error(f"Weather fetch failed: {e}")

with col2:
    st.subheader("Crypto Prices")
    try:
        df_crypto = fetch_crypto(crypto_ids)
        if not df_crypto.empty:
            st.dataframe(df_crypto, hide_index=True, use_container_width=True)
            st.bar_chart(df_crypto.set_index("coin")["price_usd"])
            btc_row = df_crypto[df_crypto["coin"] == "bitcoin"]
            if price_alert and not btc_row.empty:
                btc_price = btc_row["price_usd"].values[0]
                if btc_price >= price_alert:
                    st.error(f"ALERT: BTC price ${btc_price:,.0f} has crossed your "
                              f"threshold of ${price_alert:,.0f}")
        else:
            st.info("Select at least one coin in the sidebar.")
    except Exception as e:
        st.error(f"Crypto fetch failed: {e}")

with col3:
    st.subheader("Stock Quote")
    if not alpha_key:
        st.info("Enter a free Alpha Vantage API key in the sidebar to enable this panel.")
    else:
        try:
            s = fetch_stock(stock_symbol, alpha_key)
            if s:
                st.metric(s["symbol"], f"${s['price']:.2f}", s["change_pct"])
            else:
                st.warning("No data returned — check the symbol or your API key/rate limit.")
        except Exception as e:
            st.error(f"Stock fetch failed: {e}")

st.divider()
st.caption(
    f"Auto-refreshing every {refresh_secs}s. "
    "Data cached for the refresh interval to stay within free API rate limits."
)

# Auto-refresh loop
time.sleep(refresh_secs)
st.rerun()
