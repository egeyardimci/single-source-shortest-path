def test_1():
    # Define stations and example graph for the tourist problem
    stations = [("Harem", "Istanbul"), ("Bostanci","Istanbul"), ("Merkez","Bursa"), ("YHT","Eskisehir"), ("Yeni","Eskisehir")]
    idx = {f"{name}-{city}": i for i, (name, city) in enumerate(stations)}

    # Build directed edge list (u, v, time)
    edges = []
    # Intra-city transfers
    edges += [
        (idx["Harem-Istanbul"],    idx["Bostanci-Istanbul"], 30),
        (idx["Bostanci-Istanbul"], idx["Harem-Istanbul"],   30),
        (idx["YHT-Eskisehir"],      idx["Yeni-Eskisehir"],     10),
        (idx["Yeni-Eskisehir"],     idx["YHT-Eskisehir"],      10),
    ]
    # Inter-city travel times (two-way)
    edges += [
        (idx["Harem-Istanbul"],    idx["Merkez-Bursa"],  100),
        (idx["Merkez-Bursa"],   idx["Harem-Istanbul"],   100),
        (idx["Bostanci-Istanbul"], idx["YHT-Eskisehir"],     180),
        (idx["YHT-Eskisehir"],      idx["Bostanci-Istanbul"],180),
        (idx["Merkez-Bursa"],   idx["Yeni-Eskisehir"],    120),
        (idx["Yeni-Eskisehir"],     idx["Merkez-Bursa"],  120),
    ]
    source = "Harem-Istanbul"
    
    return stations, edges, idx, source

def test_2():
    # Simple linear graph: A -> B -> C (each in its own city)
    stations = [
        ('st1', 'A'), ('st2', 'B'), ('st3', 'C')
    ]
    idx = {f"{name}-{city}": i for i, (name, city) in enumerate(stations)}
    edges = [
        (idx['st1-A'], idx['st2-B'], 5),
        (idx['st2-B'], idx['st3-C'], 7)
    ]
    source = 'st1-A'
    return stations, edges, idx, source

def test_3():
    # Hub-and-spoke network
    stations = [
        ('st1', 'H'), ('st2', 'A'), ('st3', 'B'), ('st4', 'C'), ('st5', 'D')
    ]
    idx = {f"{name}-{city}": i for i, (name, city) in enumerate(stations)}
    edges = []
    # Hub st1 connected to all
    for i in range(2, 6):
        edges.append((idx['st1-H'], idx[f'st{i}-{stations[i-1][1]}'], i * 10))
        edges.append((idx[f'st{i}-{stations[i-1][1]}'], idx['st1-H'], i * 10))
    source = 'st1-H'
    return stations, edges, idx, source

def test_4():
    # Disconnected graph: st1 -> st2, st3 and st4 isolated
    stations = [
        ('st1', 'A'), ('st2', 'B'), ('st3', 'C'), ('st4', 'D')
    ]
    idx = {f"{name}-{city}": i for i, (name, city) in enumerate(stations)}
    edges = [
        (idx['st1-A'], idx['st2-B'], 3)
    ]
    source = 'st1-A'
    return stations, edges, idx, source

def test_5():
    # Zero-weight edges and self-loops
    stations = [
        ('st1', 'A'), ('st2', 'B'), ('st3', 'C')
    ]
    idx = {f"{name}-{city}": i for i, (name, city) in enumerate(stations)}
    edges = [
        (idx['st1-A'], idx['st1-A'], 0),
        (idx['st1-A'], idx['st2-B'], 0),
        (idx['st2-B'], idx['st3-C'], 5)
    ]
    source = 'st1-A'
    return stations, edges, idx, source

