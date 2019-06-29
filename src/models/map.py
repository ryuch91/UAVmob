from src.conf import CONFIG
from numpy import random
import copy

class Map:
    def __init__(self, map_size, scene, N_targets):
        self.sizeX = map_size[0]
        self.sizeY = map_size[1]
        self.mapSize = map_size
        self.scene = scene
        self.Obs = self.init_obs(scene)
        self.PheMap = self.init_phe()
        self.initPheMap = self.init_phe() # 초기 pheMap을 재활용하기 위한 변수
        self.Targets = self.init_target(N_targets)
        self.Cells = self.init_cells()
        self.nT = N_targets

    # 시나리오에 따른 장애물 초기화, 1: no obs, 2: many small obs, 3: few huge obs
    def init_obs(self, scene):
        Obs = []
        if scene == 1:
            pass
        elif scene == 2:
            # 5 vertical obs
            for i in range(5):
                start_x = random.randint(2,self.sizeX)
                start_y = random.randint(2,self.sizeY-5)
                size = random.randint(1,5)
                for j in range(size):
                    Obs.append((start_x,start_y+j))
            # 5 horizontal obs
            for i in range(5):
                start_x = random.randint(2,self.sizeX-5)
                start_y = random.randint(2,self.sizeY)
                size = random.randint(1,5)
                for j in range(size):
                    Obs.append((start_x+j,start_y))
        elif scene == 3:
            # 5 Big obs
            for i in range(5):
                start_x = random.randint(2,self.sizeX-7)
                start_y = random.randint(2,self.sizeY-7)
                sizeX = random.randint(3,7)
                sizeY = random.randint(3,7)
                Obs.extend([(j,k) for j in range(start_x, start_x+sizeX) for k in range(start_y, start_y+sizeY)])
        else:
            pass

        # Remove duplicated coordinate
        Obs_set = set(Obs)
        Obs = list(Obs_set)
        return Obs

    # Dict 형태의 PheMap을 0(MIN_PHE)으로 초기화, Obs 는 -1로 초기화
    def init_phe(self):
        key = [(i,j) for i in range(self.sizeX) for j in range(self.sizeY)]
        data = {i: CONFIG['MIN_PHE'] for i in key}
        for i in self.Obs:
            data[i] = CONFIG['OBS_PHE']
        return data

    # 초기의 페로몬맵을 저장해두었다가 재사용
    def reboot_phe(self):
        self.PheMap = copy.deepcopy(self.initPheMap)

    # 초기의 움직일 수 있는 normal cell 들의 좌표를 저장(metric1 에 사용)
    def init_cells(self):
        cells = [(i,j) for i in range(self.sizeX) for j in range(self.sizeY)]
        for cell in self.Obs:
            if cell in cells:
                cells.remove(cell)

        return cells

    # 테스트용 : pheMap 콘솔에 출력
    def print_pheMap(self):
        for i in range(self.sizeX):
            for j in range(self.sizeY):
                key = (i,j)
                print(self.initPheMap[key],end=' ')
            print('\n')

    # Create targets
    def init_target(self, N_targets):
        targets = []
        for i in range(N_targets):
            while True:
                x = random.randint(0,self.sizeX)
                y = random.randint(0,self.sizeY)
                pos = (x,y)
                if pos in self.Obs or pos in targets:
                    continue
                targets.append(pos)
                break
        return targets

    # 페로몬맵의 업데이트를 진행 1.전체 맵의 증발(decay) 2.새로운 pheromone 분출
    def update_phe(self, agentsLocs):
        self.decay_phe()
        self.spread_phe(agentsLocs)

    # UAV 위치에 페로몬 분출
    def spread_phe(self, agents_locs):
        for key in agents_locs:
            self.PheMap[key] = CONFIG['MAX_PHE']

    # 전체 PheMap 의 decay 진행
    def decay_phe(self):
        if self.PheMap:
            for key in self.PheMap.keys():
                self.PheMap[key] -= self.PheMap[key] * CONFIG['DecayConst']

    # Print map to txt file
    def print_map(self):
        file = open("map.txt",'w')
        for j in range(self.sizeY):
            line = ''
            for i in range(self.sizeX):
                pos = (i,self.sizeY-j-1)
                if pos in self.Targets:
                    line = line + ('* ')
                elif pos in self.Obs:
                    line = line + ('X ')
                else:
                    line = line + ('O ')
            line = line + ('\n')
            file.write(line)

        file.close()