from queue import PriorityQueue
import itertools
total_states = 0

def is_valid_state(state, map):
    rows=len(map)-1
    cols=len(map[0])-1

    for agent_state in state:
        x, y = agent_state
        if x < 0 or x > rows or y < 0 or y > cols or map[x][y] == '@':
            return False
    return True

def has_duplicate(state):
    return len(set(state)) != len(state)

def heuristic(current_state, goal_state):
    length = len(current_state)
    res = 0
    for i in range(length):
        x1,y1 = current_state[i]
        x2,y2 = goal_state[i]
        res += abs(x2-x1) + abs(y2-y1)
    return res

def count_move(tuple1, tuple2, goal_state):
    count = 0
    for i in range(len(goal_state)):
        # If current is goal and next is not. Prioritize staying in place
        if tuple1[i] == goal_state[i] and tuple2[i] == goal_state[i]:
            count += 1
    for i in range(len(tuple1)):
        if tuple1[i] != tuple2[i]:
            count += 1
    return count


def a_star(start_state, goal_state, graph):
    open_set = PriorityQueue()
    open_set.put((0, start_state))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start_state] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start_state] = heuristic(start_state, goal_state)

    while not open_set.empty():
        current = open_set.get()[1]
        if current == goal_state:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start_state)
            return path
        for neighbor in graph[current]:
            # g function -> 
            
            # 1. Priotizing path that requires least amount of len(path)
            # (len(current) + 1) - count_move(current, neighbor)

            # 2. Just blind plus 1. Works fine.
            # + 1
            
            tentative_g_score = g_score[current] + abs((len(current) + 1)*2 - count_move(current, neighbor, goal_state) )
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal_state)
                open_set.put((f_score[neighbor], neighbor))
    return None

def get_neighbors(state, map):
        neighboring_states = []
        for i, agent_state in enumerate(state):
            x,y = agent_state
            possible_neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            for neighbor in possible_neighbors:
                new_state = list(state)
                new_state[i] = neighbor
                if is_valid_state(new_state, map) and not has_duplicate(new_state):
                    neighboring_states.append(tuple(new_state))
        transpose = [list(row) for row in zip(*neighboring_states)]
        cartesian_product = list(itertools.product(*transpose))
        new_neighbours = []
        # print("cart: ", cartesian_product)
        for item in cartesian_product:
            # print(item)
            if not has_duplicate(item):
                new_neighbours.append(item)
        return list(new_neighbours)

def generateStateSpace(map, initial_state, goal_state):
    rows=len(map)
    cols=len(map[0])
    graph = {}

    stack = [initial_state]
    visited = set()
# Generate total state space that is valid and put it into graph0
    while stack:
        current_state = stack.pop()
        if current_state not in graph:
            graph[current_state] = []
        for neighbor_state in get_neighbors(current_state, map=map):
            if neighbor_state not in visited:
                stack.append(neighbor_state)
                visited.add(neighbor_state)
            graph[current_state].append(neighbor_state)

    return graph

def parseMap(filename):
    map = []
    with open(filename, "r") as file:
        for line in file:
            line = line[:-1]
            row = [char for char in line]
            map.append(row)

    letter_to_num = {
        "1" : "a",
        "2" : "b",
        "3" : "c",
        "4" : "d",
        "5" : "e",
        "6" : "f",
        "7" : "g",
        "8" : "h",
        "9" : "i"
        # Add more mappings for other characters as needed
    }

    agents = {}
    agent_start = {}
    agent_dest = {}

    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j].isalpha():
                agent = map[i][j]
                agent_start[agent] = [i,j]
                agents[agent] = 0

            if map[i][j].isdigit():
                dest = map[i][j]
                agent_dest[letter_to_num[dest]] = [i,j]

    return map, agents,agent_start,agent_dest
def cleanMap(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j].isalpha():
                map[i][j] = '.'

            if map[i][j].isdigit():
                map[i][j] = '.'
    return map
def returnAgents(map):
    agents = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j].isalpha():
                agents.append(map[i][j])
    return agents

def findPath(map, agents, agent_start, agent_dest):
    initial_state = []
    goal_state = []
    for agent in agents.keys():
        initial_state.append(tuple(agent_start[agent]))
        goal_state.append(tuple(agent_dest[agent]))

    initial_state = tuple(initial_state)
    goal_state = tuple(goal_state)

    graph = generateStateSpace(map, initial_state, goal_state)

    # print((graph.keys()))
    
    path = a_star(initial_state, goal_state, graph)

    if path == None:
        print("No path found")
    else:
        print("path:", path)
    return path

def init(filename):
    map, agents, agent_start, agent_dest = parseMap(filename)
    map = cleanMap(map)
    return findPath(map, agents, agent_start, agent_dest)
    # Combine everything together.
    # State will [[aX, aY], [bX, bY]]

    


# init("map2.map")


