# Real-Time Data Analytics Dashboard

A dashboard that continuously updates with live weather and cryptocurrency data — simulating a real-world monitoring system.

**[Live demo](docs/index.html)** — open `docs/index.html` directly in a browser (no setup, no API key) or enable GitHub Pages (Settings → Pages → source: `/docs`).

## What's inside

| Path | Purpose |
|---|---|
| `docs/index.html` | Static HTML/JS dashboard that fetches **real, live** weather ([Open-Meteo](https://open-meteo.com/), no key needed) and crypto prices ([CoinGecko](https://www.coingecko.com/en/api), no key needed) directly from your browser, with configurable auto-refresh and a BTC price-threshold alert |
| `src/realtime_dashboard.py` | Streamlit version for local use — same weather/crypto panels, plus a stock-quote panel via Alpha Vantage (requires a free API key) |
| `requirements.txt` | Python deps for the Streamlit version |

## Why two versions

`docs/index.html` is a static file, but the JavaScript inside it calls real public APIs from *your* browser when opened — so it's genuinely real-time with zero setup. `src/realtime_dashboard.py` is the more typical Python data-pipeline version (requests → pandas → Streamlit), useful if you want to run it locally, extend it, or add the stock panel.

## Getting started (static dashboard)

Just open `docs/index.html` in a browser. Set the city, coins, refresh interval, and an optional BTC price alert in the controls at the top.

## Getting started (Streamlit)

```bash
git clone <your-repo-url>
cd realtime-data-analytics-dashboard
pip install -r requirements.txt
streamlit run src/realtime_dashboard.py
```

To enable the stock panel, get a free key at [alphavantage.co](https://www.alphavantage.co/support/#api-key) and paste it into the sidebar, or set it as an environment variable first:

```bash
export ALPHA_VANTAGE_KEY=your_key_here
streamlit run src/realtime_dashboard.py
```

## Features

- Live weather: temperature, humidity, wind
- Live crypto prices with 24h change, session price-history chart
- Configurable auto-refresh interval
- Price-threshold alert banner
- (Streamlit version) optional stock quote panel

## Tech stack

Vanilla HTML/CSS/JS + [Chart.js](https://www.chartjs.org/) for the static dashboard · Python (Streamlit, requests, pandas) for the local version · [Open-Meteo](https://open-meteo.com/), [CoinGecko](https://www.coingecko.com/en/api), and [Alpha Vantage](https://www.alphavantage.co/) APIs.

## License

MIT — see [LICENSE](LICENSE).
