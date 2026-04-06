"""A custom factory to create Plotly charts."""


from __future__ import annotations

from typing import List, Set
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
CONCERT_ID_COL = "concert_id"
DATE_COL = "date"
COUNTRY_COL = "country_or_constituent_country"
CITY_COL = "city"
VENUE_COL = "venue"
ATTENDANCE_COL = "attendance_estimated_per_concert"
GROSS_COL = "gross_estimated_usd_per_concert"
SETLIST_COL = "setlist"
CONCERT_LABEL_COL = "concert_label"


# ===== Private Functions =====
def _apply_default_layout(fig: Figure, remove_title=False, legend_title: str="") -> Figure:
    """
    Applies a consistent layout/style to Plotly figures.
    """

    if remove_title:
        fig.update_layout(title="")

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        hovermode="closest",
        margin={
            "t":70, "r":30, "b":60, "l":60
        },
        legend_title_text=legend_title
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


def _compute_album_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Counts each Oasis album share according to each
    respective song played across all concerts.
    """

    rows: List[str] = []
    for _, row in df.iterrows():
        if pd.isna(row[SETLIST_COL]):
            continue

        songs = [song.strip() for song in row[SETLIST_COL].split('|')]

        for song in songs:
            if song.lower().startswith("Song played from tape:".lower()):
                continue

            clean_song = _clear_song(song)
            album = _song_to_album(clean_song)
            rows.append({
                CONCERT_ID_COL: row[CONCERT_ID_COL],  # type: ignore (Pylance)
                "song": clean_song,
                "album": album
            })

    songs_df = pd.DataFrame(rows)

    # Ensure unique songs per album (deduplicated across all concerts):
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

    albums_df = unique_songs_df.merge(song_plays_df, on="album")

    # Enforce albums order:
    albums_df["album"] = pd.Categorical(
        albums_df["album"],
        categories=oasis_discography.ALBUM_ORDER,
        ordered=True
    )

    albums_df = albums_df.sort_values("album").reset_index(drop=True)
    return albums_df


# ===== Chart Functions =====
def create_concerts_by_continent_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a pie chart concerts distribution for each continent.
    """

    df["continent"] = df[COUNTRY_COL].map(geo_data.continent_names)
    continent_df = (
        df.groupby("continent", as_index=False)
        .agg(total_concerts=(CONCERT_ID_COL, "count"))
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
        texttemplate="%{label}<br>%{value}",
        hovertemplate="<b>%{label}</b><br>Share: %{percent}<extra></extra>"
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
            total_concerts=(CONCERT_ID_COL, "count"),
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
        xaxis_title="Concerts",
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


def create_attendance_by_venue_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a dot plot of estimated attendance per venue,
    showing median as a dot and min-max as a range line.
    """

    plot_df = df.copy()
    plot_df["continent"] = plot_df[COUNTRY_COL].map(geo_data.continent_names)
    plot_df["concert_label"] = _create_concert_label(df=plot_df, include_date=False)

    venue_df = (
        plot_df.groupby(["concert_label", "continent"], as_index=False)
        .agg(
            median_attendance=(ATTENDANCE_COL, "median"),
            min_attendance=(ATTENDANCE_COL, "min"),
            max_attendance=(ATTENDANCE_COL, "max"),
            concerts=("concert_id", "count"),
        )
        .sort_values("median_attendance", ascending=True)
        .reset_index(drop=True)
    )

    fig = go.Figure()

    # Range lines (min > max), only meaningful for multi-show venues:
    for _, row in venue_df.iterrows():
        if row["min_attendance"] == row["max_attendance"]:
            continue
        fig.add_trace(
            go.Scatter(
                x=[row["min_attendance"], row["max_attendance"]],
                y=[row["concert_label"], row["concert_label"]],
                mode="lines",
                line={
                    "color": color_pallet.OASIS_COLOR_PALLET["light"],
                    "width": 3
                },
                showlegend=False,
                hoverinfo="skip",
            )
        )

    # Median dots, one trace per continent for legend:
    for continent, group in venue_df.groupby("continent"):
        fig.add_trace(
            go.Scatter(
                x=group["median_attendance"],
                y=group["concert_label"],
                mode="markers",
                name=continent,
                marker={
                    "color": color_pallet.CONTINENT_COLORS.get(continent),  # type: ignore (Pylance)
                    "size": 12,
                    "line": {"width": 1, "color": "white"}
                },
                customdata=group[["min_attendance", "max_attendance", "concerts"]].values,
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Attendance: %{x:,}<br>"
                    "Concerts: %{customdata[2]}"
                    "<extra></extra>"
                ),
            )
        )

    # Enforce global venue sort order across all traces:
    venue_order = venue_df["concert_label"].tolist()
    fig.update_layout(
        xaxis_title="Attendance",
        yaxis_title="Venue",
        yaxis={"categoryorder": "array", "categoryarray": venue_order},
        legend_title_text="Continent",
    )

    fig.update_xaxes(tickformat=",")

    return _apply_default_layout(fig, remove_title=True)


def create_attendance_by_country_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a treemap of total estimated attendance per country.
    """

    plot_df = df.copy()
    plot_df["continent"] = plot_df[COUNTRY_COL].map(geo_data.continent_names)
    plot_df["flag"] = plot_df[COUNTRY_COL].map(geo_data.country_flags)

    country_df = (
        plot_df.groupby([COUNTRY_COL, "continent", "flag"], as_index=False)
        .agg(
            total_attendance=(ATTENDANCE_COL, "sum"),
            total_concerts=("concert_id", "count"),
        )
        .sort_values("total_attendance", ascending=False)
    )

    country_df["country_label"] = country_df["flag"] + ' ' + country_df[COUNTRY_COL]

    fig = px.treemap(
        country_df,
        path=["continent", "country_label"],
        values="total_attendance",
        color="continent",
        color_discrete_map=color_pallet.CONTINENT_COLORS,
        custom_data=["total_concerts", COUNTRY_COL],
        labels={
            "continent": "Continent",
            "country_label": "Country",
            "total_attendance": "Total Attendance",
        },
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Total Attendance: %{value:,}<br>"
            "Concerts: %{customdata[0]}"
            "<extra></extra>"
        ),
        texttemplate="<b>%{label}</b><br>%{value:,}",
        textposition="middle center",
    )

    return _apply_default_layout(fig, remove_title=True)


