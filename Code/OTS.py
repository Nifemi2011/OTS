from skyfield.api import load
from skyfield.sgp4lib import EarthSatellite
line1 = "1 25544U 98067A   24196.54791667  .00002182  00000-0  44647-4 0  9995"
line2 = "2 25544  51.6445 160.8265 0008387  92.9338  25.4982 15.50629659351385"
ts = load.timescale()
cube_sat = EarthSatellite(line1, line2, "CubeSat", ts)
start = datetime.utcnow()
end = start + timedelta(hours=6)
times = ts.utc(start, end, 60)  # 60 time steps
geo = cube_sat.subpoint(times)
lat = geo.latitude.degrees
lon = geo.longitude.degrees
alt = geo.elevation.km
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(lon, lat, label='CubeSat Path', color='dodgerblue')
plt.title("CubeSat Ground Track")
plt.xlabel("Longitude (°)")
plt.ylabel("Latitude (°)")
plt.legend()
plt.grid(True)
plt.show()
hotspot_detected = True
confidence = 0.92

if hotspot_detected and confidence > 0.85:
    print("🛸 Maneuver triggered: Adjusting orbit parameters...")
    # Optionally adjust your TLE or simulate new trajectory
import json

log = {
    "timestamp": datetime.utcnow().isoformat(),
    "hotspot_triggered": hotspot_detected,
    "confidence": confidence,
    "altitude_km": alt[-1]
}

with open("orbital_maneuver_log.json", "a") as f:
    f.write(json.dumps(log) + "\n")
from datetime import datetime, timedelta
import matplotlib.pyplot as plt 
