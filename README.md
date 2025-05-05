# FloodSense: Real-Time Flood Risk Estimator

FloodSense is a real-time flood risk estimation tool designed for critical water infrastructure. It simulates flood risks based on rainfall data, infrastructure properties, and predefined risk models. The tool helps in visualizing and evaluating flood vulnerability to support preventive planning and emergency response.

## 🌐 Live App

- **Access the app:** [FloodSense Web App](https://floodsense-cstx.streamlit.app)
- **Read the report:** [FloodSense Report (DOC)](https://docs.google.com/document/d/1ajH1DKk8LyBFUrP-oaSDsM-emb375H_ddkPelXNTOIM/edit?usp=sharing)


## Features

- Real-time or simulated rainfall input
- Interactive map of infrastructure and associated flood risk
- Table view with downloadable risk report
- Adjustable parameters for rainfall simulation
- Focused on College Station, TX (location input not currently dynamic)

## Technologies Used

- Python
- Streamlit
- Pandas, NumPy
- Folium (for geospatial mapping)
- Open-Meteo API (for real-time rainfall data)

## Getting Started

Clone the repository and install dependencies to run locally:

```bash
git clone https://github.com/your-username/floodsense.git
cd floodsense
pip install -r requirements.txt
streamlit run app.py
