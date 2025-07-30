import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import st_folium
import folium
from folium.plugins import HeatMap
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Streamlit setup
st.set_page_config(layout="wide")
st.title("🌍 OTS Ozone Damage Zone Dashboard")
st.markdown("**Real-time mapping, trend analysis, and predictive modeling of global ozone depletion zones**")

# -------------------------------
# 📥 1. Simulate loading ozone data
# -------------------------------
np.random.seed(42)
years = np.random.choice(range(2000, 2025), size=1000)
latitudes = np.random.uniform(-90, 90, 1000)
longitudes = np.random.uniform(-180, 180, 1000)
ozone_values = np.random.normal(loc=300, scale=40, size=1000)

ozone_df = pd.DataFrame({
    'year': years,
    'latitude': latitudes,
    'longitude': longitudes,
    'ozone_du': ozone_values
})
ozone_df['damage_zone'] = ozone_df['ozone_du'] < 220

# -------------------------------
# 🕒 2. Time Filtering
# -------------------------------
selected_year = st.slider("Select Year", int(ozone_df['year'].min()), int(ozone_df['year'].max()), 2010)
filtered_df = ozone_df[ozone_df['year'] == selected_year]

# -------------------------------
# 🗺️ 3. Folium Map with Damage Zones
# -------------------------------
st.subheader("🛰️ Global Ozone Damage Zones")

m = folium.Map(location=[0, 0], zoom_start=2, tiles='cartodb positron')

for _, row in filtered_df.iterrows():
    color = 'red' if row['damage_zone'] else 'blue'
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=4,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        popup=f"Ozone: {row['ozone_du']:.1f} DU (Year: {row['year']})"
    ).add_to(m)

low_ozone_points = filtered_df[filtered_df['damage_zone']][['latitude', 'longitude']].values.tolist()
HeatMap(low_ozone_points, radius=15, blur=10, min_opacity=0.3).add_to(m)

st_data = st_folium(m, width=725)

# -------------------------------
# 📈 4. Trend Analysis Over Time
# -------------------------------
st.subheader("📊 Ozone Trend Over Time")
trend_df = ozone_df.groupby('year')['ozone_du'].mean().reset_index()

fig, ax = plt.subplots()
ax.plot(trend_df['year'], trend_df['ozone_du'], marker='o', linestyle='-', color='purple')
ax.set_xlabel("Year")
ax.set_ylabel("Average Ozone (DU)")
ax.set_title("Global Average Ozone Trend (Simulated)")
st.pyplot(fig)

# -------------------------------
# 🤖 5. Predictive Modeling
# -------------------------------
st.subheader("🤖 Predictive Model: Ozone DU vs Year")
X = ozone_df[['year']]
y = ozone_df['ozone_du']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

mse = mean_squared_error(y_test, predictions)
st.write(f"Model Mean Squared Error: {mse:.2f}")

# Predict for next 5 years
future_years = pd.DataFrame({'year': list(range(2025, 2031))})
future_predictions = model.predict(future_years)

st.write("📅 Predicted Average Ozone DU for Future Years:")
for year, pred in zip(future_years['year'], future_predictions):
    st.write(f"{year}: {pred:.1f} DU")

# ✅ Done
st.success("Dashboard ready for OTS mission control. Monitoring initialized.")
# ---------------------------------------------
# 🛰️ 6. Simulate OTS Swarm Satellite Positions
# ---------------------------------------------

# Simulated swarm satellite data
swarm_data = [
    {"name": "OTS-01", "lat": -75.0, "lon": -120.0, "role": "Neutralizer"},
    {"name": "OTS-02", "lat": -60.0, "lon": 30.0, "role": "Scanner"},
    {"name": "OTS-03", "lat": 20.0, "lon": 60.0, "role": "Analyzer"},
]

st.subheader("🛰️ Active Swarm Units")

for bot in swarm_data:
    folium.Marker(
        location=[bot["lat"], bot["lon"]],
        popup=f"{bot['name']} ({bot['role']})",
        icon=folium.Icon(color="green", icon="cloud")
    ).add_to(m)

# Display swarm data table
st.table(pd.DataFrame(swarm_data))

# Link swarm satellites to nearest ozone hole (if any)
from geopy.distance import geodesic

for bot in swarm_data:
    bot_coord = (bot["lat"], bot["lon"])
    # Find the closest critical damage zone
    critical_zones = filtered_df[filtered_df['ozone_du'] < 220]
    if not critical_zones.empty:
        # Calculate distances to all damage zones
        critical_zones['distance'] = critical_zones.apply(
            lambda row: geodesic(bot_coord, (row['latitude'], row['longitude'])).km,
            axis=1
        )
        closest = critical_zones.sort_values('distance').iloc[0]
        folium.PolyLine(
            locations=[bot_coord, (closest['latitude'], closest['longitude'])],
            color='red',
            weight=2,
            tooltip=f"{bot['name']} → {closest['ozone_du']:.1f} DU zone"
        ).add_to(m)
