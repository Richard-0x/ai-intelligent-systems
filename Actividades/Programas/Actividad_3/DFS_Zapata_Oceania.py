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

# 4. MAPA DEL METRO 
metro_cdmx = {
    'M.A. Quevedo': {'Viveros': 1},
    'Viveros': {'M.A. Quevedo': 1, 'Coyoacán': 1},
    'Coyoacán': {'Viveros': 1, 'Zapata': 1},
    'Hospital 20 de Noviembre': {'Zapata': 1},
    'Parque de los Venados': {'Zapata': 1},
    'Zapata': {'Parque de los Venados': 1, 'Coyoacán': 1, 'Hospital 20 de Noviembre': 1, 'División del Norte': 1},
    'División del Norte': {'Zapata': 1, 'Eugenia': 1},
    'Eugenia': {'División del Norte': 1, 'Etiopía': 1},
    'Etiopía': {'Eugenia': 1, 'Centro Médico': 1},
    'Centro Médico': {'Etiopía': 1, 'Lázaro Cárdenas': 1, 'Chilpancingo': 1, 'Hospital General': 1},
    'Lázaro Cárdenas': {'Centro Médico': 1},
    'Chilpancingo': {'Centro Médico': 1},
    'Hospital General': {'Centro Médico': 1, 'Niños Héroes': 1},
    'Niños Héroes': {'Hospital General': 1, 'Balderas': 1},
    'Balderas': {'Niños Héroes': 1, 'Juárez': 1, 'Cuauhtémoc': 1, 'Salto del Agua': 1},
    'Juárez': {'Balderas': 1},
    'Cuauhtémoc': {'Balderas': 1},
    'Salto del Agua': {'Balderas': 1, 'San Juan de Letrán': 1, 'Doctores': 1, 'Isabel la Católica': 1},
    'San Juan de Letrán': {'Salto del Agua': 1},
    'Doctores': {'Salto del Agua': 1},
    'Isabel la Católica': {'Salto del Agua': 1, 'Pino Suárez': 1},
    'Pino Suárez': {'Isabel la Católica': 1, 'Merced': 1},
    'Merced': {'Pino Suárez': 1, 'Candelaria': 1},
    'Candelaria': {'Merced': 1, 'San Lázaro': 1},
    'San Lázaro': {'Candelaria': 1, 'Ricardo Flores Magón': 1},
    'Ricardo Flores Magón': {'San Lázaro': 1, 'Romero Rubio': 1},
    'Romero Rubio': {'Ricardo Flores Magón': 1, 'Oceanía': 1},
    'Oceanía': {'Romero Rubio': 1}
}

# 5. ALGORITMO DFS
def depth_first_graph_search(problem):
    start_node = Node(problem.initial)
    if problem.is_goal(start_node.state):
        return start_node
    
    
    frontier = [start_node]
    explored = set()

    while frontier:
        # .pop()
        node = frontier.pop()
        explored.add(node.state)

      
        if problem.is_goal(node.state):
            return node

       
        for child in node.expand(problem):
            
            if child.state not in explored:
                frontier.append(child)
                
    return None

problema_metro = GraphProblem("Zapata", "Oceanía", metro_cdmx)
nodo_meta = depth_first_graph_search(problema_metro)

if nodo_meta:
    print("Ruta encontrada por DFS (Zapata -> Oceanía):")
    for estacion in nodo_meta.path():
        print(f"- {estacion}")
    print(f"\nCosto total (Estaciones recorridas): {nodo_meta.path_cost}")
else:
    print("No se encontró una ruta a la meta.")