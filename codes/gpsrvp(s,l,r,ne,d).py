import random
import math
import time

class Vehicle:
    def __init__(self, id, position, speed):
        self.id = id
        self.position = position  # (x, y) tuple
        self.speed = speed  # Speed of the vehicle
        self.neighbors = []  # List of neighboring vehicles

    def update_neighbors(self, all_vehicles):
        """Update neighbors based on distance."""
        self.neighbors = [v for v in all_vehicles if v.id != self.id and self.distance(v) < 20]  # Example distance threshold

    def distance(self, other_vehicle):
        """Calculate Euclidean distance to another vehicle."""
        return math.sqrt((self.position[0] - other_vehicle.position[0]) ** 2 + 
                         (self.position[1] - other_vehicle.position[1]) ** 2)

    def send_message(self, destination):
        """Send message to destination vehicle."""
        # Simulate latency based on speed
        latency = random.uniform(0.01, 0.1)  # Latency between 10ms and 100ms
        time.sleep(latency)  # Simulate time delay for message sending

        # Calculate and print distance to the next vehicle
        distance_to_next_vehicle = self.distance(destination)

        # Simulate reliability
        reliability = random.uniform(0, 1)  # Random number between 0 and 1
        if reliability < 0.8:  # 80% success rate for message delivery
            print(f"Vehicle {self.id} sending message to Vehicle {destination.id}.")
            print(f"Distance to Vehicle {destination.id}: {distance_to_next_vehicle:.2f} meters")
            print(f"Speed: {self.speed} units/s, Latency: {latency:.2f} seconds, Reliability: {reliability:.2f}")
            return True, reliability  # Message sent successfully
        else:
            print(f"Vehicle {self.id} failed to send message to Vehicle {destination.id}. Reliability: {reliability:.2f}")
            return False, reliability  # Message failed to send

class GreedyPerimeterStatelessRouting:
    def __init__(self):
        self.total_messages = 0
        self.successful_messages = 0
        self.reliabilities = []  # List to store reliability values

    def route(self, sender, destination, visited=None):
        """Route message using GPSR with added logic for large platoon and straight road."""
        if visited is None:
            visited = set()  # Initialize visited set if not provided

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
        success, reliability = sender.send_message(closest_neighbor)
        self.total_messages += 1  # Increment for the attempted message

        if success:
            self.reliabilities.append(reliability)  # Store reliability of the successful message
            if closest_neighbor.id == destination.id:
                print(f"Vehicle {destination.id} received message successfully.")
                self.successful_messages += 1
                return

            # Continue routing from the closest neighbor
            self.route(closest_neighbor, destination, visited)

    def print_network_efficiency(self):
        """Print network efficiency and reliability statistics."""
        if self.total_messages > 0:
            efficiency = (self.successful_messages / self.total_messages) * 100  # Efficiency in percentage
            avg_reliability = sum(self.reliabilities) / len(self.reliabilities) if self.reliabilities else 0
            print(f"\nNetwork Efficiency: {efficiency:.2f}%")
            print(f"Total Messages Sent: {self.total_messages}, Successful Messages: {self.successful_messages}")
            print(f"Average Reliability of Successful Messages: {avg_reliability:.2f}")

# Simulate a straight road platoon of vehicles for GPSR
def simulate_gpsr(num_vehicles):
    # Position vehicles in a line along the x-axis and assign random speeds
    vehicles = [Vehicle(i, (i * 10, 0), random.uniform(5, 15)) for i in range(num_vehicles)]
    
    # Update neighbors for each vehicle based on proximity
    for vehicle in vehicles:
        vehicle.update_neighbors(vehicles)

    # Route from the first vehicle to the last vehicle
    sender = vehicles[0]
    destination = vehicles[-1]
    print(f"Starting routing from Vehicle {sender.id} to Vehicle {destination.id}.\n")
    
    # Use Greedy Perimeter Stateless Routing
    gpsr = GreedyPerimeterStatelessRouting()
    gpsr.route(sender, destination)
    
    # Print network efficiency and reliability statistics
    gpsr.print_network_efficiency()

# Run the simulation with a larger number of vehicles in a straight line
simulate_gpsr(10)
