import math

data = {
    "Weedon Carp 60": (54.794444, -123.086667),
    "Burnt pine": (56.428210, -120.699450),
    "Predicted Pos": (55.67599332, -122.71791481),
    "Moberly": (55.82300, -121.76200),
    "Hart Ranges": (54.727583180778744, -122.09576522819326),
    "Monkman Provincial Park": (54.54778, -121,17227),
    "Sentinel Peak": (54.908111, -121.961111),
    "Gwillam Lake Provincial Park": (55,421738, -121,279839)
}

class Graph:
    def __init__(self, n_vertices, places, nodes):
        self.n_vertices = n_vertices
        self.n_edges = [[0 for _ in range(self.n_vertices)] for _ in range(self.n_vertices)]
        self.places = places
        self.nodes = nodes

    def calculate_distance(self, value_u, value_v):
        R = 6378
        dif_long = math.radians(value_u[0]) - math.radians(value_v[0])
        dif_lat = math.radians(value_u[0]) - math.radians(value_v[0])
        mean_lat = (math.radians(value_u[1]) + math.radians(value_v[1]))/2
        right_part = (math.cos(mean_lat)*dif_long)**2
        left_part = dif_lat**2
        distance = round(R*math.sqrt(left_part + right_part), 1)
        return distance
    
    def add_edges(self, node_u, node_v):
        u_index = self.places.index(node_u.value)
        v_index = self.places.index(node_v.value)
        distance = self.calculate_distance(node_u.pos, node_v.pos)
        self.n_edges[u_index][v_index] = distance
        self.n_edges[v_index][u_index] = distance
    
    def to_string(self):
        for i in range(len(self.n_edges)):
            print(self.n_edges[i])
        pass

    def get_value(self, u_index, v_index):
        return self.n_edges[u_index][v_index]
    
    def get_neighboors(self, node):
        val = node.value
        index = self.places.index(val)
        nodes_list = []
        for i in range(len(self.nodes)):
            if self.n_edges[i][index] != 0:
                nodes_list.append(self.nodes[i])
        return nodes_list
    

class Node:
    def __init__(self, value, position):
        self.value = value
        self.pos = position

def get_min_dis(list_dis):
    mini = list_dis[0][0]
    index = 0
    for i in range(len(list_dis)):
        if mini > list_dis[i][0]:
            mini = list_dis[i][0]
            index = i
    name = list_dis[index][1].value
    value = list_dis[index][0]
    return (name, value)

places_name = []
nodes = []

for key, value in data.items():
    places_name.append(key)
    node = Node(key, value)
    nodes.append(node)

start = places_name.index("Hart Ranges")
destination = places_name.index("Predicted Pos")

n_vertices = len(places_name)
graph = Graph(n_vertices, places_name, nodes)
for i in range(len(nodes)):
    for j in range(len(nodes)):
        graph.add_edges(nodes[i], nodes[j])

distances = []
for i in range(len(places_name)):
    if i != start and i != destination: 
        dis = graph.get_value(start, i)
        dis += graph.get_value(i, destination)
        distances.append((round(dis, 2), nodes[i]))
# print(distances)
# print(graph.n_edges[start][destination])

# print(distances)
print(get_min_dis(distances))
# graph.to_string()