"""A factory to create custom Plotly charts."""


from __future__ import annotations

from typing import List, Tuple
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Figure
from utils import (
    color_pallet,
    geo_data,
    oasis_discography
)


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

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        hovermode="closest",
        margin={ "t":70, "r":30, "b":60, "l":60 },
        legend_title_text=""
    )

    return fig


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


def _clear_song(raw: str) -> str:
    """
    Strips the "Encore" prefix from the dataset.
    """

    song = raw.strip()
    if song.lower().startswith("encore:"):
        song = song[len("encore:"):].strip()

    return song


def _song_to_album(song: str) -> str:
    """
    Gets the Oasis album according to the given song.
    """

    return oasis_discography.SONGS.get(song, "Other / Unknown")


def _compute_album_counts(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    TODO
    """

    rows: List[str] = []
    for _, row in df.iterrows():
        if pd.isna(row["setlist"]):
            continue

        songs = [song.strip() for song in row["setlist"].split('|')]

        for song in songs:
            if song.lower().startswith("Song played from tape:".lower()):
                continue

            cleaned = _clear_song(song)
            album = _song_to_album(cleaned)
            rows.append({
                "concert_id": row["concert_id"],  # type: ignore (Pylance)
                "song": cleaned,
                "album": album
            })

    songs_df = pd.DataFrame(rows)

    # Unique songs per album (deduplicated across all concerts):
    unique_songs_df = (
        songs_df.drop_duplicates(subset=["song"])
        .groupby("album")
        .size()
        .reset_index(name="unique_songs")
    )

    # Total plays per album across all concerts:
    song_plays_df = (
        songs_df.groupby("album")
        .size()
        .reset_index(name="total_plays")
    )

    merged_df = unique_songs_df.merge(song_plays_df, on="album")

    # Enforce albums order:
    merged_df["album"] = pd.Categorical(
        merged_df["album"],
        categories=oasis_discography.ALBUM_ORDER,
        ordered=True
    )
    merged_df = merged_df.sort_values("album").reset_index(drop=True)
    return merged_df, songs_df


# ===== Chart Functions =====
def create_concerts_by_continent_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a pie chart concerts distribution for each continent.
    """

    df["continent"] = df[COUNTRY_COL].map(geo_data.continent_names)
    continent_df = (
    df.groupby("continent", as_index=False)
      .agg(total_concerts=("concert_id", "count"))
    )

    fig = px.pie(
        continent_df,
        names="continent",
        values="total_concerts",
        color="continent",
        color_discrete_map=color_pallet.CONTINENT_COLORS,
        labels={
            "continent": "Continent",
            "total_concerts": "Concerts"
        }
    )

    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Concerts: %{value}<br>Share: %{percent}<extra></extra>"
    )

    return _apply_default_layout(
        fig=fig,
        remove_title=True
    )


def create_concerts_by_country_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a horizontal bar chart with the total concerts per country.
    """

    plot_df = df.copy()
    plot_df["flag"] = plot_df[COUNTRY_COL].map(geo_data.country_flags)
    plot_df["country_with_flag"] = plot_df["flag"] + " " + plot_df[COUNTRY_COL]
    plot_df["continent"] = plot_df[COUNTRY_COL].map(geo_data.continent_names)

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
        color_discrete_map=color_pallet.CONTINENT_COLORS,
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
        xaxis_title="Total Concerts",
        yaxis_title="Country",
        showlegend=True
    )

    fig.update_xaxes(tickformat=",")
    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside"
    )

    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Concerts: %{value}<extra></extra>"
    )

    return _apply_default_layout(
        fig=fig,
        remove_title=True
    )


def create_attendance_by_concert_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a horizontal bar chart of estimated attendance per concert.
    """

    plot_df = df.copy()
    plot_df[DATE_COL] = pd.to_datetime(plot_df[DATE_COL], errors="coerce")
    plot_df[ATTENDANCE_COL] = pd.to_numeric(plot_df[ATTENDANCE_COL], errors="coerce")
    plot_df["concert_label"] = _create_concert_label(df=plot_df, include_date=False)
    plot_df["continent"] = plot_df[COUNTRY_COL].map(geo_data.continent_names)
    plot_df = plot_df.sort_values(ATTENDANCE_COL, ascending=True).reset_index(drop=True)

    fig = px.bar(
        plot_df,
        x=ATTENDANCE_COL,
        y=CONCERT_LABEL_COL,
        color="continent",
        color_discrete_map=color_pallet.CONTINENT_COLORS,
        orientation="h",
        custom_data=[DATE_COL],
        category_orders={
            CONCERT_LABEL_COL: plot_df[CONCERT_LABEL_COL].tolist()
        },
        labels={
            DATE_COL: "Date",
            "continent": "Continent",
            ATTENDANCE_COL: "Estimated Attendance",
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

    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Attendance: %{x:,}<br>"
            "Date: %{customdata[0]|%b %d, %Y}"
            "<extra></extra>"
        )
    )

    return _apply_default_layout(fig, remove_title=True)