def test_6():
    # Two equal-cost paths: A->B->D and A->C->D
    stations = [
        ('st1', 'A'), ('st2', 'B'), ('st3', 'C'), ('st4', 'D')
    ]
    idx = {f"{name}-{city}": i for i, (name, city) in enumerate(stations)}
    edges = [
        (idx['st1-A'], idx['st2-B'], 4),
        (idx['st2-B'], idx['st4-D'], 4),
        (idx['st1-A'], idx['st3-C'], 3),
        (idx['st3-C'], idx['st4-D'], 5)
    ]
    source = 'st1-A'
    return stations, edges, idx, source

def test_7():
    # Complete directed graph of four nodes
    stations = [
        ('st1', 'A'), ('st2', 'B'), ('st3', 'C'), ('st4', 'D')
    ]
    idx = {f"{name}-{city}": i for i, (name, city) in enumerate(stations)}
    edges = [
        (idx['st1-A'], idx['st2-B'], 5), (idx['st1-A'], idx['st3-C'], 9), (idx['st1-A'], idx['st4-D'], 2),
        (idx['st2-B'], idx['st1-A'], 6), (idx['st2-B'], idx['st3-C'], 1), (idx['st2-B'], idx['st4-D'], 6),
        (idx['st3-C'], idx['st1-A'], 3), (idx['st3-C'], idx['st2-B'], 4), (idx['st3-C'], idx['st4-D'], 4),
        (idx['st4-D'], idx['st1-A'], 7), (idx['st4-D'], idx['st2-B'], 8), (idx['st4-D'], idx['st3-C'], 3)
    ]
    source = 'st1-A'
    return stations, edges, idx, source

def test_8():
    # Single-node graph
    stations = [
        ('st1', 'A')
    ]
    idx = {f"{name}-{city}": i for i, (name, city) in enumerate(stations)}
    edges = []
    source = 'st1-A'
    return stations, edges, idx, source

def test_9():
    # Fast intra-city hops and multiple inter-city options so optimal path is:
    # st1-A → st2-A → st3-B → st4-B → st5-C
    stations = [
        ('st1', 'A'), ('st2', 'A'),
        ('st3', 'B'), ('st4', 'B'),
        ('st5', 'C'), ('st6', 'C'),
    ]
    idx = { f"{name}-{city}": i for i,(name,city) in enumerate(stations) }

    edges = []
    # Intra-city transfers (very fast)
    edges += [
        (idx['st1-A'], idx['st2-A'], 1),
        (idx['st2-A'], idx['st1-A'], 1),
        (idx['st3-B'], idx['st4-B'], 1),
        (idx['st4-B'], idx['st3-B'], 1),
        (idx['st5-C'], idx['st6-C'], 1),
        (idx['st6-C'], idx['st5-C'], 1),
    ]

    # Inter-city transfers:
    edges += [
        # Preferred A→B via st2-A → st3-B (5)  
        (idx['st2-A'], idx['st3-B'], 5),
        (idx['st3-B'], idx['st2-A'], 5),
        # Slower alternative A→B directly  
        (idx['st1-A'], idx['st3-B'], 20),
        (idx['st3-B'], idx['st1-A'], 20),
        # Another A→B option via st2-A → st4-B  
        (idx['st2-A'], idx['st4-B'], 15),
        (idx['st4-B'], idx['st2-A'], 15),

        # Preferred B→C via st4-B → st5-C (5)  
        (idx['st4-B'], idx['st5-C'], 5),
        (idx['st5-C'], idx['st4-B'], 5),
        
        # Slower alternatives B→C
        (idx['st3-B'], idx['st5-C'], 20),
        (idx['st5-C'], idx['st3-B'], 20),
        (idx['st4-B'], idx['st6-C'], 15),
        (idx['st6-C'], idx['st4-B'], 15),

        # Direct A→C (very slow)
        (idx['st1-A'], idx['st5-C'], 50),
        (idx['st5-C'], idx['st1-A'], 50),
    ]

    source = 'st1-A'
    return stations, edges, idx, source

tests = [test_1,test_2,test_3,test_4,test_5,test_6,test_7,test_8,test_9]