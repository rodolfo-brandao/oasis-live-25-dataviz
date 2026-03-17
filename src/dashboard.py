import pandas as pd
import streamlit as st
import charts_factory


df = pd.read_csv("./data/oasis_live_25.csv")


st.set_page_config(
    page_title="Oasis Live '25 Dashboard",
    page_icon="./assets/cropped-oasis-fav.png",
    layout="wide"
)
st.title(body="Oasis Live '25")
st.markdown(
    body="""
    Data visualization applied to _estimates_ of each concert for the Live '25 World Tour,
    from the English rock band [Oasis](https://en.wikipedia.org/wiki/Oasis_(band)).\n\n
    - Author: [Rodolfo Brandão](https://github.com/rodolfo-brandao)\n\n
    - Source Code: [GitHub](https://github.com/rodolfo-brandao/oasis-live-25-dataviz)\n\n
    - Dataset: [Kaggle](https://www.kaggle.com/datasets/rodolfobrandao95/oasis-live-25/data)
    """
)


with st.container(border=True):
    # ===== Section 1 (container) =====
    st.subheader(
        body="Main Statistics"
    )

    (
        sec1_col1,
        sec1_col2,
        sec1_col3,
        sec1_col4,
    ) = st.columns(4, gap="small")

    with sec1_col1:
        st.metric(
            label="🗓️ First Concert Date",
            value=pd.to_datetime(
                df["date"], errors="coerce"
            ).min().strftime(format="%B %d, %Y")
        )

    with sec1_col2:
        st.metric(
            label="🗓️ Last Concert Date",
            value=pd.to_datetime(
                df["date"], errors="coerce"
            ).max().strftime(format="%B %d, %Y")
        )

    with sec1_col3:
        st.metric(
            label="🌎 Total Countries",
            value=len(df.groupby("country_or_constituent_country").sum())
        )

    with sec1_col4:
        st.metric(
            label="🎸 Total Concerts",
            value=len(df)
        )

    # ===== Section 2 (container) =====
    (
        sec2_col1,
        sec2_col2,
        sec2_col3,
        sec2_col4
    ) = st.columns(4, gap="small")

    with sec2_col1:
        st.metric(
            label="📍 Country with Most Concerts",
            value=df["country_or_constituent_country"].value_counts().idxmax()
        )

    with sec2_col2:
        st.metric(
            label="🎫 Avg. Ticket Price (USD)",
            value="$" + str(df["avg_ticket_price_usd_pollstar"].unique()[0])
        )

    with sec2_col3:
        st.metric(
            label="🔻 Lowest Attendance",
            value=f"{df["attendance_estimated_per_concert"].min():,}"
        )

    with sec2_col4:
        st.metric(
            label="🔺 Highest Attendance",
            value=f"{df["attendance_estimated_per_concert"].max():,}"
        )


# ===== Section 3 =====
(
    sec3_col1,
    sec3_col2
) = st.columns(2, gap="medium", border=True)

with sec3_col1:
    st.subheader(
        body="Concert Distribution by Continent"
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
(
    sec4_col1,
    sec4_col2
) = st.columns(2, gap="medium", border=True)

with sec4_col1:
    st.subheader(
        body="Estimated Attendance"
    )

    st.plotly_chart(
        figure_or_data=charts_factory.create_attendance_by_concert_chart(df)
    )

with sec4_col2:
    st.subheader(
        body="Crowd Progress by Concert"
    )

    st.plotly_chart(
        figure_or_data=charts_factory.create_attendance_progress_chart(df)
    )


# ===== Section X ===== (last one)
with st.container(border=True):
    st.subheader(
        body="Raw Data Sample"
    )

    columns_to_drop = [
        "concert_id",
        "attendance_scope_note",
        "gross_reported_usd_per_concert",
        "gross_estimation_note",
        "source_tour_dates_attendance_url",
        "source_tour_financials_url",
        "source_setlist_url"
    ]

    st.dataframe(
        data=df.drop(columns=columns_to_drop).head(n=10)
    )
