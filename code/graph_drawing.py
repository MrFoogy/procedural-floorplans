import networkx as nx
import matplotlib.pyplot as plt


def add_room(graph, room):
    graph.add_node(room.get_display_name(), color='green')


def add_edge(graph, room_1, room_2):
    graph.add_edge(room_1.get_display_name(), room_2.get_display_name())


def visualize(rooms, ind):
    graph = nx.Graph()
    for room in rooms:
        if room.ident == 0:
            continue
        add_room(graph, room)

    for room_1 in rooms:
        for room_2 in rooms:
            if ind.meta.get_adj_value(ind, room_1.ident, room_2.ident) > 0:
                if room_1.is_exterior():
                    graph.nodes[room_2.get_display_name()]['color'] = 'red'
                elif room_2.is_exterior():
                    graph.nodes[room_1.get_display_name()]['color'] = 'red'
                else:
                    add_edge(graph, room_1, room_2)

    print(graph.nodes.data())
    nx.draw(graph, with_labels=True, font_weight='bold', node_color=[node[1]['color'] for node in graph.nodes.data()])
    plt.show()