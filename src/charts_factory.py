"""A factory to create custom Plotly charts."""


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
def _apply_default_layout(
        fig: Figure,
        remove_title=False,
        remove_hover_labels=False
    ) -> Figure:
    """
    Applies a consistent layout/style to Plotly figures.
    """

    if remove_title:
        fig.update_layout(title="")

    if remove_hover_labels:
        fig.update_layout(hovermode=False)

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
            pd.to_datetime(df[DATE_COL], errors="coerce").dt.strftime("%Y-%m-%d")
            + " | "
            + df[CITY_COL].astype("str")
            + " | "
            + df[VENUE_COL].astype("str")
        )
    else:
        return (
            df[CITY_COL].astype("str")
            + " ("
            + df[VENUE_COL].astype("str")
            + ")"
        )


# ----- Chart Functions -----
def create_concerts_by_country_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a bar chart with the total concerts per country.
    """

    country_df = (
        df.groupby("country_or_constituent_country", as_index=False)
          .agg(
              total_concerts=("concert_id", "count"),
              total_attendance=("attendance_estimated_per_concert", "sum")
          )
          .sort_values("total_attendance", ascending=False)
    )

    fig = px.bar(
        country_df,
        x="total_concerts",
        y="country_or_constituent_country",
        # color="country_or_constituent_country",
        orientation="h",
        text="total_concerts"
    )

    fig.update_layout(
        xaxis_title="Total Concerts",
        yaxis_title="Country",
        showlegend=False
    )
    fig.update_xaxes(tickformat=",")
    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside"
    )
    return _apply_default_layout(
        fig,
        remove_title=True,
        remove_hover_labels=True
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
        hover_data={
            DATE_COL: True,
            ATTENDANCE_COL: ":,"
        }
    )

    fig.update_layout(
        xaxis_title="Estimated Attendance",
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
    plot_df["date_label"] = plot_df["date"].dt.strftime("%Y-%m-%d")

    fig = px.line(
        plot_df,
        x=CITY_COL,
        y=ATTENDANCE_COL,
        markers=True,
        hover_data={
            "date_label": True,
            "city": True,
            "venue": True,
            "country_or_constituent_country": True,
            "attendance_estimated_per_concert": ":,",
            "date": False
        }
    )

    fig.update_layout(
        xaxis_title="City",
        yaxis_title="Estimated Attendance"
    )
    fig.update_yaxes(tickformat=",")
    fig.update_xaxes(dtick=1)
    return _apply_default_layout(fig, remove_title=True)
