import simpy
import random
import pygame
import sys

# Constants
VEHICLE_COUNT = 5
PEDESTRIAN_COUNT = 3
COMMUNICATION_RANGE = 100  # meters
SECURITY_KEY = "secure_key"  # Dummy security key for demonstration
PEDESTRIAN_ALERT_RANGE = 50  # meters
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SCALE = 3  # Scale for visualization

class Vehicle:
    def __init__(self, env, name, position):
        self.env = env
        self.name = name
        self.position = position
        self.speed = random.randint(20, 60)  # Random speed in km/h
        self.latency = random.uniform(50, 200)  # Latency in milliseconds
        self.reliability = random.uniform(0.5, 1.0)  # Reliability between 0 and 1
        self.network_efficiency = self.calculate_network_efficiency()
        self.status = "active"
        self.communication_range = COMMUNICATION_RANGE
        self.env.process(self.run())

    def calculate_network_efficiency(self):
        # Simple efficiency based on speed and reliability
        return self.speed * self.reliability

    def run(self):
        while True:
            # Simulate vehicle movement
            self.position += self.speed / 3.6  # Convert speed to m/s
            print(f"{self.name} moving to {self.position:.2f} meters at {self.env.now:.2f} seconds. "
                  f"Speed: {self.speed} km/h, Latency: {self.latency:.2f} ms, "
                  f"Reliability: {self.reliability:.2f}, Network Efficiency: {self.network_efficiency:.2f}")

            # Print distance to the next vehicle
            self.print_distance_to_next_vehicle()

            yield self.env.timeout(1)  # Update every second
            
            # Communicate with nearby vehicles and infrastructure
            self.communicate()

    def print_distance_to_next_vehicle(self):
        """Print the distance to the nearest vehicle."""
        distances = []
        for vehicle in vehicles:
            if vehicle.name != self.name:  # Exclude self
                distance = abs(self.position - vehicle.position)
                distances.append(distance)

        if distances:
            min_distance = min(distances)
            print(f"{self.name} distance to next vehicle: {min_distance:.2f} meters.")

    def communicate(self):
        # Simplified for visualization
        print(f"{self.name} checking for nearby vehicles at {self.env.now:.2f} seconds.")

class Pedestrian:
    def __init__(self, env, name, position):
        self.env = env
        self.name = name
        self.position = position
        self.env.process(self.walk())

    def walk(self):
        while True:
            # Simulate pedestrian movement
            move_direction = random.choice([-1, 1])  # Move left or right randomly
            self.position += move_direction  # Change position
            print(f"{self.name} walking to {self.position:.2f} meters at {self.env.now:.2f} seconds.")
            yield self.env.timeout(1)  # Update every second

# Initialize Simulation Environment
env = simpy.Environment()
vehicles = [Vehicle(env, f"Vehicle-{i}", position=random.randint(0, 200)) for i in range(VEHICLE_COUNT)]
pedestrians = [Pedestrian(env, f"Pedestrian-{i}", position=random.randint(0, 200)) for i in range(PEDESTRIAN_COUNT)]

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Vehicle and Pedestrian Simulation")
clock = pygame.time.Clock()
running = True

# Run Simulation with Visualization
def run_simulation_with_visualization(until):
    for _ in range(until):
        env.step()  # Step the simulation
        screen.fill((255, 255, 255))  # Clear screen

        # Draw vehicles
        for vehicle in vehicles:
            x = vehicle.position * SCALE  # Scale position for display
            pygame.draw.rect(screen, (0, 0, 255), (x, WINDOW_HEIGHT // 2, 40, 20))  # Draw vehicle

        # Draw pedestrians
        for pedestrian in pedestrians:
            x = pedestrian.position * SCALE  # Scale position for display
            pygame.draw.circle(screen, (255, 0, 0), (x, WINDOW_HEIGHT // 2 + 40), 10)  # Draw pedestrian

        pygame.display.flip()  # Update the display
        clock.tick(1)  # 1 frame per second

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    run_simulation_with_visualization(20)  # Simulate for 20 seconds

pygame.quit()
sys.exit()
