import pygame
import random
import math

# Constants
WIDTH, HEIGHT = 800, 600
VEHICLE_COUNT = 5
COMMUNICATION_RANGE = 100  # meters
VEHICLE_SPEED = 2  # Speed of vehicles in pixels per frame

# Initialize PyGame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("V2X Traffic Simulation")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Vehicle class
class Vehicle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(1, VEHICLE_SPEED)  # Random speed
        self.color = BLUE
        self.radius = 20  # Radius for the visual representation
        self.latency = random.uniform(50, 200)  # Latency in milliseconds
        self.reliability = random.uniform(0.5, 1.0)  # Reliability between 0 and 1
        self.network_efficiency = self.calculate_network_efficiency()  # Initial network efficiency

    def calculate_network_efficiency(self):
        # Placeholder for network efficiency calculation
        return self.speed * self.reliability

    def move(self):
        # Move vehicle downwards
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = -self.radius  # Reset to top if out of view

    def draw(self):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)

    def communicate(self, other):
        distance = math.hypot(other.x - self.x, other.y - self.y)
        if distance <= COMMUNICATION_RANGE:
            # Change color to indicate communication
            self.color = GREEN
            other.color = GREEN
            
            # Update latency and network efficiency when communicating
            self.latency = random.uniform(10, 100)  # Simulated lower latency during communication
            self.network_efficiency = self.calculate_network_efficiency()
        else:
            # Reset color if not communicating
            self.color = BLUE
            other.color = BLUE

    def distance_to(self, other):
        """Calculate the distance to another vehicle."""
        return math.hypot(other.x - self.x, other.y - self.y)

# Main function to run the simulation
def main():
    # Create vehicles at random positions
    vehicles = [Vehicle(random.randint(100, WIDTH - 100), random.randint(0, HEIGHT)) for _ in range(VEHICLE_COUNT)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(BLACK)  # Clear the screen

        for i in range(len(vehicles)):
            vehicles[i].move()  # Move each vehicle
            vehicles[i].draw()  # Draw each vehicle
            
            # Check communication with other vehicles
            for j in range(len(vehicles)):
                if i != j:
                    vehicles[i].communicate(vehicles[j])

            # Calculate distance to the next vehicle and print vehicle statistics
            if len(vehicles) > 1:
                # Find the distance to the nearest vehicle
                distances = [vehicles[i].distance_to(vehicles[j]) for j in range(len(vehicles)) if i != j]
                if distances:
                    min_distance = min(distances)
                    print(f"Vehicle {i + 1}: Speed: {vehicles[i].speed:.2f} px/frame, "
                          f"Latency: {vehicles[i].latency:.2f} ms, "
                          f"Reliability: {vehicles[i].reliability:.2f}, "
                          f"Network Efficiency: {vehicles[i].network_efficiency:.2f}, "
                          f"Distance to Next Vehicle: {min_distance:.2f} px")
            else:
                print(f"Vehicle {i + 1}: Speed: {vehicles[i].speed:.2f} px/frame, "
                      f"Latency: {vehicles[i].latency:.2f} ms, "
                      f"Reliability: {vehicles[i].reliability:.2f}, "
                      f"Network Efficiency: {vehicles[i].network_efficiency:.2f}, "
                      f"Distance to Next Vehicle: N/A")

        pygame.display.flip()  # Update the display
        clock.tick(30)  # Frame rate

    pygame.quit()

if __name__ == "__main__":
    main()
