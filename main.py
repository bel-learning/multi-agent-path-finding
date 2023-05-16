import pygame
import pathfinding
import time
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 51, 51)
GREEN = (51, 255, 51)
YELLOW = (51, 51, 255)
ORANGE = (255, 153, 51)
L_RED = (255, 204, 204)
L_GREEN = (204, 255, 204)
L_YELLOW = (204, 204, 255)
L_ORANGE = (255, 204, 153)

COLORS = [RED, GREEN, YELLOW, ORANGE]
L_COLORS = [L_RED, L_GREEN, L_YELLOW, L_ORANGE]

# Initialize Pygame

# Set up the window
window_width = 400
window_height = 400


# Agent class
class Agent:
    def __init__(self, x, y, radius, color, index):
        self.index = index
        self.x = x
        self.y = y
        self.radius = radius
        self.color= color
    def change_pos(self, x,y):
        self.x = x
        self.y = y
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

# Barrier class
class Barrier:
    def __init__(self, x, y, cell_size):
        self.x = x
        self.y = y
        self.width = cell_size
        self.height = cell_size
    def draw(self, window):
        pygame.draw.rect(window, BLACK, (self.x-self.width/2, self.y-self.height/2, self.width, self.height))

# Create agents and barriers
def init_pygame(window,window_size, row_len, col_len, agents, agents_shadow, barriers):
    
    cell_size = int(window_size / row_len)
    
    # Clear the screen
    window.fill(WHITE)
    for barrier in barriers:
        barrier.draw(window)
   
    for agent_s in agents_shadow:
        agent_s.draw(window)

    for agent in agents:
        agent.draw(window)
   
    # Draw grid lines
    line_color = BLACK
    line_thickness = 1
    for x in range(0, window_width, cell_size):
        pygame.draw.line(window, line_color, (x, 0), (x, window_height), line_thickness)
    for y in range(0, window_height, cell_size):
        pygame.draw.line(window, line_color, (0, y), (window_width, y), line_thickness)

    pygame.display.flip()

# Quit the application
def xy_to_coordinate(row,col, cell_size):
    row = row+1
    col = col+1
    return (col*cell_size) - (cell_size/2),(row*cell_size) - (cell_size/2)

def findBariers(map):
    barries = []
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == '@':
                barries.append([i,j])

    return barries

def findAgent(id, agents):
    for agent in agents:
        if agent.index == id:
            return agent
    return None

def mergePath(path, goal_tuple):
    agent_count = len(goal_tuple)
    merged_path = [path[0]]
    last_tuple = list(path[0])
    for i in range(1, len(path)):
        current_tuple = path[i]
        is_distinct = True
        print(last_tuple)
        # Check if the current tuple is at the goal state or distinct from the previous tuples
        for j in range(len(current_tuple)):
            if last_tuple[j] == goal_tuple[j]:
                continue

            if current_tuple[j] == last_tuple[j]:
                # print("equal", current_tuple[j], last_tuple[j])
                is_distinct = False
            else:
                last_tuple[j] = current_tuple[j]

        if is_distinct:
            merged_path.append(tuple(last_tuple))

    return merged_path




def init(filename):
    map,agents,agent_start, agent_goal = pathfinding.parseMap(filename)
    # pathfinding.findPath(pathfinding.cleanMap(map), agents, agent_start, agent_goal)
    print(agents)
    print("start:", agent_start)
    print("goal:", agent_goal)

    agents_obj = []
    agents_shadow = []
    cell_size = 400 / len(map)
    colorI = 0
 
    colorI = 0
    for agent in agents:
        start_value = agent_start[agent]
        coord_x,coord_y = xy_to_coordinate(start_value[0], start_value[1], cell_size)
        agents_obj.append(Agent(coord_x, coord_y, cell_size/3, COLORS[colorI], colorI))

        end_value = agent_goal[agent]
        coord_x,coord_y = xy_to_coordinate(end_value[0], end_value[1], cell_size)
        agents_shadow.append(Agent(coord_x, coord_y, cell_size/3, L_COLORS[colorI], colorI))
        colorI = colorI + 1

    
    row_len = len(map)
    col_len = len(map[0])

    barriers = findBariers(map)
    barriers_obj = []
    for coord in barriers:
        x,y = xy_to_coordinate(coord[0], coord[1], cell_size)
        barriers_obj.append(Barrier(x,y, cell_size))

    pygame.init()
    window = pygame.display.set_mode((window_width, window_height)) 
    pygame.display.set_caption("MAPF")
    init_pygame(window,400, row_len, col_len, agents_obj, agents_shadow, barriers_obj)


    print(pathfinding.cleanMap(map))
    path = pathfinding.findPath(pathfinding.cleanMap(map), agents, agent_start, agent_goal)
    path = path[::-1]
    # Main Event Loop
    print(path, len(path))
    
    if path == None:
        print("No path")
        return
    
    path_index = 0
    move_speed = 2
    move_counter = 0

    running = True

    sorted_goals = [(agent_goal[key]) for key in sorted(agent_goal)] 
    # path = mergePath(path, sorted_goals)
    # print("merged", path)
    print(sorted_goals)
    # path = mergePath(path, sorted_goals)
    # print("merged", path)
    time.sleep(3.5)
    print("> Path found! Beginning")
    is_paused = False
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_paused = not is_paused
                    print(f"paused: {is_paused}")
        if is_paused:
            continue
        # Run the path
        if path_index < len(path):
            new_agent_obj = agents_obj
            agent_index = 0
            for new_x,new_y in path[path_index]:
                # print(new_x, new_y)
                pre_agent = findAgent(agent_index, agents_obj)
                x,y = xy_to_coordinate(new_x, new_y, cell_size)
                pre_agent.change_pos(x,y)
                new_agent_obj.append(pre_agent)
                agent_index = agent_index + 1
        # if tuple(new_agent_obj) == agent_goal
        init_pygame(window, 400, row_len, col_len, new_agent_obj, agents_shadow, barriers_obj)
        path_index = path_index + 1
      
        time.sleep(0.8)

        if path_index == len(path):
            print("Finished!")
            time.sleep(2)
            return

        


    pygame.quit()

if __name__ == "__main__":
    init("maps/map6.map")
    init("maps/map7.map")

    # init("maps/map6.map")
    # init("maps/map5.map")
    # init("maps/map2.map")
    # init("maps/map4.map")
