
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time

# -----------------------------------
# ASTRA-MED CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="ASTRA-MED | Mission Health",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------------
# CUSTOM DESIGN
# -----------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #07111F;
    color: #EAF4FF;
}

[data-testid="stSidebar"] {
    background-color: #0D1B2A;
}

.metric-card {
    background: linear-gradient(135deg, #102A43, #163B59);
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #245477;
}

.metric-title {
    color: #A9C7DF;
    font-size: 14px;
}

.metric-value {
    color: #FFFFFF;
    font-size: 30px;
    font-weight: bold;
}

.status {
    color: #43E6A1;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("🚀 ASTRA-MED")
st.sidebar.caption("ASTRONAUT HEALTH INTELLIGENCE")
st.sidebar.divider()

page = st.sidebar.radio(
    "MISSION NAVIGATION",
    [
        "Mission Overview",
        "Health Monitor",
        "AI Health Insights",
        "Space Environment",
        "Wellness Centre"
    ]
)

st.sidebar.divider()
st.sidebar.success("SIMULATION MODE")
st.sidebar.caption("All readings are demonstration data.")

# -----------------------------------
# SIMULATED HEALTH DATA
# -----------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

def generate_readings():
    return {
        "Heart Rate": int(np.random.normal(72, 4)),
        "SpO2": round(np.random.normal(98, 0.5), 1),
        "Temperature": round(np.random.normal(36.8, 0.2), 1),
        "Respiratory Rate": int(np.random.normal(16, 1)),
        "Blood Pressure": f"{np.random.randint(110, 
121)}/{np.random.randint(70, 81)}"
    }

if "current" not in st.session_state:
    st.session_state.current = generate_readings()

# -----------------------------------
# HEADER
# -----------------------------------

st.markdown("# 🚀 ASTRA-MED")
st.caption("ADVANCED ASTRONAUT HEALTH MONITORING SYSTEM")

st.markdown(
    "MISSION: ARTEMIS DEMO-01  |  CREW MEMBER: ASTRONAUT-001"
)

st.divider()

# -----------------------------------
# METRIC CARD
# -----------------------------------

def metric_card(title, value, unit):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-title">{unit}</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------
# MISSION OVERVIEW
# -----------------------------------

if page == "Mission Overview":

    st.subheader("🛰️ Mission Control Centre")

    a, b, c = st.columns(3)

    a.metric("MISSION STATUS", "ACTIVE")
    b.metric("CREW MEMBERS", "01")
    c.metric("SYSTEM STATUS", "ONLINE")

    st.subheader("❤️ Astronaut Health Overview")

    r = st.session_state.current

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("HEART RATE", r["Heart Rate"], "BPM")

    with col2:
        metric_card("BLOOD OXYGEN", r["SpO2"], "%")

    with col3:
        metric_card("BODY TEMPERATURE", r["Temperature"], "°C")

    col4, col5 = st.columns(2)

    with col4:
        metric_card("RESPIRATORY RATE", r["Respiratory Rate"], 
"Breaths/min")

    with col5:
        metric_card("BLOOD PRESSURE", r["Blood Pressure"], "mmHg")

    st.divider()

    st.success("Mission dashboard operational.")

# -----------------------------------
# HEALTH MONITOR
# -----------------------------------

elif page == "Health Monitor":

    st.subheader("❤️ Live Health Monitoring")

    if st.button("🔄 Generate New Health Reading"):
        st.session_state.current = generate_readings()
        st.session_state.history.append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            **st.session_state.current
        })

    r = st.session_state.current

    x, y, z = st.columns(3)

    with x:
        metric_card("HEART RATE", r["Heart Rate"], "BPM")

    with y:
        metric_card("SpO2", r["SpO2"], "%")

    with z:
        metric_card("TEMPERATURE", r["Temperature"], "°C")

    st.caption("Demonstration readings only. Not medical measurements.")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)

        st.subheader("Health History")

        st.dataframe(df, use_container_width=True)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["Time"],
            y=df["Heart Rate"],
            mode="lines+markers",
            name="Heart Rate"
        ))

        fig.update_layout(
            title="Heart Rate Trend",
            template="plotly_dark",
            paper_bgcolor="#07111F",
            plot_bgcolor="#0D1B2A"
        )

        st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# AI HEALTH INSIGHTS
# -----------------------------------

elif page == "AI Health Insights":

    st.subheader("🧠 Health Intelligence Centre")

    r = st.session_state.current

    st.info("Analyzing simulated astronaut readings...")

    st.write("Heart Rate:", r["Heart Rate"], "BPM")
    st.write("Blood Oxygen:", r["SpO2"], "%")
    st.write("Temperature:", r["Temperature"], "°C")

    st.markdown("### Health Monitoring")

    st.write(
        "This prototype displays readings and can be extended "
        "with personal baseline comparison and anomaly detection."
    )

    st.warning(
        "No medical diagnosis is performed. "
        "Use mission-approved medical protocols."
    )

# -----------------------------------
# SPACE ENVIRONMENT
# -----------------------------------

elif page == "Space Environment":

    st.subheader("🌎 Spacecraft Environment")

    col1, col2, col3 = st.columns(3)

    col1.metric("CABIN TEMPERATURE", "22.5 °C")
    col2.metric("HUMIDITY", "45%")
    col3.metric("CO2", "650 ppm")

    st.info("Environmental values are simulated.")

# -----------------------------------
# WELLNESS CENTRE
# -----------------------------------

elif page == "Wellness Centre":

    st.subheader("🧑‍🚀 Astronaut Wellness Centre")

    sleep = st.slider("Sleep duration (hours)", 0, 12, 8)

    stress = st.select_slider(
        "How stressed do you feel?",
        options=["Very Low", "Low", "Moderate", "High", "Very High"]
    )

    fatigue = st.select_slider(
        "How fatigued do you feel?",
        options=["Very Low", "Low", "Moderate", "High", "Very High"]
    )

    if st.button("Save Wellness Check-in"):

        st.success("Wellness check-in recorded.")

        st.write("Sleep:", sleep, "hours")
        st.write("Stress:", stress)
        st.write("Fatigue:", fatigue)

# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(
    "ASTRA-MED | Hackathon Prototype | "
    "Simulated data | Not an official NASA product"
)

