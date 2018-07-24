import numpy as np
from numpy import ndarray

class Agent:
    def __init__(self, start_point):
        self.position = start_point
        self.phe_map = {}
        self.history = []

    def get_pos(self):
        x = self.position[0]
        y = self.position[1]
        return x, y

    def set_pos(self, x, y):
        self.position[0] = x
        self.position[1] = y

    def move_to(self, new_pos):
        self.history.append(self.position)
        self.position = (new_pos[0], new_pos[1])

    def clear_phe_map(self):
        self.phe_map = {}

    def cal_next_pos(self):
        pos_list = []
        phe_list = []
        for pos, phe in self.phe_map.items():
            pos_list.append(pos)
            phe_list.append(phe)
        phe_array = np.array(phe_list)
        rev_phe_array = (phe_array * (-1)) + 1
        if np.sum(phe_array) == 0:
            idx = np.random.choice(range(len(phe_array)))
            new_pos = pos_list[idx]
        else:
            prob_array = np.array(rev_phe_array)/np.sum(rev_phe_array)
            # idx = np.random.choice(len(rev_phe_array), prob_array)
            idx = np.random.choice(len(rev_phe_array), p=prob_array)
            new_pos = pos_list[idx]
        return new_pos
