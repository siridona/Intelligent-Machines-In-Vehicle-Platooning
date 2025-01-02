import simpy
import random

# Constants
VEHICLE_COUNT = 5
PEDESTRIAN_COUNT = 3
COMMUNICATION_RANGE = 100  # meters
SECURITY_KEY = "secure_key"  # Dummy security key for demonstration
PEDESTRIAN_ALERT_RANGE = 50  # meters

# Simulated network parameters
LATENCY_MEAN = 0.1  # mean latency in seconds
LATENCY_STDDEV = 0.02  # standard deviation of latency
RELIABILITY_THRESHOLD = 0.9  # 90% reliability for communication
NETWORK_EFFICIENCY_BASE = 0.8  # Base efficiency of communication

class Vehicle:
    def __init__(self, env, name, position):
        self.env = env
        self.name = name
        self.position = position
        self.speed = random.randint(20, 60)  # Random speed in km/h
        self.status = "active"
        self.communication_range = COMMUNICATION_RANGE
        self.env.process(self.run())

    def run(self):
        while True:
            # Simulate vehicle movement
            self.position += self.speed / 3.6  # Convert speed to m/s
            print(f"{self.name} moving to {self.position:.2f} meters at {self.env.now:.2f} seconds.")
            yield self.env.timeout(1)  # Update every second
            
            # Communicate with nearby vehicles and infrastructure
            self.communicate()

    def communicate(self):
        # Direct Vehicle-to-Vehicle (V2V) Communication
        print(f"{self.name} checking for nearby vehicles at {self.env.now:.2f} seconds.")
        for vehicle in vehicles:
            if vehicle != self and abs(vehicle.position - self.position) <= self.communication_range:
                self.v2v_communication(vehicle)

        # Vehicle-to-Infrastructure (V2I) Communication
        self.v2i_communication()

        # Alert nearby pedestrians
        self.alert_pedestrians()

    def v2v_communication(self, other_vehicle):
        latency = random.gauss(LATENCY_MEAN, LATENCY_STDDEV)
        reliability = random.random()  # Simulate reliability as a random float between 0 and 1
        distance_to_other_vehicle = abs(other_vehicle.position - self.position)

        if reliability >= RELIABILITY_THRESHOLD:
            print(f"{self.name} communicates with {other_vehicle.name} at {self.env.now:.2f} seconds with latency {latency:.2f} seconds.")
            data = {
                "speed": self.speed,
                "position": self.position,
                "status": self.status,
                "security_key": SECURITY_KEY,
                "latency": latency,
                "network_efficiency": NETWORK_EFFICIENCY_BASE + (reliability * 0.2),  # Adjust efficiency based on reliability
                "distance_to_next_vehicle": distance_to_other_vehicle
            }
            print(f"Data exchanged: {data}")
            print(f"Distance to {other_vehicle.name}: {distance_to_other_vehicle:.2f} meters")
        else:
            print(f"{self.name} failed to communicate with {other_vehicle.name} due to low reliability at {self.env.now:.2f} seconds.")

    def v2i_communication(self):
        latency = random.gauss(LATENCY_MEAN, LATENCY_STDDEV)
        print(f"{self.name} communicating with infrastructure at {self.env.now:.2f} seconds with latency {latency:.2f} seconds.")
        data = {
            "speed": self.speed,
            "position": self.position,
            "status": self.status,
            "security_key": SECURITY_KEY,
            "latency": latency,
            "network_efficiency": NETWORK_EFFICIENCY_BASE + (random.random() * 0.2)  # Random efficiency for demo
        }
        print(f"Data exchanged with infrastructure: {data}")

    def alert_pedestrians(self):
        for pedestrian in pedestrians:
            if abs(pedestrian.position - self.position) <= PEDESTRIAN_ALERT_RANGE:
                pedestrian.receive_alert(self)

class Pedestrian:
    def __init__(self, env, name, position):
        self.env = env
        self.name = name
        self.position = position
        self.env.process(self.walk())

    def walk(self):
        while True:
            # Simulate pedestrian movement
            self.position += random.choice([-1, 1])  # Move left or right randomly
            print(f"{self.name} walking to {self.position:.2f} meters at {self.env.now:.2f} seconds.")
            yield self.env.timeout(1)  # Update every second

    def receive_alert(self, vehicle):
        # Alert message indicating the vehicle is approaching
        distance = abs(vehicle.position - self.position)
        if vehicle.position > self.position:
            print(f"Alert: {self.name}, {vehicle.name} is approaching from behind at {distance:.2f} meters!")
        else:
            print(f"Alert: {self.name}, {vehicle.name} is approaching from ahead at {distance:.2f} meters!")

        # Notify about all approaching vehicles
        for v in vehicles:
            if v != vehicle and abs(v.position - self.position) <= PEDESTRIAN_ALERT_RANGE:
                alert_distance = abs(v.position - self.position)
                if v.position > self.position:
                    print(f"Also Alert: {self.name}, {v.name} is approaching from behind at {alert_distance:.2f} meters!")
                else:
                    print(f"Also Alert: {self.name}, {v.name} is approaching from ahead at {alert_distance:.2f} meters!")

# Initialize Simulation Environment
env = simpy.Environment()
vehicles = [Vehicle(env, f"Vehicle-{i}", position=random.randint(0, 200)) for i in range(VEHICLE_COUNT)]
pedestrians = [Pedestrian(env, f"Pedestrian-{i}", position=random.randint(0, 200)) for i in range(PEDESTRIAN_COUNT)]

# Run Simulation
env.run(until=20)  # Simulate for 20 seconds
