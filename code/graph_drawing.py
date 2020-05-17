import networkx as nx
import matplotlib.pyplot as plt


def add_room(graph, index, room):
    graph.add_node(room.get_display_name(index), color='green')


def add_edge(graph, room_1, index1, room_2, index2):
    graph.add_edge(room_1.get_display_name(index1), room_2.get_display_name(index2))


def visualize(rooms, ind):
    graph = nx.Graph()
    for i in range(len(ind.room_types)):
        if ind.room_types[i] == 0:
            continue
        add_room(graph, i, rooms[ind.room_types[i]])

    for i in range(len(ind.adj_mat)):
        for j in range(len(ind.adj_mat[i])):
            if ind.adj_mat[i][j] > 0:
                room_1 = rooms[ind.room_types[i]]
                room_2 = rooms[ind.room_types[j]]
                if room_1.is_exterior():
                    graph.nodes[room_2.get_display_name(j)]['color'] = 'red'
                elif room_2.is_exterior():
                    graph.nodes[room_1.get_display_name(i)]['color'] = 'red'
                else:
                    add_edge(graph, room_1, i, room_2, j)

    """
    print(ind.adj_mat)
    print(ind.room_types)
    """
    nx.draw_kamada_kawai(graph, with_labels=True, font_weight='bold', node_color=[node[1]['color'] for node in graph.nodes.data()])
    plt.show()