def create_attendance_progress_chart(df) -> Figure:
    """
    Creates a line chart of estimated attendance progress per concert.
    """

    plot_df = df.copy()

    plot_df[DATE_COL] = pd.to_datetime(
        plot_df[DATE_COL], errors="coerce"
    )

    plot_df = plot_df.sort_values(
        [ATTENDANCE_COL, DATE_COL], ascending=[True, True]
    ).reset_index(drop=True)

    plot_df = plot_df.drop(columns=[DATE_COL])

    fig = px.line(
        plot_df,
        x=CITY_COL,
        y=ATTENDANCE_COL,
        markers=True,
        labels={
            VENUE_COL: "Venue",
            COUNTRY_COL: "Country",
            ATTENDANCE_COL: "Attendance"
        },
        hover_data={
            CITY_COL: False,
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
            "color": color_pallet.OASIS_COLOR_PALLET["primary"],
            "width": 3
        },
        marker={
            "color": color_pallet.OASIS_COLOR_PALLET["secondary"],
            "size": 8
        }
    )

    return _apply_default_layout(fig, remove_title=True)


def create_song_frequency_by_continent_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a bar chart with song frequencies by continent.
    """

    plot_df = df.copy()
    plot_df["continent"] = plot_df["country_or_constituent_country"].map(geo_data.continent_names)

    rows = []
    for _, row in plot_df.iterrows():
        if pd.notna(row["setlist"]):
            songs = [s.strip() for s in str(row["setlist"]).split("|")]
            for song in songs:
                if song:
                    rows.append({
                        "song": song,
                        "continent": row["continent"]
                    })

    songs_df = pd.DataFrame(rows)
    song_continent_df = (
        songs_df.groupby(["song", "continent"], as_index=False)
        .size()
        .rename(columns={"size": "plays"})
    )

    top_songs = (
        song_continent_df.groupby("song")["plays"]
        .sum()
        .nlargest(15)
        .index
    )

    song_continent_df = song_continent_df[
        song_continent_df["song"].isin(top_songs)
    ]

    fig = px.bar(
        song_continent_df,
        x="song",
        y="plays",
        color="continent",
        color_discrete_map=color_pallet.CONTINENT_COLORS,
        barmode="group",
        labels={
            "song": "Song",
            "plays": "Number of Performances",
            "continent": "Continent"
        },
        hover_data={
            "song": False,
            "continent": False
        }
    )

    fig.update_xaxes(tickangle=-45)
    return _apply_default_layout(fig, remove_title=True)


def create_song_frequency_by_album_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a donut chart with unique songs frequency by LP/EP.
    """

    plot_df = df.copy()
    album_df, _ = _compute_album_counts(plot_df)
    colors = [
        color_pallet.OASIS_ALBUM_COLORS.get(album, "#ADB5BD")
        for album in album_df["album"]
    ]

    fig = go.Figure(
        go.Pie(
            labels=album_df["album"],
            values=album_df["unique_songs"],
            hole=0.55,
            marker={
                "colors": colors,
                "line": {
                    "color": "rgba(0,0,0,0)",
                    "width": 0
                },
            },
            textinfo="label+percent",
            textposition="outside",
            hovertemplate="<b>%{label}</b><br>"
                            + "Unique Songs in Setlist" + ": %{value}<br>"
                            "Share: %{percent}<extra></extra>",
            sort=False,
        )
    )

    fig.update_layout(
        showlegend=True,
        legend={
            "orientation": 'v',
            "x": 1.02,
            "y": 0.5,
            "yanchor": "middle",
            "font": { "size": 12 }
        },
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin= { "t": 80, "b": 20, "l": 20, "r": 160 }
    )

    return fig
