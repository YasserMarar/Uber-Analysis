import streamlit as st
import pandas as pd

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="Ride Booking Dashboard",
    layout="wide",
    page_icon="🚖"
)

# ==============================
# Custom Styling (Professional Look)
# ==============================
st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.kpi-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
    text-align: center;
}

.kpi-title {
    font-size: 18px;
    color: #6c757d;
}

.kpi-value {
    font-size: 28px;
    font-weight: bold;
    color: #1f77b4;
}

.section-title {
    font-size: 26px;
    font-weight: bold;
    color: #2c3e50;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# Load Data
# ==============================
df = pd.read_csv("cleaned.csv")

# ==============================
# Header Section
# ==============================
st.markdown("<h1 style='color:#1f77b4;'>🚖 Ride Booking Analysis Dashboard</h1>", unsafe_allow_html=True)

st.markdown("""
Welcome to the Ride Booking Business Intelligence Dashboard.  
This dashboard provides insights into booking performance, revenue trends,
vehicle demand, and customer satisfaction metrics.
""")

# ==============================
# KPI Calculations
# ==============================
total_rides = len(df)
completed_rides = df["iscompleted"].sum()
completion_rate = (completed_rides / total_rides) * 100
total_revenue = df["booking_value"].sum()
avg_booking_value = df["booking_value"].mean()
avg_customer_rating = df["customer_rating"].mean()

# ==============================
# KPI Section
# ==============================
st.markdown("<div class='section-title'>📊 Key Performance Indicators</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Total Rides</div>
        <div class='kpi-value'>{total_rides:,}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='kpi-card' style="margin-top:15px;">
        <div class='kpi-title'>Completion Rate</div>
        <div class='kpi-value'>{completion_rate:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Total Revenue</div>
        <div class='kpi-value'>${total_revenue:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='kpi-card' style="margin-top:15px;">
        <div class='kpi-title'>Avg Booking Value</div>
        <div class='kpi-value'>${avg_booking_value:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-title'>Completed Rides</div>
        <div class='kpi-value'>{completed_rides:,}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='kpi-card' style="margin-top:15px;">
        <div class='kpi-title'>Avg Customer Rating</div>
        <div class='kpi-value'>{avg_customer_rating:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# Dataset Description Section
# ==============================
st.markdown("<div class='section-title'>📖 Dataset Description</div>", unsafe_allow_html=True)

st.markdown("""
This dataset contains detailed ride-level information including:

- Booking status & operational performance  
- Revenue & pricing metrics  
- Ride distance & time attributes  
- Customer and driver satisfaction ratings  
- Payment behavior  
""")

# ==============================
# Column Descriptions
# ==============================
st.markdown("<div class='section-title'>📂 Columns Overview</div>", unsafe_allow_html=True)

column_info = {
    "date": "Date of the booking.",
    "time": "Exact booking timestamp.",
    "booking_status": "Ride status (Completed / Cancelled).",
    "vehicle_type": "Vehicle category selected.",
    "pickup_location": "Ride starting point.",
    "drop_location": "Ride destination.",
    "avg_vtat": "Average Vehicle Turnaround Time.",
    "avg_ctat": "Average Customer Turnaround Time.",
    "booking_value": "Total ride fare.",
    "ride_distance": "Distance traveled (km).",
    "driver_ratings": "Driver rating score.",
    "customer_rating": "Customer satisfaction rating.",
    "payment_method": "Payment method used.",
    "price_per_km": "Fare per kilometer.",
    "day": "Day of the week.",
    "month": "Booking month.",
    "period": "Time segment (Morning, Afternoon, Evening, Night).",
    "hour": "Hour of the day (0–23).",
    "iscompleted": "1 = Completed, 0 = Not Completed."
}

for col, desc in column_info.items():
    st.markdown(f"**{col}** — {desc}")