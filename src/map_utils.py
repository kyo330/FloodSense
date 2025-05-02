import folium

def risk_color(risk_level):
    return {
        "Low": "green",
        "Moderate": "orange",
        "High": "red"
    }.get(risk_level, "blue")

def create_risk_map(risk_df):
    if risk_df.empty:
        return folium.Map(location=[30.62798, -96.33441], zoom_start=10)

    m = folium.Map(
        location=[risk_df['latitude'].mean(), risk_df['longitude'].mean()],
        zoom_start=11
    )

    for _, row in risk_df.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"{row['name']} - Risk: {row['risk_level']}",
            icon=folium.Icon(color=risk_color(row["risk_level"]))
        ).add_to(m)

    return m