def create_setlist_flow_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a horizontal stacked bar chart showing the setlist flow,
    with each segment representing a song coloured by its album.
    """

    raw_songs = [
        song.strip() for song
        in df[SETLIST_COL].iloc[0].split('|')
    ]

    songs = [
        _clear_song(song)
        for song in raw_songs
        if not song.strip().lower().startswith("song played from tape:")
    ]

    setlist_df = pd.DataFrame({
        "position": range(1, len(songs) + 1),
        "song": songs,
        "album": [_song_to_album(song) for song in songs],
    })

    seen_albums: Set[str] = set()
    fig = go.Figure()

    for _, row in setlist_df.iterrows():
        album = row["album"]
        show_in_legend = album not in seen_albums
        seen_albums.add(album)

        fig.add_trace(
            go.Bar(
                x=[1],
                y=["Setlist"],
                orientation="h",
                name=album,
                marker_color=color_pallet.OASIS_ALBUM_COLORS.get(album, "#ADB5BD"),
                showlegend=show_in_legend,
                legendgroup=album,
                hovertemplate=(
                    f"<b>{row['song']}</b><br>"
                    f"Album: {album}<br>"
                    f"Position: {int(row['position'])}/{len(songs)}"
                    "<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        barmode="stack",
        xaxis={ "visible": False },
        yaxis={ "visible": False },
        legend={
            "orientation": "v",
            "x": 1.02,
            "y": 0.5,
            "yanchor": "middle",
            "font": { "size": 12 },
            "title_text": "Album",
        },
        margin={ "t": 40, "b": 40, "l": 20, "r": 160 },
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return _apply_default_layout(fig, remove_title=True)


def create_song_frequency_by_album_chart(df: pd.DataFrame) -> Figure:
    """
    Creates a donut chart with unique songs frequency by LP/EP.
    """

    plot_df = df.copy()
    album_df = _compute_album_counts(plot_df)
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
            # textinfo="label+value",
            texttemplate="%{label}<br>%{value} song(s)",
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

    return _apply_default_layout(fig, remove_title=True)
