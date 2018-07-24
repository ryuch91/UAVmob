import matplotlib.pyplot as plt
import matplotlib.colors as colors
from numpy import array, mgrid, zeros, linspace
from numpy.random import choice

class ACO:
    Start = (5, 4)     # 개미굴의 위치
    Feed = (25, 10)    # 먹이의 위치
    Edge = [(0, 30),   # 개미가 움직일 수 있는 범위
            (0, 15)]   # x축 범위와 y축 범위
    Step = 80          # 먹이를 찾은 이후의 반복횟수
    PheFeed = 0.5        # 한번에 개미가 뿌릴 페로몬 양
    PheDecay = 0.5     # 페로몬 감쇠상수
    AntPop = 10         # 한번에 풀어놓을 개미의 수
    Pherom = {}        # 페로몬 정보
    def __init__(self):
        # 페로몬 초기화
        self.Pherom = self._init_pherom()

    def _init_pherom(self):
        # 페로몬 초기화 함수
        # 키 조합 생성
        key = [(i,j) for i in self.range_x() for j in self.range_y()]
        # 1로 초기화
        data = {i: 1 for i in key}
        return data

    def range_x(self):
        # x 범위 출력
        start, stop = self.Edge[0]
        return range(start, stop+1)

    def range_y(self):
        # y 범위 출력
        start, stop = self.Edge[1]
        return range(start, stop+1)

    def pherom_decay(self):
        for key in self.Pherom.keys():
            self.Pherom[key] -= self.Pherom[key]*self.PheDecay

    def next_step(self, mode="loop"):
        pheroms = {}
        antData = []
        antGoal = []
        ready = False
        for a in [ant(self) for i in range(self.AntPop)]:
            if a.is_goal():
                antGoal.append(a)
                ready = True
            antData.append(a)
        for a in antGoal:
            pheroms.update({i: 1 for i in a.Position})
        for key in pheroms.keys():
            self.Pherom[key] += 1
        self.pherom_decay()
        if mode == "pre":
            return ready, antData
        else:
            return antData

    def run(self):
        antData = []
        ready = False
        Counter = 0
        while not ready:
            Counter += 1
            print("\rpre step:", Counter, end="")
            ready, partData = self.next_step("pre")
            antData.append(partData)
            if Counter > self.Step*2:
                # 지정한 스탭의 두배보다 더 해메고 있으면 스탭 전체를 초기화
                Counter = 0
                antData.clear()
        print()
        for i in range(self.Step):
            print("\rrun step:", i+1, '/', self.Step, end="")
            partData = self.next_step()
            antData.append(partData)
        print()
        return antData



class ant:
    LoopEnd = 200  # 강제로 멈추는 지점
    def __init__(self, system):
        self.system = system
        self.Position = [self.system.Start]
        self.ant_move()

    def ant_move(self):
        # 개미 이동 함수
        # 경로는 self.Position에 저장
        LoopCounter = 0
        while LoopCounter < self.LoopEnd:
            LoopCounter += 1
            aroundBlock, aroundProb = self.get_around_blocks_info()
            ixBlock = choice(range(len(aroundBlock)), p=aroundProb)
            newPosition = aroundBlock[ixBlock]
            self.Position.append(newPosition)
            if self.is_goal() or self.is_out():
                break

    def is_out(self):
        # 맵 바깥으로 탈출했는지 판단
        nowPosition = self.Position[-1]
        isXMin = nowPosition[0] <= self.system.Edge[0][0]
        isXMax = nowPosition[0] >= self.system.Edge[0][1]
        isYMin = nowPosition[1] <= self.system.Edge[1][0]
        isYMax = nowPosition[1] >= self.system.Edge[1][1]
        return isXMin or isXMax or isYMin or isYMax

    def is_goal(self):
        # 먹이에 도달했는지 판단
        nowPosition = self.Position[-1]
        isX = nowPosition[0] == self.system.Feed[0]
        isY = nowPosition[1] == self.system.Feed[1]
        return isX and isY

    def get_around_blocks_info(self):
        x, y = self.Position[-1]
        # 주변 블록 초기화
        blocks =  [(x-1, y+1), (x, y+1), (x+1, y+1)]
        blocks += [(x-1, y), (x+1, y)]
        blocks += [(x-1, y-1), (x, y-1), (x+1, y-1)]
        # 이전 위치 제외
        if len(self.Position) >= 2:
            prePosition = self.Position[-2]
            blocks.pop(blocks.index(prePosition))
        # 페로몬 정보 획득
        pheroms = []
        for key in blocks:
            if key in self.system.Pherom.keys():
                pheroms.append(self.system.Pherom[key])
            else:
                pheroms.append(0)
        # 페로몬 정보를 확률로 변환
        probs = array(pheroms)/sum(pheroms)
        return blocks, probs

    def get_xy(self):
        # 경로를 x, y 요소로 출력
        x = [i[0] for i in self.Position]
        y = [i[1] for i in self.Position]
        return x, y


# 프로그램 초기화
system = ACO()
data = system.run()

# 그림의 크기를 ACO 시스템과 연동
figsize = [(system.Edge[0][1]-system.Edge[0][0])+1]
figsize += [(system.Edge[1][1]-system.Edge[1][0])+1]

# 컬러맵 및 칸투어 요소 초기화
cmapL = plt.get_cmap('winter')  # 개미 경로 컬러맵
cmapP = plt.get_cmap('afmhot')  # 페로몬 컬러맵
x, y = mgrid[system.range_x(), system.range_y()]
z = zeros(figsize)
for i, _x in enumerate(system.range_x()):
    for j, _y in enumerate(system.range_y()):
        # 페로몬량 받아오기
        z[i][j] += system.Pherom[(_x, _y)]

# 서브플롯 생성
fig, ax = plt.subplots(subplot_kw={'xticks': [], 'yticks': []},
                       facecolor=cmapP(0),
                       figsize=array(figsize)/4)
# 페로몬 칸투어 맵 생성
im = plt.contourf(x, y, z, cmap=cmapP)
# 개미 경로 출력
for ix, d, c in zip(range(len(data)), data, linspace(0, 1, len(data))):
    print("\rdrawing:", ix+1, "/", len(data), end="")
    for a in d:
        ax.plot(*a.get_xy(), color=(*cmapL(c)[:3], 0.05))
print()
# 출발 지점과 끝 지점 표시
ax.plot(*system.Feed, ".k", ms=10)
ax.plot(*system.Start, ".k", ms=10)
# 그림 저장
fig.tight_layout()
fig.savefig('ACO-test-fig001.png', bbox_inches='tight',
            facecolor=fig.get_facecolor())