import queue
import threading
import time
import random

class CommunicationNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.inbox = queue.Queue()
        self.neighbors = []
        self.running = True

    def add_neighbor(self, neighbor_node):
        self.neighbors.append(neighbor_node)

    def send_message(self, message, target):
        # Simulate latency and possible packet loss
        latency = random.uniform(0.05, 0.2)  # seconds
        loss_chance = 0.05  # 5% chance to lose message

        def delayed_send():
            time.sleep(latency)
            if random.random() > loss_chance:
                target.inbox.put((self.node_id, message))
                print(f"{self.node_id} → {target.node_id}: {message}")
            else:
                print(f"{self.node_id} → {target.node_id}: Message lost")

        threading.Thread(target=delayed_send).start()

    def broadcast_message(self, message):
        for neighbor in self.neighbors:
            self.send_message(message, neighbor)

    def listen(self):
        while self.running:
            try:
                sender, message = self.inbox.get(timeout=0.5)
                print(f"{self.node_id} received from {sender}: {message}")
                # Forward important messages to neighbors except sender
                if "ALERT" in message:
                    for neighbor in self.neighbors:
                        if neighbor.node_id != sender:
                            self.send_message(message, neighbor)
            except queue.Empty:
                continue

    def stop(self):
        self.running = False

# Create nodes representing drones and satellites
drone1 = CommunicationNode("Drone-1")
drone2 = CommunicationNode("Drone-2")
satellite = CommunicationNode("Satellite-1")

# Define communication neighbors (bi-directional)
drone1.add_neighbor(drone2)
drone1.add_neighbor(satellite)

drone2.add_neighbor(drone1)
drone2.add_neighbor(satellite)

satellite.add_neighbor(drone1)
satellite.add_neighbor(drone2)

# Start listening threads
threads = []
for node in [drone1, drone2, satellite]:
    t = threading.Thread(target=node.listen)
    t.start()
    threads.append(t)

# Simulate sending messages
drone1.send_message("Ozone level normal", drone2)
drone2.send_message("Ozone level low - ALERT", satellite)
satellite.broadcast_message("ALERT: Coordinated sprayer deployment needed")

# Let the simulation run briefly
time.sleep(3)

# Stop all nodes
for node in [drone1, drone2, satellite]:
    node.stop()

# Wait for threads to finish
for t in threads:
    t.join()
# End of communication simulation
