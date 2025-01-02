import pygame
import random
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("GPSR Vehicle Routing Visualization")
FONT = pygame.font.SysFont("Arial", 16)

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 200, 200)

class Vehicle:
    def __init__(self, id, position, speed):
        self.id = id
        self.position = position  # (x, y) tuple
        self.speed = speed  # Speed of the vehicle
        self.neighbors = []  # List of neighboring vehicles

    def update_neighbors(self, all_vehicles):
        """Update neighbors based on distance threshold."""
        self.neighbors = [v for v in all_vehicles if v.id != self.id and self.distance(v) < 100]  # Adjusted distance

    def distance(self, other_vehicle):
        """Calculate Euclidean distance to another vehicle."""
        return math.sqrt((self.position[0] - other_vehicle.position[0]) ** 2 + 
                         (self.position[1] - other_vehicle.position[1]) ** 2)

    def send_message(self, destination):
        """Send message to destination vehicle (visualized as an arrow)."""
        distance_to_destination = self.distance(destination)
        pygame.draw.line(screen, CYAN, self.position, destination.position, 2)
        draw_arrow(screen, self.position, destination.position, CYAN)
        pygame.display.flip()
        pygame.time.delay(300)
        print(f"Vehicle {self.id} sending message to Vehicle {destination.id}. Distance: {distance_to_destination:.2f} units")

    def calculate_metrics(self, latency_factor=1.0):
        """Calculate network metrics for the vehicle."""
        # Simple calculation based on speed, a random factor for latency and reliability
        latency = random.uniform(0.1, 0.5) * latency_factor  # Random latency between 0.1 to 0.5 seconds
        reliability = 1 - (1 / self.speed) if self.speed > 0 else 0  # Basic reliability based on speed (simplified)
        network_efficiency = self.speed / (latency + 0.1)  # Simplified efficiency calculation
        return latency, reliability, network_efficiency

class GreedyPerimeterStatelessRouting:
    def route(self, sender, destination, visited=None):
        """Route message using GPSR."""
        if visited is None:
            visited = set()

        print(f"\nRouting from Vehicle {sender.id} to Vehicle {destination.id}.")

        if sender.id in visited:
            print(f"Vehicle {sender.id} has already been visited. Ending route to prevent loops.")
            return

        visited.add(sender.id)  # Mark the sender as visited

        if not sender.neighbors:
            print(f"Vehicle {sender.id} has no neighbors to route to.")
            return

        # Greedy forwarding to the neighbor closest to the destination
        closest_neighbor = min(sender.neighbors, key=lambda v: v.distance(destination))
        sender.send_message(closest_neighbor)

        # Print metrics for the sender vehicle
        latency, reliability, efficiency = sender.calculate_metrics()
        print(f"Metrics for Vehicle {sender.id}: Speed={sender.speed:.2f} units/s, "
              f"Latency={latency:.2f}s, Reliability={reliability:.2f}, Network Efficiency={efficiency:.2f}")

        # If the closest neighbor is the destination
        if closest_neighbor.id == destination.id:
            print(f"Vehicle {destination.id} received message successfully.")
            latency, reliability, efficiency = closest_neighbor.calculate_metrics()
            print(f"Metrics for Vehicle {closest_neighbor.id}: Speed={closest_neighbor.speed:.2f} units/s, "
                  f"Latency={latency:.2f}s, Reliability={reliability:.2f}, Network Efficiency={efficiency:.2f}")
            return

        # Continue routing from the closest neighbor
        self.route(closest_neighbor, destination, visited)

def draw_arrow(screen, start_pos, end_pos, color, arrow_size=10):
    """Draw an arrow from start_pos to end_pos."""
    pygame.draw.line(screen, color, start_pos, end_pos, 2)
    angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
    arrow_end1 = (end_pos[0] - arrow_size * math.cos(angle - math.pi / 6),
                  end_pos[1] - arrow_size * math.sin(angle - math.pi / 6))
    arrow_end2 = (end_pos[0] - arrow_size * math.cos(angle + math.pi / 6),
                  end_pos[1] - arrow_size * math.sin(angle + math.pi / 6))
    pygame.draw.polygon(screen, color, [end_pos, arrow_end1, arrow_end2])

def find_farthest_vehicles(vehicles):
    """Find the two vehicles that are farthest apart."""
    max_distance = 0
    farthest_pair = (vehicles[0], vehicles[0])  # Initialize with the first vehicle

    for i in range(len(vehicles)):
        for j in range(i + 1, len(vehicles)):
            dist = vehicles[i].distance(vehicles[j])
            if dist > max_distance:
                max_distance = dist
                farthest_pair = (vehicles[i], vehicles[j])

    return farthest_pair

def create_vehicle_cluster(num_clusters, vehicles_per_cluster):
    """Create a cluster of vehicles in a grid-like arrangement.""" 
    vehicles = []
    cluster_distance = 150  # Distance between clusters

    for cluster in range(num_clusters):
        # Base position for the cluster
        base_x = 100 + cluster * cluster_distance
        base_y = random.randint(100, 500)

        for i in range(vehicles_per_cluster):
            # Position vehicles in a row within each cluster
            x = base_x + (i * 40)  # Adjust spacing for vehicles in the cluster
            y = base_y
            speed = random.uniform(10, 20)  # Random speed for each vehicle
            vehicles.append(Vehicle(len(vehicles), (x, y), speed))

    # Add intermediate vehicles between clusters
    for i in range(num_clusters - 1):
        mid_x = (100 + (i + 1) * cluster_distance + 100 + i * cluster_distance) // 2
        mid_y = random.randint(100, 500)  # Random y position for the middle vehicle
        speed = random.uniform(10, 20)
        vehicles.append(Vehicle(len(vehicles), (mid_x, mid_y), speed))

    return vehicles

def simulate_gpsr(num_clusters, vehicles_per_cluster):
    # Create clustered vehicles
    vehicles = create_vehicle_cluster(num_clusters, vehicles_per_cluster)

    # Update neighbors for each vehicle based on proximity
    for vehicle in vehicles:
        vehicle.update_neighbors(vehicles)

    # Find the farthest vehicles for routing
    sender, destination = find_farthest_vehicles(vehicles)
    print(f"Starting routing from Vehicle {sender.id} to Vehicle {destination.id}.\n")
    
    # Use Greedy Perimeter Stateless Routing
    gpsr = GreedyPerimeterStatelessRouting()

    running = True
    while running:
        screen.fill(WHITE)

        # Draw vehicles
        for vehicle in vehicles:
            color = BLUE
            if vehicle == sender:
                color = GREEN  # Starting vehicle in green
            elif vehicle == destination:
                color = RED    # Destination vehicle in red
            pygame.draw.circle(screen, color, vehicle.position, 10)
            label = FONT.render(str(vehicle.id), True, WHITE)
            screen.blit(label, (vehicle.position[0] - 5, vehicle.position[1] - 5))

            # Draw neighbor connections
            for neighbor in vehicle.neighbors:
                pygame.draw.line(screen, BLUE, vehicle.position, neighbor.position, 1)

        pygame.display.flip()

        # Start routing visualization
        gpsr.route(sender, destination)

        # Main loop to keep the window open
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()

# Run the simulation with a clustered arrangement of vehicles
simulate_gpsr(num_clusters=3, vehicles_per_cluster=5)
