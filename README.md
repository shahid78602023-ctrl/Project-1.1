# Sales Data Analysis Dashboard

An interactive dashboard that helps a business track sales performance, profit trends, and growth over time — simulating how companies turn raw transactional data into decision-ready visuals.

**[Live demo](docs/index.html)** — open `docs/index.html` directly in a browser, or enable GitHub Pages (Settings → Pages → source: `/docs`) to host it.

## What's inside

| Path | Purpose |
|---|---|
| `data/sales_data.csv` | Raw sales dataset (Order ID, Product, Category, Sales, Profit, Date, Region), Superstore-style, with intentional missing values / duplicate rows / mixed date formats for cleaning practice |
| `src/generate_data.py` | Generates the raw dataset (swap this out for a real Kaggle download if you want real data) |
| `src/sales_analysis.py` | Loads, cleans, and analyzes the data: fixes dates, fills missing values, drops duplicates, computes KPIs, builds monthly/yearly trends, exports JSON for the dashboard |
| `output/sales_data_clean.csv` | Cleaned dataset |
| `output/dashboard_data.json` | Aggregated data consumed by the dashboard |
| `docs/index.html` | Self-contained interactive dashboard (HTML/CSS/JS + Chart.js) — filter by region, category, and year |

## Features

- KPI cards: total sales, total profit, order count, average order value
- Monthly sales & profit trend line
- Sales-by-category breakdown (donut)
- Top products and top regions (bar charts)
- Searchable, filterable order-level table
- All filtering happens client-side — no backend required

## Getting started

```bash
git clone <your-repo-url>
cd sales-data-analysis-dashboard
pip install -r requirements.txt

python src/generate_data.py     # (optional) regenerate data/sales_data.csv
python src/sales_analysis.py    # clean + analyze, writes output/dashboard_data.json
```

Then open `docs/index.html` in your browser. The dashboard's data is embedded at build time, so it works fully offline — no server needed.

## Using real data

Replace `data/sales_data.csv` with the [Kaggle Superstore dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) (or any dataset with the same column names: `Order ID, Product, Category, Sales, Profit, Date, Region`), then re-run:

```bash
python src/sales_analysis.py
```

This regenerates `output/dashboard_data.json`. To refresh `docs/index.html` with the new data embedded, re-run the embed step (see `src/sales_analysis.py` output and swap the JSON into the `<script>` block in `docs/index.html`, or ask for the embed script).

## Tech stack

Python (pandas, numpy) for the data pipeline · HTML/CSS/JavaScript + [Chart.js](https://www.chartjs.org/) for the dashboard · no build tools or backend required.

## License

MIT — see [LICENSE](LICENSE).
