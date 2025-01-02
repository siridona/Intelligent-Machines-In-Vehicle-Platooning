import pygame
import time
import random
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 400, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("URLLC Traffic Simulation")

# Colors
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)

# Define vehicle properties
vehicle_width = 50
vehicle_height = 50
vehicle_speed = 2

# Vehicle class to handle movement and communication
class Vehicle:
    def __init__(self, x, y, speed):  # Fixed constructor name
        self.x = x
        self.y = y
        self.speed = speed
        self.latency = random.uniform(5, 20)  # Simulated latency in ms
        self.reliability = random.uniform(0.8, 1.0)  # Reliability between 0.8 and 1.0
        self.network_efficiency = self.calculate_network_efficiency()

    def calculate_network_efficiency(self):
        """Calculate network efficiency based on speed and reliability."""
        return self.speed * self.reliability

    def move(self):
        self.y += self.speed  # Move the vehicle downward
        if self.y > height:
            self.y = -vehicle_height  # Reset vehicle position to top once it moves out of view

    def draw(self):
        pygame.draw.rect(window, blue, (self.x, self.y, vehicle_width, vehicle_height))

    def distance_to(self, other_vehicle):
        """Calculate the distance to another vehicle."""
        return math.sqrt((self.x - other_vehicle.x) ** 2 + (self.y - other_vehicle.y) ** 2)

    def communicate(self, other_vehicle):
        # Calculate and print distance to the next vehicle
        distance_to_next_vehicle = self.distance_to(other_vehicle)
        
        # Simulate data transfer
        print(f"Vehicle at ({self.x},{self.y}) is communicating with vehicle at ({other_vehicle.x},{other_vehicle.y})")
        print(f"  Distance to next vehicle: {distance_to_next_vehicle:.2f} meters")
        print(f"  Speed: {self.speed} units/s")
        print(f"  Latency: {self.latency:.2f} ms")
        print(f"  Reliability: {self.reliability:.2f}")
        print(f"  Network Efficiency: {self.network_efficiency:.2f}")
        
        # Simulate URLLC low-latency and reliable communication
        time.sleep(0.01)  # Minimal delay to simulate real-time transfer

# Define the road and vehicles
def draw_road():
    window.fill(black)
    pygame.draw.rect(window, red, (0, 100, width, 10))  # Red line at top
    pygame.draw.line(window, yellow, (width // 2, 0), (width // 2, height), 5)  # Yellow dashed line

# URLLC Protocol Simulation
def urllc_protocol(vehicles):
    while True:
        # Check for Pygame quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # Update vehicle positions and simulate communication
        draw_road()
        for i in range(len(vehicles)):
            vehicles[i].move()  # Move each vehicle
            vehicles[i].draw()  # Draw each vehicle
            
            # Simulate communication with the next vehicle
            if i < len(vehicles) - 1:
                vehicles[i].communicate(vehicles[i + 1])

        pygame.display.update()
        time.sleep(0.05)  # Frame rate control

if __name__ == "__main__":  # Fixed main guard
    # Initialize vehicles on the road
    vehicles = [
        Vehicle(width // 2 - vehicle_width // 2, 150 + i * 100, vehicle_speed) for i in range(4)
    ]
    
    urllc_protocol(vehicles)
