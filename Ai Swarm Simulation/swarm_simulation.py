import random

class SwarmUnit:
    def __init__(self, unit_id):
        self.unit_id = unit_id
        self.payload_deployed = False
        self.ozone_level = 3.0
        self.co2_level = 350
        self.nox_level = 0.05
        self.predicted_drop = 0.0

    def sense_environment(self):
        # Simulate sensing local ozone and gases with some variation
        self.ozone_level = round(random.uniform(1.5, 4.0), 2)
        self.co2_level = round(random.uniform(300, 420), 1)
        self.nox_level = round(random.uniform(0.01, 0.15), 3)

    def predict_ozone_drop(self):
        # Simple AI prediction: ozone drop linked to CO2 and NOx
        self.predicted_drop = 0.01 * (self.co2_level - 300) + 0.1 * self.nox_level

    def decide_deployment(self):
        threshold = 2.5
        predicted_threshold = 0.2
        if self.ozone_level < threshold or self.predicted_drop > predicted_threshold:
            self.deploy_sprayer()
        else:
            self.payload_deployed = False
            print(f"{self.unit_id}: No deployment — ozone {self.ozone_level} ppm, predicted drop {self.predicted_drop:.3f}")

    def deploy_sprayer(self):
        self.payload_deployed = True
        print(f"{self.unit_id}: Deploying sprayer at ozone {self.ozone_level} ppm with predicted drop {self.predicted_drop:.3f}")

    def cycle(self):
        self.sense_environment()
        self.predict_ozone_drop()
        self.decide_deployment()

class SwarmSimulation:
    def __init__(self, num_units=5):
        self.units = [SwarmUnit(f"OTS-{i+1:03d}") for i in range(num_units)]

    def run_cycles(self, num_cycles=10):
        for cycle_num in range(1, num_cycles + 1):
            print(f"\n=== Simulation Cycle {cycle_num} ===")
            for unit in self.units:
                unit.cycle()

if __name__ == "__main__":
    sim = SwarmSimulation(num_units=5)
    sim.run_cycles(num_cycles=10)
