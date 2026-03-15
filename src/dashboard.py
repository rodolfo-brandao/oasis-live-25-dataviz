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
    Data visualization applied to _estimates_ of each concert for Oasis' 2025 World Tour.\n\n
    - Author: [Rodolfo Brandão](https://github.com/rodolfo-brandao)\n\n
    - Source Code: [GitHub](https://github.com/rodolfo-brandao/oasis-live-25-dataviz)\n\n
    - Dataset: [Kaggle](https://www.kaggle.com/datasets/rodolfobrandao95/oasis-live-25/data)
    """
)


# ===== Section 01 =====
section1_col1, section1_col2 = st.columns(2, gap="medium")

with section1_col1:
    st.subheader(
        body="Main Statistics"
    )

    with st.container(border=True, width="stretch"):
        col1, col2 = st.columns(2, gap="medium")

        with col1:
            st.metric(
                label="🗓️ First Concert Date",
                value=pd.to_datetime(
                    df["date"], errors="coerce"
                ).min().strftime(format="%B %d, %Y"),
                border=True
            )

            st.metric(
                label="🌎 Total Countries",
                value=len(df.groupby("country_or_constituent_country").sum()),
                border=True
            )

            st.metric(
                label="🔻 Lowest Attendance",
                value=f"{df["attendance_estimated_per_concert"].min():,}",
                border=True
            )

            st.metric(
                label="🎫 Avg. Ticket Price (USD)",
                value=df["avg_ticket_price_usd_pollstar"].unique()[0],
                border=True
            )

        with col2:
            st.metric(
                label="🗓️ Last Concert Date",
                value=pd.to_datetime(
                    df["date"], errors="coerce"
                ).max().strftime(format="%B %d, %Y"),
                border=True
            )

            st.metric(
                label="📍 Country with Most Concerts",
                value=df["country_or_constituent_country"].value_counts().idxmax(),
                border=True
            )

            st.metric(
                label="🔺 Highest Attendance",
                value=f"{df["attendance_estimated_per_concert"].max():,}",
                border=True
            )

            st.metric(
                label="🎸 Total Concerts",
                value=len(df),
                border=True
            )

with section1_col2:
    st.subheader(
        body="Total Concerts per Country"
    )

    with st.container(border=True, width="stretch"):
        st.plotly_chart(
            figure_or_data=charts_factory.create_concerts_by_country_chart(df)
        )


# ===== Section 02 =====
section2_col1, section2_col2 = st.columns(2, gap="medium")

with section2_col1:
    st.subheader(
        body="Attendance per Concert"
    )

    with st.container(border=True):
        st.plotly_chart(
            figure_or_data=charts_factory.create_attendance_by_concert_chart(df)
        )

with section2_col2:
    st.subheader(
        body="Crowd Progress by Concert"
    )

    with st.container(border=True):
        st.plotly_chart(
            figure_or_data=charts_factory.create_attendance_progress_chart(df)
        )


# ===== Section X ===== (last one)
st.subheader(
    body="Raw Data Sample"
)

with st.container(border=True):
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
