# Multi Agent Path Finding (MAPF)

This is a small project, visualizing simple implementation of MAPF by creating large state graph. It was done as a semestral project in Artificial Intelligence at my university.
<br>
1) It generates all the possible state space with the possible configurations of the agents and creates a graph based on that.
2) Then, uses A* on the state space graph to find better path based on Manhattan Distance on Heuristics and my custom G function for the "shortest" distance.

<br>
<h3>GUI:</h3>
<img width="399" alt="Screen Shot 2023-05-16 at 17 27 13" src="https://github.com/bel-learning/multi-agent-path-finding/assets/68243292/4c6869d9-b805-4a5e-b47b-c2719fb7bbe9">
<br>
<br>
<h3> To try: </h3>
Simply clone this repo and install pygame library. Required: Python3, Pygame.
<br>
<br>
<h3>Files</h3>
maps/ - contains simple test maps. They are configurable at init(filename) call at main.py.<br>
pathfinding.py - util functions that handles parsing, A* algorithm, generation of state space. <br>
main.py - the program to run. Scroll to the bottom and change the maps in init function. <br>

