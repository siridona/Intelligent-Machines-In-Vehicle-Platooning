import pygame
import time
import random

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

# EAP Class for Authentication
class EAP:
    def __init__(self):
        self.authenticated_vehicles = set()  # Set to track authenticated vehicles

    def authenticate(self, vehicle_id):
        # Simulate EAP authentication (can be replaced with real authentication logic)
        if random.choice([True, False]):
            self.authenticated_vehicles.add(vehicle_id)
            print(f"Vehicle {vehicle_id} authenticated successfully.")
            return True
        else:
            print(f"Vehicle {vehicle_id} failed authentication.")
            return False

# Vehicle class to handle movement and communication
class Vehicle:
    def __init__(self, x, y, speed, vehicle_id):  # Added vehicle_id for authentication
        self.x = x
        self.y = y
        self.speed = speed
        self.id = vehicle_id
        self.authenticated = False  # Track authentication status

    def move(self):
        self.y += self.speed  # Move the vehicle downward
        if self.y > height:
            self.y = -vehicle_height  # Reset vehicle position to top once it moves out of view

    def draw(self):
        pygame.draw.rect(window, blue, (self.x, self.y, vehicle_width, vehicle_height))

    def communicate(self, other_vehicle):
        if self.authenticated and other_vehicle.authenticated:
            # Simulate data transfer
            latency = random.uniform(0.01, 0.1)  # Simulate latency between 10ms and 100ms
            reliability = random.uniform(0, 1)  # Simulate reliability between 0 and 1
            success = reliability >= 0.8  # 80% chance of successful communication based on reliability
            
            # Calculate distance to the next vehicle
            distance_to_next_vehicle = abs(self.y - other_vehicle.y)

            # Print communication attempt details
            if success:
                print(f"Vehicle {self.id} at ({self.x},{self.y}) is communicating with vehicle {other_vehicle.id} at ({other_vehicle.x},{other_vehicle.y})")
                print(f"Distance to Vehicle {other_vehicle.id}: {distance_to_next_vehicle:.2f} meters")
                print(f"Speed of Vehicle {self.id}: {self.speed} units/s, Latency: {latency:.2f} seconds, Reliability: {reliability:.2f}")
                time.sleep(latency)  # Delay to simulate real-time transfer
                return True, reliability  # Communication successful
            else:
                print(f"Vehicle {self.id} failed to communicate with vehicle {other_vehicle.id}. Reliability: {reliability:.2f}")
                return False, reliability  # Communication failed
        else:
            print(f"Vehicle {self.id} cannot communicate with vehicle {other_vehicle.id} (authentication failed)")
            return False, None

# Define the road and vehicles
def draw_road():
    window.fill(black)
    pygame.draw.rect(window, red, (0, 100, width, 10))  # Red line at top
    pygame.draw.line(window, yellow, (width // 2, 0), (width // 2, height), 5)  # Yellow dashed line

# URLLC Protocol Simulation
def urllc_protocol(vehicles, eap):
    total_communications = 0
    successful_communications = 0

    while True:
        # Check for Pygame quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # Update vehicle positions and simulate communication
        draw_road()
        
        # Authenticate vehicles
        for vehicle in vehicles:
            if not vehicle.authenticated:
                vehicle.authenticated = eap.authenticate(vehicle.id)

        for i in range(len(vehicles)):
            vehicles[i].move()  # Move each vehicle
            vehicles[i].draw()  # Draw each vehicle
            
            # Simulate communication with the next vehicle
            if i < len(vehicles) - 1:
                total_communications += 1
                success, reliability = vehicles[i].communicate(vehicles[i + 1])
                if success:
                    successful_communications += 1

        # Calculate and print network efficiency and reliability
        if total_communications > 0:
            efficiency = (successful_communications / total_communications) * 100  # Efficiency in percentage
            print(f"\nNetwork Efficiency: {efficiency:.2f}% (Total Communications: {total_communications}, Successful Communications: {successful_communications})")

        pygame.display.update()
        time.sleep(0.05)  # Frame rate control

if __name__ == "__main__":  # Fixed main guard
    # Initialize EAP
    eap = EAP()
    
    # Initialize vehicles on the road
    vehicles = [
        Vehicle(width // 2 - vehicle_width // 2, 150 + i * 100, vehicle_speed, i) for i in range(4)
    ]
    
    urllc_protocol(vehicles, eap)
