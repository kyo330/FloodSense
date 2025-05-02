import streamlit as st
from streamlit_folium import st_folium
import folium

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

    # Home button
    if st.button("🏠 Go to Home"):
        st.session_state.run_sim = False
        st.session_state.simulate_mode = False
        st.session_state.rainfall_data = None  # Clear rainfall data
        st.rerun()

    # Session state init
    if "run_sim" not in st.session_state:
        st.session_state.run_sim = False
    if "simulate_mode" not in st.session_state:
        st.session_state.simulate_mode = False
    if "rainfall_data" not in st.session_state:
        st.session_state.rainfall_data = None

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
        # Only regenerate data if it's not already in session state
        if st.session_state.rainfall_data is None:
            min_rain = st.sidebar.slider("Min Rainfall (mm)", 0, 100, 10)
            max_rain = st.sidebar.slider("Max Rainfall (mm)", min_rain, 200, 60)
            sim_days = st.sidebar.slider("Days to Simulate", 1, 14, 7)

            # Generate simulated data and store it in session state
            st.session_state.rainfall_data = simulate_rainfall_data(sim_days, min_rain, max_rain)
        
        # Allow the user to select a date from the generated simulated data
        selected_date = st.sidebar.selectbox("Select Simulated Date", st.session_state.rainfall_data["date"])
        rainfall = st.session_state.rainfall_data[st.session_state.rainfall_data["date"] == selected_date]["rainfall_mm"].values[0]
        
        st.subheader("📈 Simulated Rainfall Trend")
        st.line_chart(st.session_state.rainfall_data.set_index("date"))
    else:
        # Fetch real-time rainfall data
        timestamp, rainfall = fetch_current_rainfall_college_station()
        st.sidebar.write(f"🌧️ Real-time Rainfall at {timestamp}: **{rainfall} mm**")

    # Simulation & Reset Buttons
    if st.sidebar.button("Run Simulation"):
        st.session_state.run_sim = True

    if st.sidebar.button("Reset"):
        st.session_state.run_sim = False
        st.session_state.rainfall_data = None  # Clear rainfall data
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

            # Risk Map
            st.subheader("Risk Map 🗺️")
            risk_map = create_risk_map(risk_results)
            st_folium(risk_map, width=800, height=500)

            # Risk Table below the map
            st.subheader("📋 Infrastructure Risk Table")
            st.dataframe(
                risk_results[['name', 'type', 'age', 'rainfall', 'risk_level', 'recommendation']],
                use_container_width=True
            )

            # Download Risk Report
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
