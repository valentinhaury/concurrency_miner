from collections import deque
import copy



# CODE FROM CHATGPT 08.07.2026

def trace_self_distance_list(trace):
    trace = copy.deepcopy(trace)

    activities = trace.get_activities()
    edges = trace.get_directly_follows_relations()

    # Adjazenzliste
    graph = {a: [] for a in activities}
    for src, dst in edges:
        graph[src].append(dst)

    result = {}

    for start in activities:

        start_label = activities[start].get_label()

        queue = deque([start])

        # kürzeste Distanz vom Start zu jedem Knoten
        distance = {start: 0}

        # alle Vorgänger auf einem kürzesten Pfad
        parents = {start: []}

        # alle Zielknoten mit minimaler Distanz
        best_distance = None
        best_targets = []

        while queue:

            node = queue.popleft()

            # Wenn wir schon eine Zielaktivität gefunden haben,
            # müssen längere Pfade nicht mehr betrachtet werden.
            if best_distance is not None and distance[node] >= best_distance:
                continue

            for nxt in graph[node]:

                new_dist = distance[node] + 1

                # erster Besuch
                if nxt not in distance:
                    distance[nxt] = new_dist
                    parents[nxt] = [node]
                    queue.append(nxt)

                # gleicher kürzester Weg
                elif new_dist == distance[nxt]:
                    parents[nxt].append(node)

                # gleiches Label gefunden
                if (
                    nxt != start
                    and activities[nxt].get_label() == start_label
                ):
                    if best_distance is None:
                        best_distance = new_dist
                        best_targets = [nxt]
                    elif new_dist == best_distance:
                        best_targets.append(nxt)

        # --------------------------------------------------
        # Alle Aktivitäten auf allen kürzesten Pfaden sammeln
        # --------------------------------------------------

        visited_on_shortest = set()

        def collect(node):
            if node == start:
                return

            visited_on_shortest.add(node)

            for p in parents[node]:
                collect(p)

        if best_distance is not None:
            for target in best_targets:
                collect(target)

            # Start- und Zielaktivitäten entfernen
            visited_on_shortest.discard(start)
            for target in best_targets:
                visited_on_shortest.discard(target)

        result[start] = (
            best_distance,
            list(visited_on_shortest) if best_distance is not None else None
        )

    return result