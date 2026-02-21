import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Time Analysis", layout="wide")

st.title("Temporal Analysis — Demand & Seasonality")

st.markdown(
    """
    This page analyses temporal patterns in demand: hourly diurnal cycles, weekly/period breakdowns and monthly seasonality. Figures and tables are formatted for academic reporting.
    """
)


@st.cache_data
def load_data(path: str = "cleaned.csv") -> pd.DataFrame | None:
    try:
        return pd.read_csv(path)
    except Exception:
        return None


df = load_data()
if df is None:
    st.error("cleaned.csv not found. Place the file adjacent to Home.py to enable this page.")
else:
    total = len(df)
    peak_hour = int(df["hour"].mode().iloc[0]) if "hour" in df.columns and not df["hour"].mode().empty else "N/A"
    modal_period = df["period"].mode().iloc[0] if "period" in df.columns and not df["period"].mode().empty else "N/A"

    c1, c2, c3 = st.columns([1.2, 1.2, 1.2])
    c1.metric("Total records", f"{total:,}")
    c2.metric("Peak hour (modal)", f"{peak_hour}:00")
    c3.metric("Modal period", f"{modal_period}")

    # Hourly bookings (aggregate)
    st.subheader("Hourly demand profile")
    hourly = df.groupby("hour").size().reset_index(name="count")
    hourly = hourly.sort_values("hour")
    fig1 = px.line(hourly, x="hour", y="count", markers=True, title="Bookings by hour (diurnal cycle)")
    fig1.update_layout(xaxis_title="Hour of day (0-23)", yaxis_title="Number of bookings")
    st.plotly_chart(fig1, use_container_width=True)

    # Weekly / period breakdown
    st.subheader("Bookings by time-of-day period")
    period = df["period"].value_counts().reindex(["Morning", "Afternoon", "Evening", "Night"]).reset_index()
    period.columns = ["period", "count"]
    fig3 = px.bar(period, x="period", y="count", title="Bookings by coarse period of day", color="count", color_continuous_scale="Viridis")
    st.plotly_chart(fig3, use_container_width=True)

    # Monthly trend (sorted chronologically if month numeric)
    st.subheader("Monthly booking trend")
    monthly = df.groupby("month").size().reset_index(name="count")
    try:
        monthly["month_order"] = monthly["month"].astype(int)
        monthly = monthly.sort_values("month_order")
        xcol = "month_order"
        fig2 = px.line(monthly, x=xcol, y="count", title="Monthly booking trend")
        fig2.update_layout(xaxis_title="Month (1-12)")
    except Exception:
        fig2 = px.line(monthly, x="month", y="count", title="Monthly booking trend")
    fig2.update_layout(yaxis_title="Number of bookings")
    st.plotly_chart(fig2, use_container_width=True)

    # Hourly + period summary table for reporting
    st.subheader("Summary table: hourly and period aggregates")
    summary = (
        df.groupby(["hour", "period"]) 
        .size()
        .reset_index(name="bookings")
        .sort_values(["hour", "period"])
    )
    st.dataframe(summary, use_container_width=True)

    st.markdown(
        """
        **Notes.** Hourly and monthly aggregations are simple counts. For formal analysis, consider smoothing (7‑day rolling) or seasonal decomposition. If you want, I can add confidence intervals, decomposition, or exported figures.
        """
    )