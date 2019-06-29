from src.models.agent import Agent
from src.conf import CONFIG

class AgentSwarm:
    def __init__(self, N_agents):
        self.agents = []
        self.init_agents(N_agents)
        self.n_agent = N_agents
        self.Obs = []
        self.mapSize = (1,1)

        self.targets = []
        self.sensedTargets=[]

    # initialize agents and deploy them to Nest position
    def init_agents(self, N_agents):
        self.agents = []
        for i in range(N_agents):
            agent = Agent(CONFIG['Nest'])
            self.agents.append(agent)

        self.sensedTargets = [] # 발견된 타겟 목록도 여기서 초기화

    # return all agents' position in list
    def get_all_pos(self):
        locs = []
        for agent in self.agents:
            locs.append(agent.get_pos())
        return locs

    # 테스트용 : agents 의 숫자 리턴
    def count_num(self):
        return len(self.agents)

    # 테스트용 : agents 의 페로몬맵 크기 출력
    def print_size_pM(self):
        lst = []
        for agent in self.agents:
            lst.append(len(agent.pheMap))
        print(lst)

    # 테스트용 : agent의 이동 경로 출력
    def print_path(self, num):
        print(self.agents[num].history)

    # 테스트용 : agent 의 mb 출력
    def print_mb(self, num):
        print(self.agents[num].movable_blocks)

    def get_all_agents(self):
        return self.agents

    # 장애물 데이터를 받아올 때 사용, 자체변수에 저장
    def set_Obs(self, Obs):
        self.Obs = Obs

    # 맵 데이터(장애물, 맵사이즈) 받아올 때 사용, 초기 한번만 실행
    def set_map_info(self,Obs,mapSize, targets):
        self.Obs = Obs
        self.mapSize = mapSize
        self.targets = targets

    # 전체 페로몬 맵의 정보를 받아서 각 agent의 pheMap을 업데이트
    def update_phe_info(self, pheMap):
        for agent in self.agents:
            agent.clear_phe_map()
            for key in agent.movable_blocks:
                agent.pheMap[key] = pheMap[key]

    # 단순히 movable block 을 계산하기 위해 사용
    def cal_movable_blocks(self):
        for agent in self.agents:
            agent.cal_movable_blocks(self.Obs, self.mapSize)

    # 3개의 무빙 모델 : 1.이동가능한블록계산 2.3가지방법중 하나로 이동 결정 3.이동
    def cal_and_move_phe(self):
        for agent in self.agents:
            agent.cal_movable_blocks(self.Obs, self.mapSize)
            next_pos = agent.cal_next_pos_phe()
            agent.move_to(next_pos)

    def cal_and_move_rand(self):
        for agent in self.agents:
            agent.cal_movable_blocks(self.Obs, self.mapSize)
            next_pos = agent.cal_next_pos_rand()
            agent.move_to(next_pos)

    def cal_and_move_flex(self):
        for agent in self.agents:
            agent.cal_movable_blocks(self.Obs, self.mapSize)
            next_pos = agent.cal_next_pos_flex(self.n_agent)
            agent.move_to(next_pos)

    # Calculate number of neigh UAVs in Communicable Range and assign in to each UAVs
    def cal_num_in_CR(self):
        num_in_CR = [0 for i in range(self.n_agent)]
        locs = self.get_all_pos()

        for i in range(len(locs)):
            for j in range(1, len(locs)-i):
                if (locs[i][0]-3 <= locs[i+j][0] and locs[i+j][0] <= locs[i][0]+3):
                    if (locs[i][1]-3 <= locs[i+j][1] and locs[i+j][1] <= locs[i][1]+3):
                        num_in_CR[i] += 1
                        num_in_CR[i+j] += 1

        for i, agent in enumerate(self.agents):
            agent.numInCR = num_in_CR[i]

    # 각 에이전트의 SR에 들어온 타겟을 체크하여 새로운 target이 발견되면 전체 swarm 의 sensedTarget에 추가
    def sense_target(self):
        sensedTargets = []
        for agent in self.agents:
            sensed = agent.sense_target(self.targets)
            sensedTargets.extend(sensed)

        sensedTargetsSet = set(sensedTargets)
        sensedTargets = list(sensedTargetsSet)

        for target in sensedTargets:
            if target in self.sensedTargets:
                pass
            else:
                self.sensedTargets.append(target)

    # Metric 을 위해서, 발견된 타겟의 숫자를 리턴
    def count_sensed_target(self):
        return len(self.sensedTargets)
