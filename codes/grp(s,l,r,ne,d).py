import random
import math

class Vehicle:
    def __init__(self, id, position):
        self.id = id
        self.position = position  # Position along the straight road (x-coordinate)
        self.speed = random.randint(20, 60)  # Random speed in km/h
        self.latency = random.uniform(50, 200)  # Latency in milliseconds
        self.reliability = random.uniform(0.5, 1.0)  # Reliability between 0 and 1
        self.network_efficiency = self.calculate_network_efficiency()
        self.neighbors = []  # List of neighboring vehicles

    def calculate_network_efficiency(self):
        """Calculate network efficiency based on speed and reliability."""
        return self.speed * self.reliability

    def update_neighbors(self, all_vehicles):
        """Update neighbors based on distance."""
        distance_threshold = 10  # Increase the distance threshold for better neighbor detection
        self.neighbors = [v for v in all_vehicles if v.id != self.id and abs(self.position - v.position) < distance_threshold]
        print(f"Vehicle {self.id} neighbors: {[v.id for v in self.neighbors]}")  # Debug print

    def send_message(self, destination):
        """Send message to destination vehicle."""
        if self.neighbors:
            closest_neighbor = min(self.neighbors, key=lambda v: abs(self.position - v.position))
            distance_to_next = abs(self.position - closest_neighbor.position)
            print(f"Vehicle {self.id} sending message to Vehicle {closest_neighbor.id}. "
                  f"Distance to next vehicle: {distance_to_next:.2f} units. "
                  f"Speed: {self.speed} km/h, Latency: {self.latency:.2f} ms, "
                  f"Reliability: {self.reliability:.2f}, Network Efficiency: {self.network_efficiency:.2f}.")
        else:
            print(f"Vehicle {self.id} has no neighbors to send a message.")

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
        
        # Filter out the sender from neighbors
        valid_neighbors = [v for v in sender.neighbors if v.id != sender.id]

        if not valid_neighbors:
            print(f"Vehicle {sender.id} has no valid neighbors to route to.")
            return

        # Greedily forward to the neighbor closest to the destination
        closest_neighbor = min(valid_neighbors, key=lambda v: abs(destination.position - v.position))
        sender.send_message(closest_neighbor)

        # Check if the closest neighbor is the destination
        if closest_neighbor.id == destination.id:
            print(f"Vehicle {closest_neighbor.id} received message from Vehicle {sender.id}.")
            return
        
        # Continue routing from the closest neighbor
        self.route(closest_neighbor, destination, visited)

# Simulate a platoon of vehicles on a straight road for GRP
def simulate_grp(num_vehicles):
    # Place vehicles in a straight line with reduced spacing
    vehicles = [Vehicle(i, i * 8) for i in range(num_vehicles)]  # Each vehicle spaced 8 units apart on the x-axis
    
    # Update neighbors for each vehicle
    for vehicle in vehicles:
        vehicle.update_neighbors(vehicles)

    # Example routing from Vehicle 0 to Vehicle 9 (only if there are at least 10 vehicles)
    if num_vehicles > 9:
        sender = vehicles[0]
        destination = vehicles[9]
        print(f"\nStarting routing from Vehicle {sender.id} to Vehicle {destination.id}.\n")
        
        # Create instance of Geographic Routing Protocol
        grp = GeographicRoutingProtocol()
        grp.route(sender, destination)
    else:
        print("Not enough vehicles to perform routing from Vehicle 0 to Vehicle 9.")

# Run the simulation for GRP with a defined number of vehicles
simulate_grp(10)
