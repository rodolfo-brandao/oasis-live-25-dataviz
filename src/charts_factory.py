"""A factory to create custom Plotly charts."""


from __future__ import annotations

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


# ===== Dictionaries =====
country_continents: dict[str, str] = {
    "England": "Europe",
    "Wales": "Europe",
    "Scotland": "Europe",
    "Ireland": "Europe",
    "United States": "North America",
    "Canada": "North America",
    "Mexico": "North America",
    "Japan": "Asia",
    "South Korea": "Asia",
    "Australia": "Oceania",
    "Argentina": "South America",
    "Chile": "South America",
    "Brazil": "South America"
}

continent_colors: dict[str, str] = {
        "Europe": "#FF2C2C",            # red
        "North America": "#007FFF",     # azure
        "South America": "#0BDA51",     # malachite
        "Asia": "#FFEF00",              # canary yellow
        "Oceania": "#F2F0EF"            # off-white
}

# Country/Constituent Country:
country_flags: dict[str, str] = {
    "England": "🇬🇧",
    "Wales": "🇬🇧",
    "Scotland": "🇬🇧",
    "Ireland": "🇮🇪",
    "United States": "🇺🇸",
    "Canada": "🇨🇦",
    "Mexico": "🇲🇽",
    "Japan": "🇯🇵",
    "South Korea": "🇰🇷",
    "Australia": "🇦🇺",
    "Argentina": "🇦🇷",
    "Chile": "🇨🇱",
    "Brazil": "🇧🇷"
}


# ===== DataFrame Main Columns =====
DATE_COL = "date"
COUNTRY_COL = "country_or_constituent_country"
CITY_COL = "city"
VENUE_COL = "venue"
ATTENDANCE_COL = "attendance_estimated_per_concert"
GROSS_COL = "gross_estimated_usd_per_concert"
SETLIST_COL = "setlist"
CONCERT_LABEL_COL = "concert_label"


# ===== Private Functions =====
def _apply_default_layout(fig: Figure, remove_title=False) -> Figure:
    """
    Applies a consistent layout/style to Plotly figures.
    """

    if remove_title:
        fig.update_layout(title="")

    return fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        hovermode="closest",
        margin={ "t":70, "r":30, "b":60, "l":60 },
        legend_title_text=""
    )


def _create_concert_label(df: pd.DataFrame, include_date: bool=True) -> pd.Series:
    """
    Creates a friendly concert label for charts.
    """

    if include_date:
        return (
            df[CITY_COL].astype("str")
            + " ("
            + df[VENUE_COL].astype("str")
            + ")"
            + " | "
            + pd.to_datetime(df[DATE_COL], errors="coerce").dt.strftime("%Y-%m-%d")
        )

    return (
        df[CITY_COL].astype("str")
        + " ("
        + df[VENUE_COL].astype("str")
        + ")"
    )


# ===== Chart Functions =====
def create_concerts_by_continent_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a pie chart concerts distribution for each continent.
    """

    df["continent"] = df["country_or_constituent_country"].map(country_continents)
    continent_df = (
    df.groupby("continent", as_index=False)
      .agg(total_concerts=("concert_id", "count"))
    )

    fig = px.pie(
        continent_df,
        names="continent",
        values="total_concerts",
        color="continent",
        color_discrete_map=continent_colors,
        labels={
            "continent": "Continent",
            "total_concerts": "Concerts"
        }
    )

    fig.update_traces(
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>Concerts: %{value}<br>Share: %{percent}<extra></extra>"
    )

    return _apply_default_layout(
        fig=fig,
        remove_title=True
    )


def create_concerts_by_country_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a bar chart with the total concerts per country.
    """

    plot_df = df.copy()
    plot_df["flag"] = plot_df["country_or_constituent_country"].map(country_flags)
    plot_df["country_with_flag"] = plot_df["flag"] + " " + plot_df["country_or_constituent_country"]
    plot_df["continent"] = plot_df[COUNTRY_COL].map(country_continents)

    country_df = (
        plot_df.groupby(["country_with_flag", "continent"], as_index=False)
        .agg(
            total_concerts=("concert_id", "count"),
            total_attendance=(ATTENDANCE_COL, "sum")
        )
        .sort_values("total_attendance")
    )

    fig = px.bar(
        country_df,
        x="total_concerts",
        y="country_with_flag",
        color="continent",
        color_discrete_map=continent_colors,
        orientation="h",
        text="total_concerts",
        labels={
            "total_concerts": "Concerts",
            "country_with_flag": "Country",
            "continent": "Continent",
            "total_attendance": "Attendance"
        },
        category_orders={
            "country_with_flag": country_df["country_with_flag"].tolist()
        },
        hover_data={
            "continent": True,
            "total_concerts": False,
            "total_attendance": ":,",
            "country_with_flag": False
        }
    )

    fig.update_layout(
        xaxis_title="Concerts",
        yaxis_title="Country",
        showlegend=True
    )

    fig.update_xaxes(tickformat=",")
    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside"
    )

    return _apply_default_layout(
        fig=fig,
        remove_title=True
    )


def create_attendance_by_concert_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a bar chart of estimated attendance per concert.
    """

    plot_df = df.copy()
    plot_df[DATE_COL] = pd.to_datetime(plot_df[DATE_COL], errors="coerce")
    plot_df[ATTENDANCE_COL] = pd.to_numeric(plot_df[ATTENDANCE_COL], errors="coerce")
    plot_df["concert_label"] = _create_concert_label(df=plot_df, include_date=False)
    plot_df.sort_values(ATTENDANCE_COL, ascending=True)

    fig = px.bar(
        plot_df,
        x=ATTENDANCE_COL,
        y=CONCERT_LABEL_COL,
        color=COUNTRY_COL,
        orientation="h",
        labels={
            COUNTRY_COL: "Country",
            ATTENDANCE_COL: "Estimated Attendance per Concert",
            "concert_label": "Concert"
        },
        hover_data={
            ATTENDANCE_COL: ":,"
        }
    )

    fig.update_layout(
        xaxis_title="Estimated Total Attendance",
        yaxis_title="Concert"
    )
    fig.update_yaxes(tickformat=",")
    return _apply_default_layout(fig, remove_title=True)


def create_attendance_progress_chart(df) -> Figure:
    """
    Creates a line chart of estimated attendance progress per concert.
    """

    plot_df = df.copy()
    plot_df[DATE_COL] = pd.to_datetime(plot_df[DATE_COL], errors="coerce")
    plot_df[ATTENDANCE_COL] = pd.to_numeric(
        plot_df[ATTENDANCE_COL], errors="coerce"
    )
    plot_df = plot_df.sort_values(ATTENDANCE_COL, ascending=True).reset_index(drop=True)
    plot_df["date_label"] = plot_df[DATE_COL].dt.strftime("%Y-%m-%d")

    fig = px.line(
        plot_df,
        x=CITY_COL,
        y=ATTENDANCE_COL,
        markers=True,
        hover_data={
            "date_label": True,
            DATE_COL: False,
            CITY_COL: True,
            VENUE_COL: True,
            COUNTRY_COL: True,
            ATTENDANCE_COL: ":,"
        }
    )

    fig.update_layout(
        xaxis_title="City",
        yaxis_title="Crowd"
    )
    fig.update_yaxes(tickformat=",")
    fig.update_xaxes(dtick=1)
    fig.update_traces(
        line={
            "color": "#F2F0EF",  # emerald
            "width": 3
        },
        marker={
            "color": "#FF2C2C",  # red
            "size":8
        }
    )

    return _apply_default_layout(fig, remove_title=True)
