def test_1():
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