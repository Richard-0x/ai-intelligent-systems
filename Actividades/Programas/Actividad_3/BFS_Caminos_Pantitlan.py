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

# 4. MAPA DEL METRO costo unitario = 1
metro_cdmx = {
    'Cuatro Caminos': {'Panteones': 1},
    'Panteones': {'Cuatro Caminos': 1, 'Tacuba': 1},
    'Tacuba': {'Panteones': 1, 'Cuitláhuac': 1, 'Refinería': 1, 'San Joaquín': 1},
    'Cuitláhuac': {'Tacuba': 1, 'Popotla': 1},
    'Popotla': {'Cuitláhuac': 1},
    'Refinería': {'Tacuba': 1, 'Camarones': 1},
    'Camarones': {'Refinería': 1},
    'San Joaquín': {'Tacuba': 1, 'Polanco': 1},
    'Polanco': {'San Joaquín': 1, 'Auditorio': 1},
    'Auditorio': {'Polanco': 1, 'Constituyentes': 1},
    'Constituyentes': {'Auditorio': 1, 'Tacubaya': 1},
    'Tacubaya': {'Constituyentes': 1, 'Patriotismo': 1, 'Observatorio': 1, 'San Pedro de los Pinos': 1},
    'Observatorio': {'Tacubaya': 1},
    'San Pedro de los Pinos': {'Tacubaya': 1},
    'Patriotismo': {'Tacubaya': 1, 'Chilpancingo': 1},
    'Chilpancingo': {'Patriotismo': 1, 'Centro Médico': 1},
    'Centro Médico': {'Chilpancingo': 1, 'Lázaro Cárdenas': 1},
    'Lázaro Cárdenas': {'Centro Médico': 1, 'Chabacano': 1},
    'Chabacano': {'Lázaro Cárdenas': 1, 'Jamaica': 1},
    'Jamaica': {'Chabacano': 1, 'Mixiuhca': 1},
    'Mixiuhca': {'Jamaica': 1, 'Velódromo': 1},
    'Velódromo': {'Mixiuhca': 1, 'Ciudad Deportiva': 1},
    'Ciudad Deportiva': {'Velódromo': 1, 'Puebla': 1},
    'Puebla': {'Ciudad Deportiva': 1, 'Pantitlán': 1},
    'Pantitlán': {'Puebla': 1}
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
            if child.state not in explored and child not in frontier:
                frontier.append(child)
    return None


problema_metro = GraphProblem("Cuatro Caminos", "Pantitlán", metro_cdmx)
nodo_meta = breadth_first_graph_search(problema_metro)

print("Ruta óptima encontrada por BFS:")
for estacion in nodo_meta.path():
    print(f"- {estacion}")
print(f"\nCosto total (Estaciones recorridas): {nodo_meta.path_cost}")