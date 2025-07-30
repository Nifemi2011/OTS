import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import random
from datetime import datetime

# --- MODEL FUNCTION ---
def model_ozone_level(altitude, lat):
    base = 2.0
    ozone_variation = 0.8 * (altitude / 10000) + 0.2 * abs(lat / 90)
    noise = random.uniform(-0.2, 0.2)
    return round(base + ozone_variation + noise, 2)

# --- SWARM DATA ---
def generate_swarm_data():
    units = ["OTS-001", "OTS-002", "OTS-003", "OTS-004", "OTS-005"]
    data = []

    for unit in units:
        altitude = random.randint(8000, 15000)
        lat = random.uniform(-90, 90)
        lon = random.uniform(-180, 180)
        ozone = model_ozone_level(altitude, lat)
        override = "None"
        
        if altitude < 9000:
            override = "Altitude Drop"
        elif ozone > 3.8:
            override = "Ozone Spike"

        data.append({
            "Unit ID": unit,
            "Altitude (m)": altitude,
            "Latitude": lat,
            "Longitude": lon,
            "Ozone Level (ppm)": ozone,
            "Payload Deployed": random.choice([True, False]),
            "Mission Confidence": round(random.uniform(0.6, 1.0), 2),
            "User Override": override,
            "Timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "Safety Alert": (
                "LOW ALTITUDE" if altitude < 9000 else
                "OZONE SPIKE" if ozone > 3.8 else
                "OK"
            )
        })

    return pd.DataFrame(data)

# --- DASH SETUP ---
app = dash.Dash(__name__)
app.title = "OTS Swarm | Space Interface"
server = app.server

# --- LAYOUT ---
app.layout = html.Div([
    html.Div([
        html.H1("🛰️ OTS Swarm Control Dashboard", className="header-title"),
        html.H3("Terraforming Mission Interface", className="header-subtitle")
    ], className="header"),

    html.Div([
        dcc.Graph(id="map-graph", className="big-graph")
    ], className="graph-container"),

    dcc.Interval(id="interval-component", interval=5000, n_intervals=0),

    html.Div([
        html.Div(id="last-update", className="status-box"),
        html.Div(id="feedback-log", className="status-box warning"),
        html.Div(id="emergency-status", className="status-box critical")
    ], className="status-container"),

    html.Footer("🌍 Ozone Terraforming Swarm | Updated: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"), className="footer")
], className="main")

# --- CALLBACK ---
@app.callback(
    Output("map-graph", "figure"),
    Output("last-update", "children"),
    Output("feedback-log", "children"),
    Output("emergency-status", "children"),
    Input("interval-component", "n_intervals")
)
def update_dashboard(n):
    df = generate_swarm_data()

    fig = px.scatter_geo(
        df,
        lat="Latitude",
        lon="Longitude",
        color="User Override",
        size="Ozone Level (ppm)",
        hover_name="Unit ID",
        hover_data={
            "Altitude (m)": True,
            "Ozone Level (ppm)": True,
            "Payload Deployed": True,
            "Mission Confidence": True,
            "User Override": True,
            "Safety Alert": True,
            "Timestamp": True,
            "Latitude": False,
            "Longitude": False
        },
        projection="orthographic"
    )

    fig.update_layout(
        height=650,
        geo=dict(
            landcolor="rgb(30,30,30)",
            showocean=True,
            oceancolor="rgb(10,25,60)",
            lakecolor="rgb(10,25,60)",
            showcountries=True,
            bgcolor="#0b0c10"
        ),
        paper_bgcolor="#0b0c10",
        plot_bgcolor="#0b0c10",
        font=dict(color="white"),
        margin={"r":0, "t":0, "l":0, "b":0},
        dragmode="zoom"
    )

    last_update = f"🕒 Cycle {n} | Units Active: {len(df)} | UTC: {datetime.utcnow().strftime('%H:%M:%S')}"
    feedback_summary = df["User Override"].value_counts().to_dict()
    feedback_text = "🔁 Override Summary: " + ", ".join(f"{k}: {v}" for k, v in feedback_summary.items())

    ozone_spikes = (df["User Override"] == "Ozone Spike").sum()
    avg_conf = df["Mission Confidence"].mean()
    emergency_text = ""
    if ozone_spikes > 2 or avg_conf < 0.7:
        emergency_text = f"🚨 EMERGENCY: "
        if ozone_spikes > 2:
            emergency_text += f"{ozone_spikes} ozone spikes. "
        if avg_conf < 0.7:
            emergency_text += f"Avg Confidence: {avg_conf:.2f}"

    return fig, last_update, feedback_text, emergency_text

# --- RUN ---
if __name__ == "__main__":
    app.run(debug=True)


