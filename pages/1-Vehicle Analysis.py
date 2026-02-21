import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Vehicle Analysis", layout="wide")

st.title("Vehicle-class Analysis — Operational & Quality Metrics")

st.markdown(
    """
    This page provides a concise, reproducible analysis of performance by vehicle class. Metrics include booking volume, completion rate, and customer satisfaction. The visualizations and summary table are intended for academic reporting and operational review.
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
    # Core KPIs
    total_rides = int(len(df))
    modal_vehicle = df["vehicle_type"].mode().iloc[0] if "vehicle_type" in df.columns else "N/A"
    overall_completion = float(df["iscompleted"].mean() * 100) if "iscompleted" in df.columns else float("nan")
    mean_booking_value = float(df["booking_value"].replace([np.inf, -np.inf], np.nan).dropna().mean()) if "booking_value" in df.columns else float("nan")
    mean_distance = float(df["ride_distance"].replace([np.inf, -np.inf], np.nan).dropna().mean()) if "ride_distance" in df.columns else float("nan")

    a, b, c, d = st.columns([1.4, 1.2, 1.2, 1.2])
    a.metric("Total records", f"{total_rides:,}")
    b.metric("Modal vehicle class", f"{modal_vehicle}")
    c.metric("Overall completion rate", f"{overall_completion:.2f}%")
    d.metric("Mean booking value", f"₹{mean_booking_value:,.2f}")

    # Summarize by vehicle type
    summary = (
        df.groupby("vehicle_type")
        .agg(
            bookings=("vehicle_type", "count"),
            completion_rate=("iscompleted", "mean"),
            avg_customer_rating=("customer_rating", "mean"),
            avg_booking_value=("booking_value", "mean"),
            avg_distance=("ride_distance", "mean"),
        )
        .reset_index()
    )

    # Convert completion to percent for readability
    if "completion_rate" in summary.columns:
        summary["completion_rate_pct"] = summary["completion_rate"] * 100

    # Order by bookings descending
    summary = summary.sort_values("bookings", ascending=False)

    # Display summary table (select original columns then rename for presentation)
    st.subheader("Per‑vehicle summary")
    display_cols = [
        "vehicle_type",
        "bookings",
        "completion_rate_pct",
        "avg_customer_rating",
        "avg_booking_value",
        "avg_distance",
    ]
    display_df = summary[display_cols].rename(
        columns={
            "vehicle_type": "Vehicle",
            "bookings": "Bookings",
            "completion_rate_pct": "Completion (%)",
            "avg_customer_rating": "Avg customer rating",
            "avg_booking_value": "Avg booking value",
            "avg_distance": "Avg distance (km)",
        }
    )
    st.dataframe(display_df, use_container_width=True)

    # Booking volume chart
    st.subheader("Booking volume by vehicle class")
    fig1 = px.bar(
        summary,
        x="vehicle_type",
        y="bookings",
        title="Total bookings by vehicle class",
        labels={"vehicle_type": "Vehicle class", "bookings": "Number of bookings"},
        color="bookings",
        color_continuous_scale="Blues",
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

    # Completion rate chart (percentage)
    st.subheader("Completion rate by vehicle class")
    fig2 = px.bar(
        summary,
        x="vehicle_type",
        y="completion_rate_pct",
        title="Completion rate (%) by vehicle class",
        labels={"completion_rate_pct": "Completion rate (%)", "vehicle_type": "Vehicle class"},
        color="completion_rate_pct",
        color_continuous_scale="Greens",
    )
    fig2.update_layout(yaxis=dict(ticksuffix="%"), showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

    # Customer satisfaction chart
    st.subheader("Customer satisfaction by vehicle class")
    fig3 = px.bar(
        summary,
        x="vehicle_type",
        y="avg_customer_rating",
        title="Mean customer rating by vehicle class",
        labels={"avg_customer_rating": "Mean customer rating (1-5)"},
        color="avg_customer_rating",
        color_continuous_scale="OrRd",
    )
    fig3.update_layout(showlegend=False, yaxis=dict(range=[0, 5]))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(
        """
        **Notes.** Completion rate is defined as the proportion of rides with `iscompleted == 1`. Aggregations are unweighted simple means unless otherwise noted. For publication-ready figures, I can export SVG/PNG with captions and a brief methods paragraph.
        """
    )