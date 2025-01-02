import pygame
import random
import math

# Node class
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def distance_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

# Packet class
class Packet:
    def __init__(self, src, dest, data):
        self.src = src
        self.dest = dest
        self.data = data
        self.speed = random.uniform(1, 5)  # Random speed between 1 and 5 units per frame
        self.latency = random.uniform(50, 200)  # Latency in milliseconds
        self.reliability = random.uniform(0.5, 1.0)  # Reliability between 0 and 1
        self.network_efficiency = self.calculate_network_efficiency()

    def calculate_network_efficiency(self):
        """Calculate network efficiency based on speed and reliability."""
        return self.speed * self.reliability

# Function to draw nodes and packets
def draw_nodes(screen, nodes, packets):
    for node in nodes:
        pygame.draw.circle(screen, (0, 255, 0), (int(node.x), int(node.y)), 5)
    for packet in packets:
        pygame.draw.line(screen, (255, 0, 0), (int(packet.src.x), int(packet.src.y)), (int(packet.dest.x), int(packet.dest.y)), 2)

# Greedy routing function
def greedy_routing(src, dest):
    current = src
    path = [current]
    
    while current != dest:
        closest = None
        closest_dist = float('inf')
        for neighbor in current.neighbors:
            dist = neighbor.distance_to(dest)
            if dist < closest_dist:
                closest = neighbor
                closest_dist = dist
        if closest is None:
            print("No more neighbors to route through.")
            break
        
        # Print the distance to the next node
        distance_to_next = current.distance_to(closest)
        print(f"Distance from Node ({current.x}, {current.y}) to Node ({closest.x}, {closest.y}): {distance_to_next:.2f} units")
        
        current = closest
        path.append(current)

    return path

# Main function to run the simulation
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Geographic Routing Protocol Simulation")
    clock = pygame.time.Clock()

    # Create nodes
    nodes = [Node(random.randint(50, 750), random.randint(50, 550)) for _ in range(20)]
    
    # Create neighbors (for simplicity, connect nodes within 100 pixels)
    for node in nodes:
        for other in nodes:
            if node != other and node.distance_to(other) < 100:  
                node.add_neighbor(other)

    # Create a packet
    src = random.choice(nodes)
    dest = random.choice(nodes)
    while dest == src:
        dest = random.choice(nodes)
    packet = Packet(src, dest, "Hello!")

    # Perform greedy routing
    path = greedy_routing(src, dest)

    # Print packet attributes
    print(f"Packet Source: ({packet.src.x}, {packet.src.y})")
    print(f"Packet Destination: ({packet.dest.x}, {packet.dest.y})")
    print(f"Speed: {packet.speed:.2f} units/frame")
    print(f"Latency: {packet.latency:.2f} ms")
    print(f"Reliability: {packet.reliability:.2f}")
    print(f"Network Efficiency: {packet.network_efficiency:.2f}")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        draw_nodes(screen, nodes, [packet])

        # Draw the path of the greedy routing
        for i in range(len(path) - 1):
            pygame.draw.line(screen, (0, 0, 255), (int(path[i].x), int(path[i].y)), (int(path[i + 1].x), int(path[i + 1].y)), 2)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
