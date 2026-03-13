"""
IEEJ EAST 30-machine system data parser
Parse Y-method format data from IEEJ official files
Extract bus/branch topology for PMU placement analysis
"""

import re

def parse_east30(filepath="/tmp/DataWIN/east30p/s.txt"):
    buses = set()
    branches = []  # (from, to, r, x, b)
    generators = {}  # bus -> (Pg, Qg)
    loads = {}  # bus -> (Pl, Ql)
    transformers = []

    with open(filepath) as f:
        lines = f.readlines()

    for line in lines:
        line = line.rstrip()

        # T lines: transmission lines
        # T  ID  FROM  TO  circuits  R  X  B
        if line.startswith('T ') and not line.startswith('TEND'):
            parts = line.split()
            if len(parts) >= 8:
                from_bus = int(parts[2])
                to_bus = int(parts[3])
                r = float(parts[5])
                x = float(parts[6])
                b = float(parts[7]) if len(parts) > 7 else 0.0
                buses.add(from_bus)
                buses.add(to_bus)
                branches.append((from_bus, to_bus, r, x, b, 'line'))

        # X lines: transformers
        # X  ID  FROM  TO  type  Xpu  tap  ...
        elif line.startswith('X ') and not line.startswith('XEND'):
            parts = line.split()
            if len(parts) >= 7:
                from_bus = int(parts[2])
                to_bus = int(parts[3])
                x = float(parts[5])
                tap = float(parts[6])
                buses.add(from_bus)
                buses.add(to_bus)
                branches.append((from_bus, to_bus, 0.0, x, 0.0, 'transformer'))

        # N lines: node data
        # Generator: N  BUS  V  angle  Pg  Qg  ...
        # Load bus:  N  BUS        ...  Pl  Ql  ...
        elif line.startswith('N ') and not line.startswith('NEND'):
            parts = line.split()
            if len(parts) >= 2:
                bus = int(parts[1])
                buses.add(bus)
                # Generator buses (2001-2008, 3001-3022): have voltage and angle
                if len(parts) >= 5:
                    try:
                        v = float(parts[2])
                        angle = float(parts[3])
                        pg = float(parts[4])
                        if v > 0.5:  # has voltage setpoint = generator
                            generators[bus] = {'V': v, 'angle': angle, 'Pg': pg}
                    except (ValueError, IndexError):
                        pass
                # Load data in columns 5,6
                if len(parts) >= 7:
                    try:
                        pl = float(parts[5])
                        ql = float(parts[6])
                        if abs(pl) > 0.001 or abs(ql) > 0.001:
                            loads[bus] = {'Pl': pl, 'Ql': ql}
                    except (ValueError, IndexError):
                        pass

    # Sort buses
    buses = sorted(buses)

    # Create sequential bus mapping for easier handling
    bus_map = {b: i+1 for i, b in enumerate(buses)}

    print(f"IEEJ EAST 30-machine System")
    print(f"  Buses: {len(buses)}")
    print(f"  Branches (lines): {sum(1 for b in branches if b[5]=='line')}")
    print(f"  Branches (transformers): {sum(1 for b in branches if b[5]=='transformer')}")
    print(f"  Total branches: {len(branches)}")
    print(f"  Generators: {len(generators)}")
    print(f"  Load buses: {len(loads)}")

    # Classify buses by voltage level
    v500 = [b for b in buses if 3100 <= b <= 3199]
    v275 = [b for b in buses if 3200 <= b <= 3299]
    v154 = [b for b in buses if 3300 <= b <= 3399]
    v66  = [b for b in buses if 3400 <= b <= 3499]
    v500_area2 = [b for b in buses if 2100 <= b <= 2199]
    v275_area2 = [b for b in buses if 2200 <= b <= 2299]
    gen_buses = [b for b in buses if (2001 <= b <= 2099) or (3001 <= b <= 3099)]

    print(f"\n  Bus classification:")
    print(f"    500kV (Area3): {len(v500)} buses ({v500[0]}..{v500[-1] if v500 else 'N/A'})")
    print(f"    275kV (Area3): {len(v275)} buses")
    print(f"    154kV (Area3): {len(v154)} buses")
    print(f"    66kV  (Area3): {len(v66)} buses")
    print(f"    500kV (Area2): {len(v500_area2)} buses")
    print(f"    275kV (Area2): {len(v275_area2)} buses")
    print(f"    Generator:     {len(gen_buses)} buses")

    # Print adjacency as JS format
    print("\n// JavaScript branch data:")
    print("const BRANCHES = [")
    for (f, t, r, x, b, typ) in branches:
        print(f"  [{bus_map[f]}, {bus_map[t]}],  // {f}-{t} ({typ})")
    print("];")

    print(f"\n// Bus mapping (original -> sequential):")
    print("const BUS_MAP = {")
    for orig, seq in bus_map.items():
        is_gen = orig in generators
        is_load = orig in loads
        label = "GEN" if is_gen else ("LOAD" if is_load else "")
        print(f"  {seq}: {{orig: {orig}, label: '{label}'}},")
    print("};")

    return {
        'buses': buses,
        'branches': branches,
        'generators': generators,
        'loads': loads,
        'bus_map': bus_map,
    }


if __name__ == "__main__":
    data = parse_east30()
