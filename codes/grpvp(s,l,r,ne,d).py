import random
import math

class Vehicle:
    def __init__(self, id, position):
        self.id = id
        self.position = position  # (x, y) tuple
        self.neighbors = []  # List of neighboring vehicles
        self.speed = random.uniform(5, 15)  # Random speed for the vehicle
        self.latency = random.uniform(0.1, 0.5)  # Random latency in seconds
        self.reliability = random.uniform(0.7, 1.0)  # Random reliability factor
        self.network_efficiency = self.calculate_network_efficiency()

    def update_neighbors(self, all_vehicles):
        """Update neighbors based on distance."""
        self.neighbors = [v for v in all_vehicles if v.id != self.id and self.distance(v) < 10]  # Example distance threshold
        print(f"Vehicle {self.id} neighbors: {[v.id for v in self.neighbors]}")  # Debug print

    def distance(self, other_vehicle):
        """Calculate Euclidean distance to another vehicle."""
        return math.sqrt((self.position[0] - other_vehicle.position[0]) ** 2 + 
                         (self.position[1] - other_vehicle.position[1]) ** 2)

    def send_message(self, destination):
        """Send message to destination vehicle."""
        print(f"Vehicle {self.id} sending message to Vehicle {destination.id}.")
        # Print metrics for the vehicle sending the message
        self.print_metrics()

    def print_metrics(self):
        """Print the vehicle's metrics and distances to neighbors."""
        print(f"Vehicle {self.id} metrics: Speed={self.speed:.2f} units/s, "
              f"Latency={self.latency:.2f}s, Reliability={self.reliability:.2f}, "
              f"Network Efficiency={self.network_efficiency:.2f}")
        
        # Print distances to neighboring vehicles
        for neighbor in self.neighbors:
            distance = self.distance(neighbor)
            print(f"Distance to Vehicle {neighbor.id}: {distance:.2f} units")

    def calculate_network_efficiency(self):
        """Calculate network efficiency based on speed and latency."""
        return self.speed / (self.latency + 0.1)  # Adding a small value to avoid division by zero

class GeographicRoutingProtocol:
    def route(self, sender, destination, visited=None):
        """Route message using Geographic Routing Protocol."""
        if visited is None:
            visited = set()
        
        print(f"Routing using GRP from Vehicle {sender.id} to Vehicle {destination.id}.")
        
        if sender.id in visited:
            print(f"Vehicle {sender.id} already visited; stopping recursion.")
            return
        
        visited.add(sender.id)

        if not sender.neighbors:
            print(f"Vehicle {sender.id} has no neighbors to route to.")
            return
        
        # Greedily forward to the neighbor closest to the destination
        closest_neighbor = min(sender.neighbors, key=lambda v: sender.distance(v))
        sender.send_message(closest_neighbor)
        
        # Check if the closest neighbor is the destination
        if closest_neighbor.id == destination.id:
            print(f"Vehicle {closest_neighbor.id} received message from Vehicle {sender.id}.")
            closest_neighbor.print_metrics()  # Print metrics for the destination
            return
        
        # Continue routing from the closest neighbor
        self.route(closest_neighbor, destination, visited)

# Simulate a platoon of vehicles for GRP
def simulate_grp(num_vehicles):
    vehicles = [Vehicle(i, (random.uniform(0, 20), random.uniform(0, 20))) for i in range(num_vehicles)]  # Smaller area for positions
    
    # Update neighbors for each vehicle
    for vehicle in vehicles:
        vehicle.update_neighbors(vehicles)

    # Example routing from Vehicle 0 to Vehicle 5
    sender = vehicles[0]
    destination = vehicles[5]
    print(f"Starting routing from Vehicle {sender.id} to Vehicle {destination.id}.\n")
    
    # Create instance of Geographic Routing Protocol
    grp = GeographicRoutingProtocol()
    grp.route(sender, destination)

# Run the simulation for GRP with a defined number of vehicles
simulate_grp(10)
