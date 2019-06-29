import matplotlib.pyplot as plt
import matplotlib.colors as clrs
from matplotlib import animation
from numpy import array, mgrid, zeros, linspace
from numpy.random import choice
import csv
from math import sqrt

from src.models import agent
import src.conf as cfg
from src.models.map import Map
from src.models.agent_swarm import AgentSwarm
from src.conf import CONFIG

class Simulation:
    def __init__(self, map):
        self.map = map
        self.nRepeat = CONFIG['N_Repeat']
        self.nStep = CONFIG['N_Step']
        self.nUAVs = CONFIG['N_Agents']

        self.figSize = (self.map.sizeX, self.map.sizeY)

        self.nlistST = [] # 스텝별 센싱된 타겟 개수를 리스트로 저장
        self.nlistlistST = [] # 타겟 개수 리스트의 리스트

        self.leftCells = [] # 스텝별 스캔안된 셀들을 저장, 시뮬 직전에 초기화해야함
        self.nlistLCs = [] # leftCells 개수를 리스트로 저장
        self.nlistlistLCs = [] #leftCells 개수 리스트의 리스트

        self.listFN = [] # Fairness 저장을 위한 리스트
        self.scanCounter = {} # 각 셀의 scan 횟수를 저장하는 dict

    # nUAV x 반복횟수 만큼 시뮬 진행. 각 시뮬은 step 수 만큼 진행
    def run(self):

        self.init_scan_counter()

        # 3개의 UAV 개수에 대해 실험 진행
        for i in range(len(self.nUAVs)):
            # UAV 생성 및 초기화
            nUAVs = self.nUAVs[i]
            swarm = AgentSwarm(nUAVs)
            swarm.set_map_info(self.map.Obs, self.map.mapSize, self.map.Targets)

            for j in range(self.nRepeat):

                # 필요한 메트릭 설정(e.g. init unscanned cell)
                self.pre_init_metric()

                #각 시뮬 순서 : 1.이동가능방향계산/2.페로몬정보전달/3.무빙-전체페로몬맵업뎃-전달 반복/4.페로맵리셋/5.스웜리셋
                swarm.cal_movable_blocks()
                swarm.update_phe_info(self.map.PheMap)
                for k in range(self.nStep):

                    swarm.cal_and_move_rand()
                    self.map.update_phe(swarm.get_all_pos())
                    swarm.update_phe_info(self.map.PheMap)

                    # Metric 측정 및 값 기록
                    self.cal_left_cells(swarm)
                    self.nlistLCs.append(len(self.leftCells))
                    swarm.sense_target()
                    self.nlistST.append(swarm.count_sensed_target())
                    self.update_scan_counter(swarm)

                self.map.reboot_phe()
                swarm.init_agents(nUAVs)

                # Metric 측정된 값들을 하나의 리스트에 기록
                self.nlistlistST.append(self.nlistST)
                self.nlistlistLCs.append(self.nlistLCs)
                self.listFN.append(self.cal_fairness())
                self.init_metric() # 메트릭 관련 변수들(새 repeat 마다 초기화되어야하는것들) 초기화

                print(str(i) + '-' + str(j) + '-rand' + ' finished!')  # 진행사항을 알기위한 콘솔 출력

            self.write_csv_metric0(self.nlistlistST, self.map.mapSize, self.map.scene, self.map.nT, nUAVs, 'Rand')
            self.write_csv_metric1(self.nlistlistLCs, self.map.mapSize, self.map.scene, self.map.nT, nUAVs, 'Rand')
            self.write_csv_metric2(self.listFN, self.map.mapSize, self.map.scene, self.map.nT, nUAVs, 'Rand')
            self.init_upper_metric() # 전체 step x repeat 끝날때마다 초기화되어야 하는 것들 초기화

            for j in range(self.nRepeat):

                self.pre_init_metric()

                swarm.cal_movable_blocks()
                swarm.update_phe_info(self.map.PheMap)
                for k in range(self.nStep):
                    swarm.cal_and_move_phe()
                    self.map.update_phe(swarm.get_all_pos())
                    swarm.update_phe_info(self.map.PheMap)

                    self.cal_left_cells(swarm)
                    self.nlistLCs.append(len(self.leftCells))
                    swarm.sense_target()
                    self.nlistST.append(swarm.count_sensed_target())
                    self.update_scan_counter(swarm)

                self.map.reboot_phe()
                swarm.init_agents(nUAVs)

                self.nlistlistST.append(self.nlistST)
                self.nlistlistLCs.append(self.nlistLCs)
                self.listFN.append(self.cal_fairness())
                self.init_metric()

                print(str(i) + '-' + str(j) + '-phe' + ' finished!')  # 진행사항을 알기위한 콘솔 출력

            self.write_csv_metric0(self.nlistlistST, self.map.mapSize, self.map.scene, self.map.nT, nUAVs, 'Phe')
            self.write_csv_metric1(self.nlistlistLCs, self.map.mapSize, self.map.scene, self.map.nT, nUAVs, 'Phe')
            self.write_csv_metric2(self.listFN, self.map.mapSize, self.map.scene, self.map.nT, nUAVs, 'Phe')
            self.init_upper_metric()

            for j in range(self.nRepeat):

                self.pre_init_metric()

                swarm.cal_movable_blocks()
                swarm.update_phe_info(self.map.PheMap)
                for k in range(self.nStep):
                    swarm.cal_and_move_flex()
                    self.map.update_phe(swarm.get_all_pos())
                    swarm.update_phe_info(self.map.PheMap)

                    self.cal_left_cells(swarm)
                    self.nlistLCs.append(len(self.leftCells))
                    swarm.sense_target()
                    self.nlistST.append(swarm.count_sensed_target())
                    self.update_scan_counter(swarm)

                self.map.reboot_phe()
                swarm.init_agents(nUAVs)

                self.nlistlistST.append(self.nlistST)
                self.nlistlistLCs.append(self.nlistLCs)
                self.listFN.append(self.cal_fairness())
                self.init_metric()

                print(str(i)+'-'+str(j)+'-flex'+' finished!') # 진행사항을 알기위한 콘솔 출력

            self.write_csv_metric0(self.nlistlistST, self.map.mapSize, self.map.scene, self.map.nT, nUAVs, 'Flex')
            self.write_csv_metric1(self.nlistlistLCs, self.map.mapSize, self.map.scene, self.map.nT, nUAVs, 'Flex')
            self.write_csv_metric2(self.listFN, self.map.mapSize, self.map.scene, self.map.nT, nUAVs, 'Flex')
            self.init_upper_metric()

    def draw(self,name, i_n,j_repeat,k_step):
        cmapA = plt.get_cmap('winter')
        cmapP = plt.get_cmap('afmhot')
        x, y = mgrid[range(self.figSize[0]), range(self.figSize[1])]
        z = zeros(self.figSize)

        for i, _x in enumerate(range(self.figSize[0])):
            for j, _y in enumerate(range(self.figSize[1])):
                z[i][j] += map.PheMap[(_x, _y)]

        fig, ax = plt.subplots(subplot_kw={'xticks':[], 'yticks':[]},facecolor=cmapP(0),figsize=array(self.figSize)/4)

        im = plt.contourf(x,y,z,cmap=cmapP)


        fig.tight_layout()
        fileName = 'Test_'+name+'+'+str(i_n)+'-UAV+'+str(j_repeat)+'-repeat+'+str(k_step)+'-step.png'
        fig.savefig(fileName,bbox_inches='tight', facecolor=fig.get_facecolor())

        plt.close('all')

    # 각 Repeat 마다 사전에 초기화해야 되는 것들
    def pre_init_metric(self):
        LCs = []
        for cell in self.map.Cells:
            LCs.append(cell)
        self.leftCells = LCs
        
        # scanCounter value들을 모두 0으로 설정
        for key, val in self.scanCounter.items():
            self.scanCounter[key] = 0

    # 시뮬 생성시 스캔카운터 초기화(여기서 map.cell 통해 key를 넣어주고 이후로는 값만 초기화)
    def init_scan_counter(self):
        for key in self.map.Cells:
            self.scanCounter[key] = 0

    def init_metric(self):
        self.nlistST = []
        self.nlistLCs = []

    def init_upper_metric(self):
        self.nlistST = []
        self.nlistlistST = []

        self.nlistLCs = []
        self.nlistlistLCs = []

        self.listFN = []

    def cal_left_cells(self,swarm):
        for agent in swarm.agents:
            if agent.position in self.leftCells:
                self.leftCells.remove(agent.position)
            for block in agent.movable_blocks:
                if block in self.leftCells:
                    self.leftCells.remove(block)

    # Swarm을 통해 scanCounter를 업데이트
    def update_scan_counter(self, swarm):
        for agent in swarm.agents:
            self.scanCounter[agent.position] += 1
            for block in agent.movable_blocks:
                self.scanCounter[block] += 1

    # scanCounter로부터 fairness 를 계산해서 return
    def cal_fairness(self):
        FN = 0.0
        sum = 0
        sqSum = 0
        vals = []
        for key, val in self.scanCounter.items():
            sum += val
            vals.append(val)
        size = len(self.scanCounter)
        if size != 0:
            mean = sum/size
        else:
            mean = 0.0
            return 0.0

        for val in vals:
            sqSum += (mean - val)**2

        FN = sqrt((float(sqSum)/size))

        return FN

    # Met0: 타겟 수 측정을 위한 csv 파일에 작성 (data는 list of list)
    def write_csv_metric0(self, data, mapSize, scene, nT, nU, method):
        new_data = list(zip(*data))

        filename = 'Map'+str(mapSize[0])+'_Scene'+str(scene)+'_T'+str(nT)+'_U'+str(nU)+'_'+method+'_Met0.csv'
        f = open(filename, 'w', newline='')
        wr = csv.writer(f)

        for row in new_data:
            wr.writerow(row)

        f.close()

    # Met1: Unscanned cell 수 측정을 위한 csv 파일에 작성 (data 는 list of list)
    def write_csv_metric1(self, data, mapSize, scene, nT, nU, method):
        new_data = list(zip(*data))

        filename = 'Map'+str(mapSize[0])+'_Scene'+str(scene)+'_T'+str(nT)+'_U'+str(nU)+'_'+method+'_Met1.csv'
        f = open(filename, 'w', newline='')
        wr = csv.writer(f)

        for row in new_data:
            wr.writerow(row)

        f.close()

    # Met2: Scan Fairness 측정을 위한 csv 파일에 작성 (data 는 list)
    def write_csv_metric2(self, data, mapSize, scene, nT, nU, method):
        filename='Map'+str(mapSize[0])+'_Scene' + str(scene) + '_T' +str(nT)+'_U'+str(nU)+'_' + method + '_Met2.csv'
        f = open(filename, 'w',newline='')
        wr = csv.writer(f)

        for fn in data:
            tmp = [fn]
            wr.writerow(tmp)

        f.close()

