import random
import time
import pandas as pd
import matplotlib.pyplot as plt

class OzoneSwarmUnit:
    def __init__(self, unit_id):
        self.unit_id = unit_id
        self.altitude = random.randint(8000, 15000)  # in meters
        self.ozone_level = self.sense_ozone()
        self.status = "Idle"
        self.payload_deployed = False

    def sense_ozone(self):
        return round(random.uniform(2.0, 4.0), 2)

    def detect_gases(self):
        gases = {
            "O₃": self.ozone_level,
            "CO₂": round(random.uniform(300, 420), 1),
            "NOx": round(random.uniform(0.01, 0.15), 3)
        }
        return gases

    def analyze_and_act(self):
        self.ozone_level = self.sense_ozone()
        gases = self.detect_gases()

        if self.ozone_level < 2.5 and not self.payload_deployed:
            self.deploy_payload()
        else:
            self.status = "Monitoring"

        return gases

    def deploy_payload(self):
        self.status = "Deploying ozone enhancer"
        self.payload_deployed = True

    def report(self):
        return {
            "Unit ID": self.unit_id,
            "Altitude (m)": self.altitude,
            "Ozone Level (ppm)": self.ozone_level,
            "Status": self.status,
            "Payload Deployed": self.payload_deployed
        }

NUM_UNITS = 5
swarm_units = [OzoneSwarmUnit(f"OTS-{i+1:03}") for i in range(NUM_UNITS)]

for cycle in range(3):
    print(f"\n🌍 OTS SIMULATION CYCLE {cycle + 1} 🌍\n")
    for unit in swarm_units:
        gases = unit.analyze_and_act()
        report = unit.report()
        print(f"📡 {report['Unit ID']} @ {report['Altitude (m)']}m | "
              f"O₃: {report['Ozone Level (ppm)']} ppm | "
              f"Status: {report['Status']} | Payload: {report['Payload Deployed']}")
    time.sleep(1)
    print("\nGases Detected:")
    for unit in swarm_units:
        print(f"{unit.unit_id}: {unit.detect_gases()}")
    time.sleep(2)
    print("End of Cycle\n")
    plt.show()
    time.sleep(1)
    plt.clf()
    plt.title("Ozone Levels Over Time")
    plt.xlabel("Year")
    plt.ylabel("Average Ozone (DU)")
    