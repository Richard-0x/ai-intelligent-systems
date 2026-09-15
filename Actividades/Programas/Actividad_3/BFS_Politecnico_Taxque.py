from collections import deque

# 1. CLASE ABSTRACTA
class Problem:
    def __init__(self, initial, goal):
        self.initial = initial 
        self.goal = goal 
    
    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def is_goal(self, state):
        return self.goal == state
    
    def action_cost(self, state1, action, state2):
        return 1
   
    def h(self, state):
        return 0

# 2. CLASE DEL GRAFO
class GraphProblem(Problem):
    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph
    
    def actions(self, state):
        lista = []
        for key in self.graph[state].keys():
            lista.append(key)
        return lista

    def result(self, state, action):
        return action

    def action_cost(self, state1, action, state2):
        return self.graph[state1][state2]

# 3. ESTRUCTURA DEL NODO
class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def path(self):
        lista_path = []
        node = self
        while node:
            lista_path.append(node.state)
            node = node.parent
        return lista_path[::-1]

    def expand(self, problem):
        lista = []
        for action in problem.actions(self.state):
            lista.append(self.child_node(problem, action))
        return lista

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        step_cost = problem.action_cost(self.state, action, next_state)
        return Node(next_state, self, action, self.path_cost + step_cost)

# 4. MAPA DEL METRO Subgrafo relevante con costo unitario = 1
metro_cdmx = {
    'Politécnico': {'Instituto del Petróleo': 1},
    'Instituto del Petróleo': {'Politécnico': 1, 'Autobuses del Norte': 1, 'Vallejo': 1, 'Lindavista': 1},
    'Autobuses del Norte': {'Instituto del Petróleo': 1, 'La Raza': 1},
    'Vallejo': {'Instituto del Petróleo': 1, 'Norte 45': 1},
    'Norte 45': {'Vallejo': 1},
    'Lindavista': {'Instituto del Petróleo': 1, 'Deportivo 18 de Marzo': 1},
    'Deportivo 18 de Marzo': {'Lindavista': 1, 'La Villa-Basílica': 1, 'Indios Verdes': 1, 'Potrero': 1},
    'La Villa-Basílica': {'Deportivo 18 de Marzo': 1},
    'Indios Verdes': {'Deportivo 18 de Marzo': 1},
    'Potrero': {'Deportivo 18 de Marzo': 1, 'La Raza': 1},
    'La Raza': {'Autobuses del Norte': 1, 'Misterios': 1, 'Potrero': 1, 'Tlatelolco': 1},
    'Misterios': {'La Raza': 1, 'Valle Gómez': 1},
    'Valle Gómez': {'Misterios': 1},
    'Tlatelolco': {'La Raza': 1, 'Guerrero': 1},
    'Guerrero': {'Tlatelolco': 1, 'Hidalgo': 1},
    'Hidalgo': {'Guerrero': 1, 'Juárez': 1, 'Revolución': 1, 'Bellas Artes': 1},
    'Juárez': {'Hidalgo': 1, 'Balderas': 1},
    'Balderas': {'Juárez': 1},
    'Revolución': {'Hidalgo': 1, 'San Cosme': 1},
    'San Cosme': {'Revolución': 1},
    'Bellas Artes': {'Hidalgo': 1, 'Allende': 1, 'San Juan de Letrán': 1, 'Garibaldi': 1},
    'San Juan de Letrán': {'Bellas Artes': 1},
    'Garibaldi': {'Bellas Artes': 1},
    'Allende': {'Bellas Artes': 1, 'Zócalo': 1},
    'Zócalo': {'Allende': 1, 'Pino Suárez': 1},
    'Pino Suárez': {'Zócalo': 1, 'San Antonio Abad': 1, 'Isabel la Católica': 1},
    'Isabel la Católica': {'Pino Suárez': 1},
    'San Antonio Abad': {'Pino Suárez': 1, 'Chabacano': 1},
    'Chabacano': {'San Antonio Abad': 1, 'Viaducto': 1, 'Lázaro Cárdenas': 1},
    'Lázaro Cárdenas': {'Chabacano': 1},
    'Viaducto': {'Chabacano': 1, 'Xola': 1},
    'Xola': {'Viaducto': 1, 'Villa de Cortés': 1},
    'Villa de Cortés': {'Xola': 1, 'Nativitas': 1},
    'Nativitas': {'Villa de Cortés': 1, 'Portales': 1},
    'Portales': {'Nativitas': 1, 'Ermita': 1},
    'Ermita': {'Portales': 1, 'General Anaya': 1, 'Eje Central': 1, 'Mexicaltzingo': 1},
    'Eje Central': {'Ermita': 1},
    'Mexicaltzingo': {'Ermita': 1},
    'General Anaya': {'Ermita': 1, 'Taxqueña': 1},
    'Taxqueña': {'General Anaya': 1}
}

# 5. ALGORITMO BFS 
def breadth_first_graph_search(problem):
    start_node = Node(problem.initial)
    
    
    if problem.is_goal(start_node.state):
        return start_node
    
    
    frontier = deque([start_node])
    explored = set()

    while frontier:
        
        node = frontier.popleft()
        explored.add(node.state)

        
        if problem.is_goal(node.state):
            return node

        
        for child in node.expand(problem):
            
            if child.state not in explored and all(child.state != n.state for n in frontier):
                frontier.append(child)
                
    return None

problema_metro = GraphProblem("Politécnico", "Taxqueña", metro_cdmx)
nodo_meta = breadth_first_graph_search(problema_metro)

if nodo_meta:
    print("Ruta óptima encontrada por BFS (Politécnico -> Taxqueña):")
    for estacion in nodo_meta.path():
        print(f"- {estacion}")
    print(f"\nCosto total (Estaciones recorridas): {nodo_meta.path_cost}")
else:
    print("No se encontró una ruta a la meta.")