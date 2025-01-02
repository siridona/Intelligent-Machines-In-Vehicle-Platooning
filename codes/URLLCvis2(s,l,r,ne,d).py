import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Function to calculate a point on a Bezier curve
def bezier_point(t, p0, p1, p2, p3):
    return (
        (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0],
        (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
    )

# Define multiple control points for a winding road with more curves
control_points_set = [
    [(100, 500), (250, 400), (400, 450), (550, 300)],  # First curve (start from left)
    [(550, 300), (700, 200), (600, 150), (450, 100)],  # Second curve (moving back)
    [(450, 100), (300, 50), (200, 100), (100, 200)],   # Third curve (turn back left)
]

# Generate road path points using multiple Bezier curves
path_points = []
for control_points in control_points_set:
    for i in range(101):  # Generate 101 points along each curve
        t = i / 100
        path_points.append(bezier_point(t, control_points[0], control_points[1], control_points[2], control_points[3]))

# Vehicle class to follow the path
class Vehicle:
    def __init__(self, index):
        self.index = index  # Index of the vehicle in the platoon
        self.x, self.y = path_points[0]  # Initial position
        self.speed = 2
        self.path_index = 0
        self.angle = 0
        self.width = 30
        self.height = 60
        
        # Randomly generate additional attributes
        self.latency = random.uniform(50, 200)  # Latency in milliseconds
        self.reliability = random.uniform(0.5, 1.0)  # Reliability between 0 and 1
        self.network_efficiency = self.calculate_network_efficiency()

    def calculate_network_efficiency(self):
        """Calculate network efficiency based on speed and reliability."""
        return self.speed * self.reliability

    def follow_path(self):
        if self.path_index < len(path_points) - 1:
            # Get current and next point on the path
            current_point = path_points[self.path_index]
            next_point = path_points[self.path_index + 1]
            
            # Calculate the angle towards the next point
            self.angle = math.degrees(math.atan2(next_point[1] - current_point[1], next_point[0] - current_point[0]))
            
            # Move vehicle towards next point
            self.x += self.speed * math.cos(math.radians(self.angle))
            self.y += self.speed * math.sin(math.radians(self.angle))
            
            # Check if the vehicle has reached the next point
            distance_to_next = math.hypot(next_point[0] - self.x, next_point[1] - self.y)
            if distance_to_next < 10:
                self.path_index += 1  # Move to next point on the path

    def maintain_distance(self, vehicles):
        if self.index > 0:
            # Get the vehicle in front
            vehicle_ahead = vehicles[self.index - 1]
            distance = math.hypot(self.x - vehicle_ahead.x, self.y - vehicle_ahead.y)
            if distance < 80:  # Maintain a distance of 80 pixels
                self.speed = 0  # Stop if too close
            else:
                self.speed = 2  # Normal speed

    def print_info(self, vehicles):  # Corrected method
        if self.index > 0:
            vehicle_ahead = vehicles[self.index - 1]
            distance = math.hypot(self.x - vehicle_ahead.x, self.y - vehicle_ahead.y)
            print(f"Vehicle {self.index}: Position ({self.x:.2f}, {self.y:.2f}), Speed: {self.speed}, "
                  f"Distance to next: {distance:.2f}, Latency: {self.latency:.2f} ms, "
                  f"Reliability: {self.reliability:.2f}, Network Efficiency: {self.network_efficiency:.2f}.")
        else:
            print(f"Vehicle {self.index}: Position ({self.x:.2f}, {self.y:.2f}), Speed: {self.speed}, "
                  f"Latency: {self.latency:.2f} ms, Reliability: {self.reliability:.2f}, "
                  f"Network Efficiency: {self.network_efficiency:.2f}.")

    def draw(self, screen):
        rotated_vehicle = pygame.transform.rotate(pygame.Surface((self.width, self.height)), -self.angle)
        rotated_vehicle.fill(BLUE)
        # Adjust the position to center the vehicle after rotation
        rect = rotated_vehicle.get_rect(center=(self.x, self.y))
        screen.blit(rotated_vehicle, rect.topleft)

# Function to draw the road based on path points
def draw_road():
    pygame.draw.lines(screen, BLACK, False, path_points, 60)  # Road width
    pygame.draw.lines(screen, YELLOW, False, path_points, 5)  # Yellow centerline

# Main function to run the simulation
def main():
    clock = pygame.time.Clock()
    vehicles = [Vehicle(i) for i in range(4)]  # Create 4 vehicles
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(GRAY)
        draw_road()

        # Update and draw each vehicle
        for vehicle in vehicles:
            vehicle.maintain_distance(vehicles)
            vehicle.follow_path()
            vehicle.draw(screen)
            vehicle.print_info(vehicles)  # Print vehicle info to the console

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":  # Corrected main check
    main()