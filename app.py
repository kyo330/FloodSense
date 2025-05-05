import streamlit as st
from streamlit_folium import st_folium
import folium
from datetime import datetime
import pytz

from src.data_loader import load_infrastructure_data
from src.simulation import simulate_risk
from src.map_utils import create_risk_map
from src.rainfall_loader import (
    fetch_current_rainfall_college_station,
    simulate_rainfall_data
)

def main():
    st.set_page_config(page_title="FloodSense", layout="wide")
    st.title("🌊 FloodSense: Real-Time Flood Risk Estimator (College Station)")

    # Initialize session state
    if "run_sim" not in st.session_state:
        st.session_state.run_sim = False
    if "simulate_mode" not in st.session_state:
        st.session_state.simulate_mode = False
    if "rainfall_data" not in st.session_state:
        st.session_state.rainfall_data = None

    # Home button
    if st.button("🏠 Go to Home"):
        st.session_state.run_sim = False
        st.session_state.simulate_mode = False
        st.session_state.rainfall_data = None
        st.rerun()

    # Sidebar Inputs
    st.sidebar.header("User Inputs")
    location = st.sidebar.text_input("Location", "College Station, TX")
    infra_types = st.sidebar.multiselect(
        "Infrastructure Types", 
        ["Private Well", "Treatment Plant", "Sewage Station"],
        default=["Private Well"]
    )

    st.sidebar.markdown("### 🌧️ Simulate Rainfall (optional)")
    simulate = st.sidebar.checkbox("Use Simulated Rainfall", value=st.session_state.simulate_mode)
    st.session_state.simulate_mode = simulate

    if simulate:
        if st.session_state.rainfall_data is None:
            min_rain = st.sidebar.slider("Min Rainfall (mm)", 0, 100, 10)
            max_rain = st.sidebar.slider("Max Rainfall (mm)", min_rain, 200, 60)
            sim_days = st.sidebar.slider("Days to Simulate", 1, 14, 7)
            st.session_state.rainfall_data = simulate_rainfall_data(sim_days, min_rain, max_rain)

        selected_date = st.sidebar.selectbox("Select Simulated Date", st.session_state.rainfall_data["date"])
        rainfall = st.session_state.rainfall_data[
            st.session_state.rainfall_data["date"] == selected_date
        ]["rainfall_mm"].values[0]

        st.subheader("📈 Simulated Rainfall Trend")
        st.line_chart(st.session_state.rainfall_data.set_index("date"))

        st.markdown(f"**Selected Simulated Date:** `{selected_date.strftime('%Y-%m-%d')}`  |  **Rainfall:** `{rainfall:.2f} mm`")

    else:
        rainfall_df = fetch_current_rainfall_college_station()

        # user select timestamp from real 7-day data
        formatted_times = rainfall_df["datetime"].dt.strftime("%Y-%m-%d %I:%M %p %Z")
        selected_time = st.sidebar.selectbox(
            "Select a date and hour (past 7 days)",
            formatted_times,
            index=len(rainfall_df) - 1
        )

        selected_row = rainfall_df[
            rainfall_df["datetime"].dt.strftime("%Y-%m-%d %I:%M %p %Z") == selected_time
        ].iloc[0]

        timestamp = selected_row["datetime"]
        rainfall = selected_row["precipitation_mm"]

        st.sidebar.markdown(f"🌧️ Real Rainfall at `{timestamp.strftime('%A, %B %d %Y at %I:%M %p %Z')}`")
        st.sidebar.markdown(f"**Rainfall:** `{rainfall:.2f} mm`")

        st.subheader("📈 Past 7 Days Rainfall Trend")
        st.line_chart(rainfall_df.set_index("datetime")["precipitation_mm"])

    # Buttons
    if st.sidebar.button("Run Simulation"):
        st.session_state.run_sim = True

    if st.sidebar.button("Reset"):
        st.session_state.run_sim = False
        st.session_state.rainfall_data = None
        st.rerun()

    # Load and filter infrastructure data
    infra_data = load_infrastructure_data()
    if isinstance(infra_types, list) and len(infra_types) > 0:
        infra_data = infra_data[infra_data['type'].isin(infra_types)]
    infra_data = infra_data.reset_index(drop=True)

    if st.session_state.run_sim:
        if not infra_data.empty:
            rainfall = float(rainfall)
            risk_results = simulate_risk(infra_data, rainfall)

            with st.container():
                st.subheader("🗺️ Risk Map")
                risk_map = create_risk_map(risk_results)
                st_folium(risk_map, width=800, height=500)

                st.subheader("📋 Infrastructure Risk Table")
                st.dataframe(
                    risk_results[['name', 'type', 'age', 'rainfall', 'risk_level', 'recommendation']],
                    use_container_width=True
                )

                csv = risk_results.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Risk Report (CSV)",
                    data=csv,
                    file_name='floodsense_risk_report.csv',
                    mime='text/csv',
                )
        else:
            st.warning("No infrastructure data found for the selected type.")
    else:
        st.info("Adjust inputs and click 'Run Simulation' to begin.")

    with st.expander("🔮 What's Next for FloodSense?"):
        st.markdown("""
        - Live NOAA integration  
        - Floodplain + soil absorption data  
        - Real-time alerts to public officials  
        - Integration with local sensors and weather stations  
        """)

if __name__ == "__main__":
    main()
