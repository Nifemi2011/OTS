import random
import time
import csv

class OzoneSwarmUnit:
    def __init__(self, unit_id):
        self.unit_id = unit_id
        self.altitude = random.randint(8000, 15000)
        self.ozone_level = self.sense_ozone()
        self.status = "Idle"
        self.payload_deployed = False
        self.compound_deployed = False
        self.restoration_cycles_remaining = 0

    def sense_ozone(self):
        return round(random.uniform(2.0, 4.0), 2)

    def detect_gases(self):
        gases = {
            "CO₂": round(random.uniform(300, 420), 1),
            "NOx": round(random.uniform(0.01, 0.15), 3)
        }
        return gases

    def update_ozone(self, gases):
        # Calculate depletion factors
        depletion = (gases["CO₂"] - 300) * 0.001 + gases["NOx"] * 2

        # Apply compound protection effect
        if self.compound_deployed and self.restoration_cycles_remaining > 0:
            self.ozone_level += 0.2  # restorative effect
            depletion *= 0.6         # dampen ozone depletion
            self.restoration_cycles_remaining -= 1
        elif self.restoration_cycles_remaining == 0:
            self.compound_deployed = False

        # Apply main payload restoration
        if self.payload_deployed:
            self.ozone_level += 0.3

        # Update final ozone level
        self.ozone_level -= depletion
        self.ozone_level = round(max(0, self.ozone_level), 2)

    def analyze_and_act(self):
        gases = self.detect_gases()
        self.update_ozone(gases)

        if self.ozone_level < 2.5 and not self.payload_deployed:
            self.deploy_payload()
        elif self.ozone_level < 3.0 and not self.compound_deployed:
            self.release_ozone_safe_compound()
        else:
            self.status = "Monitoring"

        return gases

    def deploy_payload(self):
        self.status = "Deploying ozone enhancer"
        self.payload_deployed = True

    def release_ozone_safe_compound(self):
        self.status = "Releasing ozone-safe compound"
        self.compound_deployed = True
        self.restoration_cycles_remaining = 3

    def report(self, cycle, gases):
        return {
            "Cycle": cycle + 1,
            "Unit ID": self.unit_id,
            "Altitude (m)": self.altitude,
            "Ozone Level (ppm)": self.ozone_level,
            "CO₂ (ppm)": gases["CO₂"],
            "NOx (ppm)": gases["NOx"],
            "Status": self.status,
            "Payload Deployed": self.payload_deployed,
            "Compound Deployed": self.compound_deployed
        }

# Simulation Setup
NUM_UNITS = 5
NUM_CYCLES = 5
FILENAME = "ots_swarm_log.csv"
swarm_units = [OzoneSwarmUnit(f"OTS-{i+1:03}") for i in range(NUM_UNITS)]
log_data = []

# Simulation Loop
for cycle in range(NUM_CYCLES):
    print(f"\n🌍 OTS SIMULATION CYCLE {cycle + 1} 🌍\n")
    for unit in swarm_units:
        gases = unit.analyze_and_act()
        report = unit.report(cycle, gases)
        print(f"📡 {report['Unit ID']} @ {report['Altitude (m)']}m | "
              f"O₃: {report['Ozone Level (ppm)']} ppm | "
              f"Status: {report['Status']} | "
              f"Payload: {report['Payload Deployed']} | "
              f"Compound: {report['Compound Deployed']}")
        log_data.append(report)
    time.sleep(1)
with open(FILENAME, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=log_data[0].keys())
    writer.writerows(log_data)

print(f"\n✅ Data saved to {FILENAME}")