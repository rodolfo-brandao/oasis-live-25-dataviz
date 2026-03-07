from __future__ import annotations

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


# ----- DataFrame Main Columns -----
DATE_COL = "date"
COUNTRY_COL = "country_or_constituent_country"
CITY_COL = "city"
VENUE_COL = "venue"
ATTENDANCE_COL = "attendance_estimated_per_concert"
GROSS_COL = "gross_estimated_usd_per_concert"
SETLIST_COL = "setlist"
CONCERT_LABEL_COL = "concert_label"


# ----- Private Functions -----
def _apply_default_layout(fig: Figure) -> Figure:
    """
    Applies a consistent layout/style to Plotly figures.
    """

    return fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        hovermode="closest",
        margin={ "t":70, "r":30, "b":60, "l":60 },
        legend_title_text=""
    )


def _create_concert_label(df: pd.DataFrame) -> pd.Series:
    """
    Creates a friendly concert label for charts.
    """

    return (
        pd.to_datetime(df[DATE_COL], errors="coerce").dt.strftime("%Y-%m-%d")
        + " | "
        + df[CITY_COL].astype("str")
        + " | "
        + df[VENUE_COL].astype("str")
    )


# ----- Chart Functions -----
def create_attendance_by_concert_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a bar chart of estimated attendance per concert.
    """

    plot_df = df.copy()
    plot_df = plot_df.sort_values(DATE_COL)
    plot_df[DATE_COL] = pd.to_datetime(plot_df[DATE_COL], errors="coerce")
    plot_df[ATTENDANCE_COL] = pd.to_numeric(plot_df[ATTENDANCE_COL], errors="coerce")
    plot_df["concert_label"] = _create_concert_label(df=plot_df)

    fig = px.bar(
        plot_df.sort_values(DATE_COL),
        x=ATTENDANCE_COL,
        y=CONCERT_LABEL_COL,
        color=COUNTRY_COL,
        title="Oasis Live '25 — Estimated Attendance per Concert",
        orientation="h",
        category_orders={
            "concert_label": plot_df["concert_label"].tolist()
        },
        hover_data={
            DATE_COL: True,
            CITY_COL: True,
            VENUE_COL: True,
            COUNTRY_COL: True,
            ATTENDANCE_COL: ":,"
        }
    )

    fig.update_layout(
        xaxis_title="Estimated Attendance",
        yaxis_title="Concert",
        xaxis_tickangle=-60
    )
    fig.update_yaxes(tickformat=",")
    return _apply_default_layout(fig)
