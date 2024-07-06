from collections import defaultdict
import json
from halerium_utilities.collab import CollabBoard
from halerium_utilities.board.navigator import BoardNavigator


class Graph:
    def __init__(self, vertices):
        # Number of vertices
        self.V = vertices  
        # Dictionary to store adjacency lists
        self.adj = defaultdict(list)
        # Dictionary to map vertices to their corresponding IDs
        self.vertex_to_id = {}
        # Dictionary to map vertices to their corresponding names
        self.vertex_to_name = {}  # Corrected: Added this line
        self.vertex_to_input ={}

    def addEdge(self, u, v):
        # Function to add an edge to the graph
        self.adj[u].append(v)

    def set_vertex_name(self, vertex, name):
        self.vertex_to_name[vertex] = name  # Corrected: Fixed the typo

    def set_vertex_id(self, vertex, id):
        # Function to map a vertex to an ID
        self.vertex_to_id[vertex] = id
    def set_vertex_type_spec(self, vertex, typespec):
        # Function to map a vertex to an ID
        self.vertex_to_input[vertex] = typespec

    def topologicalSort(self):
        # Function to perform Topological Sort
        # Create a list to store in-degree of all vertices
        in_degree = [0] * self.V

        # Traverse adjacency lists to fill in_degree of vertices
        for i in range(self.V):
            for j in self.adj[i]:
                in_degree[j] += 1

        # Create a queue and enqueue all vertices with in-degree 0
        q = []
        for i in range(self.V):
            if in_degree[i] == 0:
                q.append(i)

        # Initialize count of visited vertices
        count = 0

        # Create a list to store topological order
        top_order = []

        # One by one dequeue vertices from queue and enqueue
        # adjacent vertices if in-degree of adjacent becomes 0
        while q:
            # Extract front of queue (or perform dequeue)
            # and add it to topological order
            u = q.pop(0)
            top_order.append(u)

            # Iterate through all its neighbouring nodes
            # of dequeued node u and decrease their in-degree
            # by 1
            for node in self.adj[u]:
                # If in-degree becomes zero, add it to queue
                in_degree[node] -= 1
                if in_degree[node] == 0:
                    q.append(node)

            count += 1

        # Check if there was a cycle
        if count != self.V:
            print("Graph contains cycle")
            return

        # Print topological order
        top_order_names = [self.vertex_to_name[vertex] for vertex in top_order]
        top_order_ids = [self.vertex_to_id[vertex] for vertex in top_order]
        print("Topological Sort Names:", top_order_names)
        print("Topological Sort IDs:", top_order_ids)
        return top_order_ids, top_order_names


def get_current_board_version(board_path: str) -> CollabBoard:
    """
    Returns the current version of a board as a dictionary.

    Args:
        board_path (str): Path to the board

    Returns:
        CollabBoard: CollabBoard instance of the current board version
    """
    c = CollabBoard(board_path, pull_on_init=True)
    return c


def find_frame_card_id(json_data, color_name):
    # Assuming json_data is a dictionary parsed from the JSON string
    nodes = json_data.get('nodes', [])
    selected_frames = []
    # Find the card with type 'frame' and color 'note-color-8'
    for node in nodes:
        if node.get('type') == 'frame' and node.get('type_specific', {}).get('color') == color_name:
            selected_frames.append(node.get('id'))
    
    return selected_frames


def get_cards_in_colored_frame(board, color_name):
    board = CollabBoard(board, pull_on_init = True)
    board_jso = board.to_json()
    board_json = json.loads(board_jso)
    selected_colored_frames = find_frame_card_id(board_json, color_name)
    list_of_cards_in_colored_frame = []
    for colored_frame in selected_colored_frames:
        card_id_list = BoardNavigator(board_json).get_frame_ids(colored_frame)
        list_of_cards_in_colored_frame.extend(card_id_list)
    return list_of_cards_in_colored_frame

def is_in_colored_frame(id, board_path, color_name):
    card_id_list = get_cards_in_colored_frame(board_path, color_name)
    if id in card_id_list:
        return True
    else:
        return False

COLORS = {
    "yellow": "note-color-8", #is_execute_and_show
    "blue":"note-color-4", #is_execute_only
    "red": "note-color-6" #don't care
        } 

def is_execute_and_show(card_id, board_path):
    return is_in_colored_frame(card_id, board_path, COLORS["yellow"])

def is_execute_only(card_id, board_path):
    return is_in_colored_frame(card_id, board_path, COLORS["blue"])


def format_json_to_graph(json_data):
    # Capitalize boolean values in json_data
    
    # Initialize a graph with the number of cards detected
    num_cards = len(json_data['nodes'])
    g = Graph(num_cards)
    
    # Create a mapping from card IDs to vertex indices
    id_to_index = {}
    for index, node in enumerate(json_data['nodes']):
        card_id = node['id']
        id_to_index[card_id] = index
        # Set the vertex ID
        g.set_vertex_id(index, card_id)
        # Set the vertex name (assuming the name is in the 'type' field)
        g.set_vertex_name(index, node['type'])
    
    # Add edges based on the connections
    for edge in json_data['edges']:
        source_id = edge['connections']['source']['id']
        target_id = edge['connections']['target']['id']
        source_index = id_to_index[source_id]
        target_index = id_to_index[target_id]
        g.addEdge(source_index, target_index)
    
    return g


def json_to_string(json_obj):
    # Convert the JSON object to a string with indentation for readability
    json_str = json.dumps(json_obj, indent=4)
    # Wrap the string in triple quotes
    triple_quoted_json_str = f'"""{json_str}"""'
    return triple_quoted_json_str