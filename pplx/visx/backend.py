from flask import Flask, render_template, request
import networkx as nx
import json
from pplx.settings import FOLDER_PATH
from pplx.parser import load, statements_to_graph
import uuid

app = Flask(__name__)

GRAPH = None
NODES = None
NODE_DICT = {}
COLORS = {'variable': '#7a7a7a', 'relation': '#dd4b39'}


def format_graph(graph: nx.Graph) -> nx.Graph:
    for node in graph.nodes:
        graph.nodes[node]['id'] = str(uuid.uuid4())
        if graph.nodes[node]['node_type'] != 'variable':
            graph.nodes[node]['color'] = COLORS['relation']
        else:
            graph.nodes[node]['color'] = COLORS['variable']
        graph.nodes[node]['shape'] = 'dot'
        graph.nodes[node]['borderWidth'] = 0
        graph.nodes[node]['size'] = 10
        graph.nodes[node]['label'] = " ".join(node.split()[1:])
    for source, destination in graph.edges:
        graph[source][destination]['id'] = str(uuid.uuid4())
        graph[source][destination]['from'] = source
        graph[source][destination]['to'] = destination
        graph[source][destination]['width'] = 2
        graph[source][destination]['color'] = COLORS['variable']
    return graph


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nodes', methods=['GET'])
def nodes():
    return NODES

@app.route('/related', methods=['POST'])
def related():
    data = request.get_json()
    node = data['request']
    graph = GRAPH.subgraph(nx.node_connected_component(GRAPH.to_undirected(), NODE_DICT[node]))
    graph = format_graph(graph)
    data = nx.json_graph.node_link_data(graph)
    return json.dumps(data)

if __name__ == '__main__':
    relations, statements = load(FOLDER_PATH)
    GRAPH = statements_to_graph(statements)
    node_names = [node for node in GRAPH.nodes if GRAPH.nodes[node]['node_type'] == 'variable']
    for node_name in node_names:
        NODE_DICT[" ".join(node_name.split()[1:])] = node_name
    NODES = json.dumps([{"id": node, "text": node} for node in NODE_DICT.keys()])
    app.run()