if __name__ == '__main__':
    # Generate Map
    map = Map(CONFIG['MapSize'],CONFIG['Scene'],CONFIG['N_Targets'])
    map.print_map()
    new_sim = Simulation(map)
    new_sim.run()

    #################################### Draw the pheromone snapshot ######################
    ## setup the figure, axis
    # figsize = [map.size, map.size]
    # cmapA = plt.get_cmap('winter')
    # cmapP = plt.get_cmap('afmhot')
    # x, y = mgrid[range(map.size), range(map.size)]
    # z = zeros(figsize)

    # for i, _x in enumerate(range(map.size)):
    #     for j, _y in enumerate(range(map.size)):
    #         z[i][j] += map.PheMap[(_x, _y)]
    #
    # fig, ax = plt.subplots(subplot_kw={'xticks':[], 'yticks':[]},facecolor=cmapP(0),figsize=array(figsize)/4)
    #
    # im = plt.contourf(x,y,z,cmap=cmapP)
    #
    #
    # fig.tight_layout()
    # fig.savefig('Test-fig015.png',bbox_inches='tight', facecolor=fig.get_facecolor())

    ############################## above comments : to draw pheromone plot #################


    # # make subplots
    # fig, ax = plt.subplots(figsize = array(figsize)/4)
    # ax.set_xlim(-1,30)
    # ax.set_ylim(-1,30)
    # #fig,ax = plt.subplots(subplot_kw={'xticks':[], 'yticks':[]}, figsize=array(figsize)/4)
    # #im = plt.contourf(x, y, z, cmap=cmapP)
    #
    # sample_agent = agent_swarm.agents[0]
    # line, = ax.plot(sample_agent.history[0][0], sample_agent.history[0][1])
    # def animate(i):
    #     if i<11:
    #         line.set_xdata(sample_agent.history[i][0])
    #         line.set_ydata(sample_agent.history[i][1])
    #     return line,
    #
    # ani = animation.FuncAnimation(fig, animate, interval=30, blit=True)
    # plt.show()