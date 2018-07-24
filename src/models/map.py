from src.conf import CONFIG

class Map:
    def __init__(self, map_size):
        self.size = map_size
        self.PheMap = self.init_phe()

    # Create Pheromone map data structure and initialize as 0 (which is MIN_PHE)
    def init_phe(self):
        key = [(i,j) for i in range(self.size) for j in range(self.size)]
        data = {i: CONFIG['MIN_PHE'] for i in key}
        return data

    def phe_decay(self):
        if self.PheMap:
            for key in self.PheMap.keys():
                self.PheMap[key] -= self.PheMap[key]*CONFIG['DecayConst']

    # Get agents' position as list and do update phero info (e.g. [(1,3), (5,6), ... ])
    def update_phe(self, agents_locs):
        for key in agents_locs:
            self.PheMap[key] = CONFIG['MAX_PHE']