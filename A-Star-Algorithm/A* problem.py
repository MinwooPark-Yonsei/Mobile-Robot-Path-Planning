# Use Manhattan distance as the heuristic function
from typing import Tuple, List
from heapq import heappush, heappop

def find_shortest_path(start: Tuple[int, int],
                        end: Tuple[int, int],
                        obstacles: List[Tuple[int, int]])\
                        -> List[Tuple[int, int]]:
    
    class Node:
        def __init__(self, position: Tuple[int, int], parent=None):
            self.position = position
            self.parent = parent
            self.g_score = 0
            self.h_score = 0
            self.f_score = 0

        def __lt__(self, other):
            return self.f_score < other.f_score

    current = Node(position=start)
    shortest_path = []
    open_nodes = []
    closed_nodes_pos = []
    
    while current.position != end:
        # Consider every neighboring nodes.
        for move in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            neighbor = Node(position=(current.position[0] + move[0], current.position[1] + move[1]), 
                            parent=current)
            if neighbor.position in obstacles or neighbor.position in closed_nodes_pos:
                continue

            if abs(move[0]) + abs(move[1]) == 1:
                neighbor.g_score = current.g_score + 10
            else:
                neighbor.g_score = current.g_score + 14
            
            # Manhattan distance
            neighbor.h_score = abs(end[0]-neighbor.position[0]) + abs(end[1]-neighbor.position[1])

            neighbor.f_score = neighbor.g_score + neighbor.h_score

            # If the neighbor is already in open_nodes and the new f_score is smaller than the existing one, update.
            # Else if the neighbor is already in open_nodes but the new f_score is larger than or same with, continue.
            no_update = False
            for node in open_nodes:
                if node.position == neighbor.position and node.f_score > neighbor.f_score:
                    open_nodes.remove(node)
                    break

                elif node.position == neighbor.position and node.f_score <= neighbor.f_score:
                    no_update = True

            if no_update == True:
                continue
            
            heappush(open_nodes, neighbor)
        
        closed_nodes_pos.append(current.position)
        current = heappop(open_nodes)

    while current.position != start:
        shortest_path.insert(0, current.position)
        current = current.parent
    shortest_path.insert(0, start)

    return shortest_path
        

if __name__ == '__main__':
    start = (0, 0)
    end = (10, 10)
    obstacles = [(1, 1), (2, 2)]
    print(find_shortest_path(start, end, obstacles))