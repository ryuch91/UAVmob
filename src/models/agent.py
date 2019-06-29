import numpy as np
from numpy import ndarray

from src.conf import CONFIG

class Agent:
    def __init__(self, start_point):
        self.position = start_point
        self.movable_blocks = []
        self.pheMap = {}
        self.history = []
        self.numInCR = 0
        self.prev_mov = (0,0)


    def get_pos(self):
        x = self.position[0]
        y = self.position[1]
        return x, y

    def set_pos(self, x, y):
        self.position[0] = x
        self.position[1] = y

    # Obs: 장애물 좌표 list, mapSize : 전체 맵크기 (x,y)
    def cal_movable_blocks(self, Obs, mapSize):
        # 현재 위치 기준 8방향으로의 block 생성
        x= self.position[0]
        y= self.position[1]
        blocks = []
        blocks += [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
        blocks += [(x - 1, y), (x + 1, y)]
        blocks += [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]

        # 맵 밖으로 나가는 경우를 제외 (앞에서부터 지우면 index가 꼬여서 뒤집어서 실행)
        to_remove = [i for i, key in enumerate(blocks) if (-1 in key) or (mapSize[0] in key) or (mapSize[1] in key)]
        for idx in reversed(to_remove):
            del blocks[idx]

        # 장애물이 있는 경우를 제외
        to_remove = [i for i, key in enumerate(blocks) if key in Obs]
        for idx in reversed(to_remove):
            del blocks[idx]

        # set 을 통해서 블락을 정렬
        blocks_set = set(blocks)
        blocks = list(blocks_set)

        self.movable_blocks = blocks


    # 움직임을 저장하고, 새 포지션으로 이동
    def move_to(self, new_pos):
        self.history.append(self.position)
        delta_x = new_pos[0] - self.position[0]
        delta_y = new_pos[1] - self.position[1]
        self.prev_mov = (delta_x, delta_y)
        self.position = (new_pos[0], new_pos[1])

    def clear_phe_map(self):
        self.pheMap = {}

    def cal_next_pos_phe(self):
        pos_list = []
        phe_list = []
        for pos, phe in self.pheMap.items():
            pos_list.append(pos)
            phe_list.append(phe)
        phe_array = np.array(phe_list)
        rev_phe_array = (phe_array * (-1)) + 1

        # 주변이 모두 0이거나 1인경우 오류를 방지하고, 랜덤으로 방향 결정
        if (np.sum(phe_array) == 0) or (np.sum(rev_phe_array) == 0):
            idx = np.random.choice(range(len(phe_array)))
            new_pos = pos_list[idx]
        else:
            prob_array = np.array(rev_phe_array)/np.sum(rev_phe_array)
            # idx = np.random.choice(len(rev_phe_array), prob_array)
            idx = np.random.choice(len(rev_phe_array), p=prob_array)
            new_pos = pos_list[idx]
        return new_pos

    # 다음 포지션을 랜덤으로 결정
    def cal_next_pos_rand(self):
        #movable_array = np.array(self.movable_blocks)
        idx = np.random.choice(range(len(self.movable_blocks)))
        new_pos = self.movable_blocks[idx]
        return new_pos


    def cal_next_pos_flex(self, nUAV):
        flex = self.numInCR/float(nUAV)
        if flex < CONFIG['Flex_Thr']:
            new_pos = self.cal_next_pos_phe()
        else:
            new_pos = (self.position[0] + self.prev_mov[0], self.position[1] + self.prev_mov[1])
            if new_pos not in self.movable_blocks:
                new_pos = self.cal_next_pos_rand()
        return new_pos

    # Sensing Range 안의 target을 검출하여 좌표 리스트를 반환
    def sense_target(self, targets):
        sensedTargets = []
        if self.position in targets:
            sensedTargets.append(self.position)
        for block in self.movable_blocks:
            if block in targets:
                sensedTargets.append(block)
        return sensedTargets
