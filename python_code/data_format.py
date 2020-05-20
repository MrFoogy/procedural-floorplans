import ga


def format_full_output(logbook_chapters, hof, config):
    return {"graph": format_log_output(logbook_chapters), "hof": serialize_hof(hof, config)}


def format_log_output(logbook_chapters):
    res = { "data": {}, "titles": list(logbook_chapters.keys())}
    for line_title in logbook_chapters.keys():
        res["data"][line_title] = {}
        stat_titles = list(set(logbook_chapters[line_title][0].keys()) - set(["gen", "nevals"]))
        for stat_title in stat_titles:
            res["data"][line_title][stat_title] = []
            for entry in logbook_chapters[line_title]:
                res["data"][line_title][stat_title].append(entry[stat_title])

    return res


def serialize_hof(hof, config):
    return [serialize_building(building, config) for building in hof]


def serialize_building(individual, config):
    res = {"room_types": individual.room_types, "nodes": [], "edges": [], "scores": serialize_building_fitness(individual, config)}
    for i in range(1, len(individual.room_types)):
        res["nodes"].append({"id": i, "room_type": individual.room_types[i], "label": config.rooms[individual.room_types[i]].get_display_name(), "exterior_connected": False})

    for i in range(len(individual.adj_mat)):
        for j in range(len(individual.adj_mat[i])):
            if individual.adj_mat[i][j] > 0:
                room_1 = config.rooms[individual.room_types[i]]
                room_2 = config.rooms[individual.room_types[j]]
                if room_1.is_exterior():
                    res["nodes"][j - 1]["exterior_connected"] = True
                elif room_2.is_exterior():
                    res["nodes"][i - 1]["exterior_connected"] = True
                else:
                    res["edges"].append({"from": i, "to": j})
    
    return res


def serialize_building_fitness(individual, config):
    return { 
            "fitness": ga.get_fitness(individual, config)[0],
            "adj_score": individual.get_adjacency_score(config), 
            "utility_score": individual.get_utility_score(config), 
            "valency_pen": individual.get_valence_violation(config), 
            "num_rooms_pen": individual.get_num_room_types_violation(config), 
           }