import pandas as pd
import streamlit as st
import charts_factory


df = pd.read_csv("./data/oasis_live_25.csv")


st.set_page_config(
    page_title="Oasis Live '25 — Dashboard",
    page_icon="./assets/cropped-oasis-fav.png",
    layout="wide"
)
st.title(body="Oasis Live '25")
st.markdown(
    body="""
        Data visualization applied to _estimates_ of each concert for the Live '25 World Tour.\n\n
        - Author: [Rodolfo Brandão](https://github.com/rodolfo-brandao)\n\n
        - Source Code: [GitHub](https://github.com/rodolfo-brandao/oasis-live-25-dataviz)\n\n
        - Dataset: [Kaggle](https://www.kaggle.com/datasets/rodolfobrandao95/oasis-live-25/data)
    """
)


with st.container(border=True):
    # ===== Section 1 (container) =====
    st.subheader(
        body="Summary"
    )

    (
        sec1_col1,
        sec1_col2,
        sec1_col3,
        sec1_col4,
        sec1_col5
    ) = st.columns(5, gap="small")

    with sec1_col1:
        st.metric(
            label="🗓️ First Concert Date",
            value=pd.to_datetime(df["date"], errors="coerce")
            .min().strftime(format="%B %d, %Y")
        )

    with sec1_col2:
        st.metric(
            label="🗓️ Last Concert Date",
            value=pd.to_datetime(df["date"], errors="coerce")
                .max().strftime(format="%B %d, %Y")
        )

    with sec1_col3:
        st.metric(
            label="🎸 Total Concerts",
            value=len(df)
        )

    with sec1_col4:
        st.metric(
            label="🌎 Total Countries",
            value=df['country_or_constituent_country'].nunique()
        )

    with sec1_col5:
        st.metric(
            label="🏙️ Total Cities",
            value=df['city'].nunique()
        )

    # ===== Section 2 (container) =====
    (
        sec2_col1,
        sec2_col2,
        sec2_col3,
        sec2_col4,
        sec2_col5
    ) = st.columns(5, gap="small")

    with sec2_col1:
        st.metric(
            label="💰 Total Estimated Gross (USD)",
            value=f"${df["gross_estimated_usd_per_concert"].sum():,.0f}"
        )

    with sec2_col2:
        st.metric(
            label="🎫 Avg. Ticket Price (USD)",
            value=f"${df["avg_ticket_price_usd_pollstar"].unique()[0]}"
        )

    with sec2_col3:
        st.metric(
            label="🔻 Lowest Attendance per Concert",
            value=f"{df["attendance_estimated_per_concert"].min():,}"
        )

    with sec2_col4:
        st.metric(
            label="🔺 Highest Attendance per Concert",
            value=f"{df["attendance_estimated_per_concert"].max():,}"
        )

    with sec2_col5:
        st.metric(
            label="🧑‍🧑‍🧒‍🧒 Total Attendance",
            value=f"{df["attendance_estimated_per_concert"].sum():,}"
        )


# ===== Section 3 =====
(
    sec3_col1,
    sec3_col2
) = st.columns(2, gap="medium", border=True)

with sec3_col1:
    st.subheader(
        body="Total Concerts per Continent"
    )

    st.plotly_chart(
        figure_or_data=charts_factory.create_concerts_by_continent_chart(df)
    )

with sec3_col2:
    st.subheader(
        body="Total Concerts per Country"
    )

    st.plotly_chart(
        figure_or_data=charts_factory.create_concerts_by_country_chart(df)
    )


# ===== Section 4 =====
with st.container(border=True):
    st.subheader(
        body="Estimated Attendance per Concert"
    )

    st.plotly_chart(
        figure_or_data=charts_factory.create_attendance_by_venue_chart(df)
    )


# ===== Section 5 =====
with st.container(border=True):
    st.subheader(
        body="Estimated Attendance per Country"
    )

    st.plotly_chart(
        figure_or_data=charts_factory.create_attendance_by_country_chart(df)
    )


# ===== Section 6 =====
(
    sec6_col1,
    sec6_col2
) = st.columns(2, gap="medium", border=True)

with sec6_col1:
    st.subheader(
        body="Live '25 Setlist — Songs by LP/EP"
    )

    st.markdown(
        body="""
            All setlists in the tour are the same, except tape intro songs.\n
            _(hover the mouse for more details)_
        """
    )

    st.plotly_chart(
        figure_or_data=charts_factory.create_setlist_flow_chart(df)
    )

with sec6_col2:
    st.subheader(
        body="LP/EP Share in Setlist"
    )

    st.plotly_chart(
        figure_or_data=charts_factory.create_song_frequency_by_album_chart(df)
    )


# ===== Section 7 =====
with st.container(border=True):
    st.subheader(
        body="Raw Data"
    )

    cols_to_drop = [
        "concert_id",
        "attendance_scope_note",
        "gross_reported_usd_per_concert",
        "gross_estimation_note",
        "source_tour_dates_attendance_url",
        "source_tour_financials_url",
        "source_setlist_url",
        "setlist_variant",
        "setlist"
    ]

    st.dataframe(
        data=df.drop(columns=cols_to_drop),
        height=400,  # Enables vertical scroll
        width="stretch"
    )
