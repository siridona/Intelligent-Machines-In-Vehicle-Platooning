import random
import time

class Vehicle:
    def __init__(self, id, position, speed):
        self.id = id
        self.position = position
        self.speed = speed
    
    def update_position(self, delta_time):
        # Update vehicle position based on speed and time
        self.position += self.speed * delta_time
    
    def communicate(self, other_vehicle):
        # Simulate URLLC communication with another vehicle
        distance = abs(self.position - other_vehicle.position)
        latency = random.uniform(0.001, 0.005)  # Simulate URLLC latency in seconds
        reliability = random.uniform(0.999, 1.0)  # Simulate reliability close to 100%
        return distance, latency, reliability


class Platoon:
    def __init__(self, vehicles):
        self.vehicles = vehicles
        self.total_communications = 0  # Total number of communication attempts
        self.successful_communications = 0  # Total successful communications

    def update(self, delta_time):
        # Update the positions of all vehicles in the platoon
        for i, vehicle in enumerate(self.vehicles):
            vehicle.update_position(delta_time)
            if i > 0:  # All vehicles except the leader communicate with the vehicle ahead
                distance, latency, reliability = vehicle.communicate(self.vehicles[i - 1])
                
                # Increment total communications
                self.total_communications += 1

                # Get the vehicle ahead
                vehicle_ahead = self.vehicles[i - 1]

                print(f"Vehicle {vehicle.id} (Speed: {vehicle.speed:.2f} m/s) communicating with Vehicle {vehicle_ahead.id} (Speed: {vehicle_ahead.speed:.2f} m/s):")
                print(f"  Distance: {distance:.2f} meters")
                print(f"  Latency: {latency:.4f} seconds")
                print(f"  Reliability: {reliability:.4f}")

                # Adjust speed based on the distance to the vehicle ahead
                if distance < 10:  # If too close, slow down
                    vehicle.speed -= 0.5
                elif distance > 20:  # If too far, speed up
                    vehicle.speed += 0.5
                
                # Simulate success based on reliability
                if random.random() <= reliability:  # Communication successful
                    self.successful_communications += 1

    def calculate_efficiency(self):
        # Calculate network efficiency
        if self.total_communications > 0:
            efficiency = (self.successful_communications / self.total_communications) * 100
        else:
            efficiency = 0
        return efficiency


def simulate_platoon():
    # Initialize vehicles with random starting positions and speeds
    vehicles = [
        Vehicle(id=1, position=0, speed=30),  # Leader
        Vehicle(id=2, position=15, speed=28),
        Vehicle(id=3, position=30, speed=27),
        Vehicle(id=4, position=45, speed=29)
    ]

    platoon = Platoon(vehicles)
    
    # Simulate for 10 seconds with 0.1-second intervals
    for t in range(100):
        delta_time = 0.1  # time step in seconds
        platoon.update(delta_time)
        time.sleep(delta_time)  # Simulate real-time behavior

        # Print network efficiency every second (after 10 iterations)
        if t % 10 == 0:  # Print every 10 iterations (1 second)
            efficiency = platoon.calculate_efficiency()
            print(f"Network Efficiency: {efficiency:.2f}% (Total Communications: {platoon.total_communications}, Successful Communications: {platoon.successful_communications})")

# Call the simulation function to run the simulation
simulate_platoon()
