#!/usr/bin/env python3
"""
Parse CRESR126 CSV data and extract network topology for PMU placement.

The CRESR126 model is a real Japanese 6.6kV urban distribution system
(Tokyo metropolitan area) with ~2,500 buses and 3 substations.

This script:
  1. Reads node.csv, Line.csv, hload.csv, Lload.csv
  2. Builds a spanning tree (radial topology) from the full graph
  3. Identifies zero-injection buses (no load, no generation)
  4. Exports the topology as JSON for use in HTML demos
"""
import csv
import json
import os
from collections import defaultdict, deque

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, '..', 'data')


def parse_network(data_dir=None):
    """Parse CREST CSV files and return network topology.

    Returns
    -------
    dict with keys:
        'name', 'n_buses', 'buses', 'branches', 'zero_injection_buses',
        'substation_buses', 'node_names', 'coordinates', 'loads'
    """
    if data_dir is None:
        data_dir = DATA_DIR

    # Read nodes
    nodes = []
    coords = {}
    with open(os.path.join(data_dir, 'node.csv')) as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            name = row[0].strip()
            lat, lon = float(row[1]), float(row[2])
            nodes.append(name)
            coords[name] = (lat, lon)

    # Read lines
    lines = []
    with open(os.path.join(data_dir, 'Line.csv')) as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            fn = row[0].strip()
            tn = row[1].strip()
            lt = row[2].strip()
            length_m = float(row[3])
            is_feeder = int(row[4])
            lines.append((fn, tn, lt, length_m, is_feeder))

    # Read loads
    load_nodes = set()
    # High-voltage loads
    with open(os.path.join(data_dir, 'hload.csv')) as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            load_nodes.add(row[0].strip())

    # Low-voltage loads (pole transformers)
    with open(os.path.join(data_dir, 'Lload.csv')) as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            load_nodes.add(row[0].strip())

    # Build full graph
    node_set = set(nodes)
    adj = defaultdict(set)
    edge_list = []
    for fn, tn, lt, length_m, is_feeder in lines:
        if fn in node_set and tn in node_set:
            adj[fn].add(tn)
            adj[tn].add(fn)
            edge_list.append((fn, tn, is_feeder))

    # BFS spanning tree from substations
    substations = ['F1HN0', 'F2HN0', 'F3HN0']
    visited = set()
    tree_edges = []
    queue = deque()
    for sn in substations:
        if sn in node_set and sn not in visited:
            visited.add(sn)
            queue.append(sn)

    while queue:
        node = queue.popleft()
        for nb in adj[node]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
                tree_edges.append((node, nb))

    # Node name -> 1-indexed bus ID
    used_nodes = sorted(visited)
    name_to_id = {name: i + 1 for i, name in enumerate(used_nodes)}
    n_buses = len(used_nodes)

    # Branches as (from_id, to_id)
    branches = [(name_to_id[fn], name_to_id[tn]) for fn, tn in tree_edges
                if fn in name_to_id and tn in name_to_id]

    # Substation bus IDs (generators)
    substation_buses = [name_to_id[sn] for sn in substations
                        if sn in name_to_id]

    # Zero-injection buses: no load AND not a substation
    zi_buses = []
    for name in used_nodes:
        if name not in load_nodes and name not in substations:
            zi_buses.append(name_to_id[name])

    # Coordinates for visualization
    coord_list = []
    for name in used_nodes:
        if name in coords:
            coord_list.append({
                'id': name_to_id[name],
                'name': name,
                'lat': coords[name][0],
                'lon': coords[name][1],
            })

    # Compute load per bus
    load_per_bus = {}
    for name in used_nodes:
        if name in load_nodes:
            load_per_bus[name_to_id[name]] = True

    result = {
        'name': 'CREST 126-Feeder Distribution System',
        'n_buses': n_buses,
        'buses': list(range(1, n_buses + 1)),
        'branches': branches,
        'zero_injection_buses': zi_buses,
        'substation_buses': substation_buses,
        'node_names': {name_to_id[n]: n for n in used_nodes},
        'coordinates': coord_list,
        'n_load_buses': len([n for n in used_nodes if n in load_nodes]),
        'n_zi_buses': len(zi_buses),
        'n_substations': len(substation_buses),
    }
    return result


def export_json(output_path=None):
    """Export network topology as JSON for HTML demo."""
    if output_path is None:
        output_path = os.path.join(BASE, '..', 'data', 'crest126_topology.json')

    data_dir = DATA_DIR
    # Check if data files exist, otherwise try Downloads
    if not os.path.exists(os.path.join(data_dir, 'node.csv')):
        data_dir = os.path.expanduser('~/Downloads/CRESR126model')

    net = parse_network(data_dir)

    # Slim down for JSON export
    export_data = {
        'name': net['name'],
        'n_buses': net['n_buses'],
        'branches': net['branches'],
        'zero_injection_buses': net['zero_injection_buses'],
        'substation_buses': net['substation_buses'],
        'coordinates': net['coordinates'],
        'n_load_buses': net['n_load_buses'],
        'n_zi_buses': net['n_zi_buses'],
    }

    with open(output_path, 'w') as f:
        json.dump(export_data, f)

    print(f"Exported: {output_path}")
    print(f"  Buses: {net['n_buses']}")
    print(f"  Branches: {len(net['branches'])}")
    print(f"  Zero-injection buses: {net['n_zi_buses']}")
    print(f"  Load buses: {net['n_load_buses']}")
    print(f"  Substations: {net['n_substations']}")

    return net


if __name__ == '__main__':
    export_json()
