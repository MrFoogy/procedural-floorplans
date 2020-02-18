import networkx as nx
import matplotlib.pyplot as plt


def add_room(graph, index, room):
    graph.add_node(room.get_display_name(index), color='green')


def add_edge(graph, room_1, index1, room_2, index2):
    graph.add_edge(room_1.get_display_name(index1), room_2.get_display_name(index2))


def visualize(rooms, ind):
    graph = nx.Graph()
    for i in range(len(ind.meta.room_types)):
        if ind.meta.room_types[i] == 0:
            continue
        add_room(graph, i, rooms[ind.meta.room_types[i]])

    for i in range(len(ind)):
        for j in range(len(ind[i])):
            if ind[i][j] > 0:
                room_1 = rooms[ind.meta.room_types[i]]
                room_2 = rooms[ind.meta.room_types[j]]
                if room_1.is_exterior():
                    graph.nodes[room_2.get_display_name(j)]['color'] = 'red'
                elif room_2.is_exterior():
                    graph.nodes[room_1.get_display_name(i)]['color'] = 'red'
                else:
                    add_edge(graph, room_1, i, room_2, j)

    print(graph.nodes.data())
    nx.draw(graph, with_labels=True, font_weight='bold', node_color=[node[1]['color'] for node in graph.nodes.data()])
    plt.show()