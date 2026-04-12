# CLAUDE.md

## Project Overview

Interactive Streamlit dashboard visualizing the **Oasis Live '25 World Tour** using public data. Charts are built with Plotly and explore attendance figures, estimated revenues, concert distribution, and setlist composition.

- Live app: [oasis-live-25.streamlit.app](https://oasis-live-25.streamlit.app/)
- Dataset: [Kaggle](https://www.kaggle.com/datasets/rodolfobrandao95/oasis-live-25/data)

## Tech Stack

| Tool       | Version |
|------------|---------|
| Python     | 3.14    |
| Pandas     | 2.3.3   |
| Plotly     | 6.6.0   |
| Streamlit  | 1.44.0  |

## Running Locally

```bash
pip install -r requirements.txt
streamlit run src/dashboard.py
```

The app reads `./data/oasis_live_25.csv` relative to the project root, so always run from the root.

## Project Structure

```
oasis-live-25-dataviz/
├── assets/                         # Repo banner and dashboard favicon
├── data/
│   └── oasis_live_25.csv           # Tour dataset (one row per concert)
├── src/
│   ├── dashboard.py                # Streamlit entry point — layout and metrics only
│   ├── charts_factory.py           # All Plotly chart creation functions
│   └── utils/
│       ├── color_pallet.py         # Color system: album palette + continent palette
│       ├── geo_data.py             # Country → continent and country → flag emoji maps
│       └── oasis_discography.py    # Album/song reference data and album order
├── requirements.txt
└── README.md
```

## Architecture Notes

- **`dashboard.py`** handles only layout, metrics, and `st.plotly_chart` calls — no data transformation logic.
- **`charts_factory.py`** owns all chart logic. Each public function accepts a `pd.DataFrame` and returns a `plotly.graph_objects.Figure`. Private helpers are prefixed with `_`.
- `_apply_default_layout()` is the single place to enforce visual consistency (`plotly_white` template, margins, hover mode). Call it at the end of every chart function.
- **`utils/`** modules are pure data: no Streamlit or Plotly imports allowed there.

## Key Data Conventions

- Primary dataset columns used across charts are defined as module-level constants at the top of `charts_factory.py` (e.g. `ATTENDANCE_COL`, `COUNTRY_COL`).
- Continent and flag lookups live in `geo_data.py` as plain dicts; map them with `df[col].map(geo_data.continent_names)`.
- Song → album resolution goes through `oasis_discography.SONGS`; unknown songs fall back to `"Other / Unknown"`.
- Album ordering in charts is enforced via `oasis_discography.ALBUM_ORDER` and `pd.Categorical`.

## Color System

All colors come from `utils/color_pallet.py`. Never hard-code hex values in chart functions.

- `OASIS_ALBUM_COLORS` — one color per LP/EP, used in setlist charts.
- `CONTINENT_COLORS` — one color per continent, used in geography charts.
- `OASIS_COLOR_PALLET` — named semantic colors (`primary`, `secondary`, `accent`, etc.) for one-off use (e.g. range lines in the dot plot use `light`).

## Linting

CI runs Pylint on every push (`.github/workflows/pylint.yml`). The score must be **≥ 7.0**.

Disabled rules: `C0103` (naming), `C0114` (missing module docstring), `C0116` (missing function docstring), `E0401` (import errors — Pylint can't resolve local imports in CI).

Run locally with the same flags:

```bash
pylint --disable=C0103,C0114,C0116,E0401 --fail-under=7 $(git ls-files '*.py')
```
