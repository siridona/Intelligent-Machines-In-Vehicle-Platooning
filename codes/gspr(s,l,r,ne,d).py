import random
import pygame
import math

class Node:
    def __init__(self, x, y, index):
        self.position = (x, y)
        self.index = index
        self.neighbors = []
        self.speed = random.uniform(10, 20)  # Assign random speed between 10 and 20
        self.latency = random.uniform(0.1, 0.5)  # Random latency between 0.1 to 0.5 seconds
        self.reliability = 1 - (1 / self.speed) if self.speed > 0 else 0  # Basic reliability based on speed
        self.network_efficiency = self.speed / (self.latency + 0.1)  # Simplified efficiency calculation

    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

def create_nodes(num_nodes, width, height):
    nodes = []
    for i in range(num_nodes):
        x = random.randint(100, width - 100)
        y = random.randint(100, height - 100)
        nodes.append(Node(x, y, i))  # Assign an index to each node
    return nodes

def connect_nodes(nodes, threshold):
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                dist = distance(nodes[i].position, nodes[j].position)
                if dist < threshold:
                    nodes[i].add_neighbor(nodes[j])

def distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

def gpsr_route(source, destination):
    current = source
    path = [current]
    print(f"Routing from Node {source.index} at {source.position} to Node {destination.index} at {destination.position}")

    while current != destination:
        next_node = None
        best_distance = float('inf')

        for neighbor in current.neighbors:
            dist = distance(neighbor.position, destination.position)
            if dist < best_distance:
                best_distance = dist
                next_node = neighbor

        if next_node and best_distance < distance(current.position, destination.position):
            dist_to_next = distance(current.position, next_node.position)
            print(f"\nNode {current.index} at {current.position} sends packet to Node {next_node.index} at {next_node.position}")
            print(f"Distance to next node: {dist_to_next:.2f}")
            print(f"Speed: {current.speed:.2f} units/s, Latency: {current.latency:.2f}s, Reliability: {current.reliability:.2f}, Network Efficiency: {current.network_efficiency:.2f}")

            current = next_node
            path.append(current)
        else:
            print(f"Node {current.index} at {current.position} cannot find a better neighbor. Stopping routing.")
            break  # Break if greedy forwarding fails
    return path

def visualize(nodes, path, source, destination):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Clear the screen

        # Draw nodes with annotations
        for node in nodes:
            if node == source:
                pygame.draw.circle(screen, (0, 255, 0), (node.position[0], node.position[1]), 10)  # Start node
            elif node == destination:
                pygame.draw.circle(screen, (255, 0, 0), (node.position[0], node.position[1]), 10)  # End node
            else:
                pygame.draw.circle(screen, (0, 0, 255), (node.position[0], node.position[1]), 5)  # Regular nodes
            
            # Draw annotation (index) for each node
            font = pygame.font.Font(None, 24)
            index_text = font.render(str(node.index), True, (0, 0, 0))
            screen.blit(index_text, (node.position[0] + 10, node.position[1] - 15))

        # Draw the routing path with a highlighted line
        if path:
            for i in range(len(path) - 1):
                pygame.draw.line(screen, (255, 0, 0), path[i].position, path[i + 1].position, 4)  # Thicker line for the path

        # Draw labels for source and destination
        font = pygame.font.Font(None, 36)
        source_label = font.render("Start", True, (0, 255, 0))
        dest_label = font.render("End", True, (255, 0, 0))
        screen.blit(source_label, (source.position[0] + 5, source.position[1] - 20))
        screen.blit(dest_label, (destination.position[0] + 5, destination.position[1] - 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def main():
    num_nodes = 50
    width, height = 800, 600
    threshold = 150  # Adjusted threshold for distant nodes

    nodes = create_nodes(num_nodes, width, height)
    connect_nodes(nodes, threshold)

    source = nodes[0]  # Choose the source node
    destination = nodes[9]  # Choose the destination node

    path = gpsr_route(source, destination)

    visualize(nodes, path, source, destination)

if __name__ == "__main__":
    main()
