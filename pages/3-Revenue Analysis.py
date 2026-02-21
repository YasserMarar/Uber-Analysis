import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Revenue Analysis", layout="wide")

st.title("Revenue & Pricing Analysis")

st.markdown(
    """
    Revenue-oriented summaries: total and per-class revenue, relationships between distance and fare, and price-per-km distribution. These outputs are formatted for reproducible reporting.
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
    total_revenue = float(df["booking_value"].sum()) if "booking_value" in df.columns else float("nan")
    avg_fare = float(df["booking_value"].replace([np.inf, -np.inf], np.nan).dropna().mean()) if "booking_value" in df.columns else float("nan")
    median_price_per_km = float(df["price_per_km"].replace([np.inf, -np.inf], np.nan).dropna().median()) if "price_per_km" in df.columns else float("nan")
    top_revenue_vehicle = (
        df.groupby("vehicle_type")["booking_value"].sum().sort_values(ascending=False).index[0]
        if "vehicle_type" in df.columns and "booking_value" in df.columns
        else "N/A"
    )

    c1, c2, c3, c4 = st.columns([1.2, 1.2, 1.2, 1.2])
    c1.metric("Total revenue", f"₹{total_revenue:,.2f}")
    c2.metric("Mean fare per booking", f"₹{avg_fare:,.2f}")
    c3.metric("Median price per km", f"₹{median_price_per_km:,.2f}")
    c4.metric("Top revenue vehicle", f"{top_revenue_vehicle}")

    # Revenue by vehicle class summary
    st.subheader("Revenue by vehicle class")
    rev_by_vehicle = (
        df.groupby("vehicle_type")
        .agg(total_revenue=("booking_value", "sum"), bookings=("booking_value", "count"), avg_fare=("booking_value", "mean"))
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )
    st.dataframe(rev_by_vehicle, use_container_width=True)

    fig1 = px.bar(
        rev_by_vehicle,
        x="vehicle_type",
        y="total_revenue",
        title="Total revenue by vehicle class",
        labels={"total_revenue": "Total revenue (local currency)", "vehicle_type": "Vehicle class"},
        color="total_revenue",
        color_continuous_scale="Blues",
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

    # Distance vs fare scatter (sampled)
    st.subheader("Distance vs fare relationship")
    sample_n = min(4000, len(df))
    sample_df = df.sample(sample_n, random_state=42)
    fig2 = px.scatter(
        sample_df,
        x="ride_distance",
        y="booking_value",
        title=f"Distance vs fare (sample n={sample_n})",
        labels={"ride_distance": "Distance (km)", "booking_value": "Booking value"},
        opacity=0.6,
        color="vehicle_type" if "vehicle_type" in df.columns else None,
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Price per km distribution
    st.subheader("Price per km distribution")
    fig3 = px.histogram(df.replace([np.inf, -np.inf], np.nan).dropna(subset=["price_per_km"]), x="price_per_km", nbins=40, title="Price per km")
    fig3.update_layout(xaxis_title="Price per km", yaxis_title="Count")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(
        """
        **Notes.** Revenue totals are raw sums. For robust comparisons use median or trimmed-mean and inspect outliers. I can add revenue per driver, per-hour revenue heatmaps, or publishable figure exports on request.
        """
    )