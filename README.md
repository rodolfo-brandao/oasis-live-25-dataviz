<p align="center">
    <img src="assets/oasis-live-25-logo.png" width="350" alt="The Oasis Live '25 World Tour official logo.">
</p>

# Oasis Live '25 – Data Visualization

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-white.svg)](https://creativecommons.org/licenses/by/4.0/)
![Python version](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
[![Pylint](https://github.com/rodolfo-brandao/oasis-live-25-dataviz/actions/workflows/pylint.yml/badge.svg)](https://github.com/rodolfo-brandao/oasis-live-25-dataviz/actions/workflows/pylint.yml)

## Overview
As a big fan of the band, I decided to combine business with pleasure and put into practice the knowledge I acquired in data visualization during my [postgraduate studies in Data Science](https://github.com/rodolfo-brandao/pos-graduacao) (pt-BR) using public data from Oasis Live '25 World Tour.

## Regarding the Dataset
[![Kaggle dataset](https://img.shields.io/badge/Dataset-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/rodolfobrandao95/oasis-live-25/data)

The dataset contains structured information about the Oasis Live ’25 World Tour, the reunion tour by the British rock band in 2025. It compiles detailed data about each concert, including dates, locations, venues, attendance figures, **estimated** revenues, and performed setlists.

Each row represents a single concert from the tour.

The dataset consolidates publicly available information from multiple sources, including official tour announcements, financial reports, and concert setlist archives.

### Contents
The dataset includes information such as:
- Concert dates
- Cities and countries where concerts took place
- Venues
- Number of shows per city residency
- Reported and estimated attendance
- Estimated gross revenue per concert
- Average ticket price (when available)
- Setlists performed during each concert
- Source references used to compile the information

This structure allows users to analyze the tour both event-by-event and aggregated by city, country, or residency.

### Data Sources
Information in the dataset was compiled from publicly available sources, including:
- Tour date and attendance reports
- Concert financial reports and industry publications
- Concert setlist archives

Each row includes reference fields indicating the source used for the corresponding data (Wikipedia, Poolstar Magazine, setlist.fm).

Primary types of sources include:
- Official tour information
- Concert industry reporting (e.g., Pollstar-style financial summaries)
- Public setlist databases

### Notes on Estimates
Not all concerts have publicly reported financial data or attendance figures. In these cases:
- Attendance values may be estimated from city residency totals
- Gross revenue may be estimated using average ticket price and attendance

Fields describing these estimates are included in the dataset to maintain transparency.

> [!NOTE]
> _The dataset is compiled exclusively from publicly available information and is intended for educational, analytical, and research purposes._
> 
> _All referenced materials remain the property of their respective sources._