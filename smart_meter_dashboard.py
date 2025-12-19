import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import random

# ------------------------------
# Household Consumption Simulation
# ------------------------------
def generate_hourly_data(profile="family"):
    base = np.random.normal(0.3, 0.05, 24)
    if profile == "family":
        base[6:8] += np.random.normal(1.5, 0.2, 2)
        base[17:22] += np.random.normal(2.0, 0.3, 5)
    elif profile == "student":
        base[10:14] += np.random.normal(1.0, 0.3, 4)
        base[22:24] += np.random.normal(1.2, 0.2, 2)
    elif profile == "retired":
        base[8:18] += np.random.normal(0.8, 0.2, 10)
    elif profile == "working_couple":
        base[6:7] += np.random.normal(1.0, 0.2, 1)
        base[18:21] += np.random.normal(1.8, 0.3, 3)
    base = np.clip(base, 0.1, None)
    hours = [f"{h}:00" for h in range(24)]
    return pd.DataFrame({"Hour": hours, "Consumption": base})

# ------------------------------
# Privacy Mechanism
# ------------------------------
def apply_privacy(data, method="Daily Aggregation", noise_scale=0.1):
    if method == "Raw Hourly":
        return data.copy()
    elif method == "Daily Aggregation":
        total = data["Consumption"].sum()
        return pd.DataFrame({"Hour": ["Total"], "Consumption": [total]})
    elif method == "Differential Privacy":
        noisy = data.copy()
        noise = np.random.laplace(0, noise_scale, len(noisy))
        noisy["Consumption"] += noise
        noisy["Consumption"] = noisy["Consumption"].clip(lower=0.05)
        return noisy

# ------------------------------
# Synthetic Appliance Data (NILM)
# ------------------------------
def generate_appliance_traces():
    hours = np.arange(24)
    fridge = np.random.normal(0.15, 0.02, 24)
    lights = np.zeros(24)
    lights[6:8] += np.random.normal(0.3, 0.05, 2)
    lights[18:23] += np.random.normal(0.4, 0.05, 5)
    washing_machine = np.zeros(24)
    start = np.random.choice([8, 9, 18, 19])
    washing_machine[start:start+2] = np.random.normal(0.8, 0.1, 2)
    ev = np.zeros(24)
    if np.random.rand() > 0.5:
        ev[22:24] = np.random.normal(2.5, 0.2, 2)
    total = fridge + lights + washing_machine + ev
    return pd.DataFrame({
        "Hour": [f"{h}:00" for h in hours],
        "Fridge": fridge,
        "Lights": lights,
        "WashingMachine": washing_machine,
        "EV": ev,
        "Total": total
    })

# ------------------------------
# EV Detection Based on Noise
# ------------------------------
def detect_ev_based_on_noise(noise_scale, threshold=0.1):
    # If noise_scale is very low (≤ threshold), EV is detected
    return noise_scale <= threshold

# ------------------------------
# Helper: Plot
# ------------------------------
def plot_line(data, x_col, y_col, title):
    fig = px.line(data, x=x_col, y=y_col, title=title, markers=True)
    fig.update_layout(template="plotly_white")
    return fig

# ------------------------------
# Streamlit App Setup
# ------------------------------
st.set_page_config(page_title="Smart Meter Privacy Dashboard", layout="wide")
st.title("⚡Smart Meter Privacy Dashboard")

# ------------------------------
# Sidebar: Random Seed & Unified Noise
# ------------------------------
seed = st.sidebar.number_input("Random Seed", min_value=0, max_value=9999, value=42)
np.random.seed(seed)
random.seed(seed)

st.sidebar.header("Privacy Control")
noise_scale_global = st.sidebar.slider("Noise Scale for Privacy (kWh)", 0.0, 1.0, 0.3, 0.05)

tab1, tab2, tab4 = st.tabs([
    "🏠 Simulation",
    "🔐 Privacy vs Utility",
    "🚗 NILM (Appliance Detection)"
])

# ------------------------------
# Tab 1: Live Household Simulation
# ------------------------------
with tab1:
    st.header("Household Consumption Simulation")
    profile = st.selectbox("Select Household Profile", ["family", "student", "retired", "working_couple"])
    data = generate_hourly_data(profile)

    play_animation = st.checkbox("▶️ Play Live Simulation")
    if play_animation:
        placeholder = st.empty()
        for i in range(24):
            fig = plot_line(data.iloc[:i+1], "Hour", "Consumption", f"{profile.capitalize()} Household Consumption")
            placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(0.2)
    else:
        hour_slider = st.slider("Select Hour", 0, 23, 0)
        stream_data = data.iloc[:hour_slider+1]
        st.plotly_chart(plot_line(stream_data, "Hour", "Consumption", f"{profile.capitalize()} Household Consumption"), use_container_width=True)

# ------------------------------
# Tab 2: Privacy vs Utility
# ------------------------------
with tab2:
    st.header("Privacy-Preserving Methods")
    method = st.radio("Select Privacy Method", ["Raw Hourly", "Daily Aggregation", "Differential Privacy"])
    noise_scale = st.slider("Noise Scale (for Differential Privacy)", 0.01, 0.5, 0.1)
    data = generate_hourly_data("family")
    private_data = apply_privacy(data, method, noise_scale)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_line(data, "Hour", "Consumption", "Original Hourly Data"), use_container_width=True)
    with col2:
        if method == "Daily Aggregation":
            fig2 = px.bar(private_data, x="Hour", y="Consumption", text="Consumption", title="Daily Aggregation")
            fig2.update_traces(texttemplate='%{text:.2f} kWh', textposition="outside")
            fig2.update_layout(template="plotly_white")
        else:
            fig2 = plot_line(private_data, "Hour", "Consumption", f"{method}")
        st.plotly_chart(fig2, use_container_width=True)

# ------------------------------
# Tab 4: NILM Appliance Detection (Unified Noise)
# ------------------------------
with tab4:
    st.header("NILM Appliance Detection (Unified Noise)")
    data = generate_appliance_traces()

    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.area(data, x="Hour", y=["Fridge", "Lights", "WashingMachine", "EV"], title="Appliance-Level Traces (Ground Truth)")
        fig1.update_layout(template="plotly_white", yaxis_title="kWh")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(plot_line(data, "Hour", "Total", "Total Household Consumption"), use_container_width=True)

    # Apply unified noise
    private_data = data.copy()
    private_data["Total"] = private_data["Total"] + np.random.laplace(0, noise_scale_global, len(private_data))
    private_data["Total"] = private_data["Total"].clip(lower=0.05)

    # EV detection based on noise scale
    ev_detected_noisy = detect_ev_based_on_noise(noise_scale_global, threshold=0.0)  # detected if noise = 0

    fig3 = plot_line(private_data, "Hour", "Total", f"Noisy Total Consumption (Noise={noise_scale_global})")
    st.plotly_chart(fig3, use_container_width=True)

    if ev_detected_noisy:
        st.warning(f"⚠️ EV detected due to low/no noise.")
    else:
        st.success(f"✅ EV hidden due to sufficient noise.")
