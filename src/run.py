import matplotlib.pyplot as plt
import matplotlib.colors as clrs
from matplotlib import animation
from numpy import array, mgrid, zeros, linspace
from numpy.random import choice
import csv

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

    # nUAV x 반복횟수 만큼 시뮬 진행. 각 시뮬은 step 수 만큼 진행
    def run(self):

        # 3개의 UAV 개수에 대해 실험 진행
        for i in range(len(self.nUAVs)):
            # UAV 생성 및 초기화
            nUAVs = self.nUAVs[i]
            swarm = AgentSwarm(nUAVs)
            swarm.set_map_info(self.map.Obs, self.map.mapSize, self.map.Targets)

            for j in range(self.nRepeat):

                #각 시뮬 순서 : 1.이동가능방향계산/2.페로몬정보전달/3.무빙-전체페로몬맵업뎃-전달 반복/4.페로맵리셋/5.스웜리셋
                swarm.cal_movable_blocks()
                swarm.update_phe_info(self.map.PheMap)
                for k in range(self.nStep):
                    swarm.cal_and_move_rand()
                    self.map.update_phe(swarm.get_all_pos())
                    swarm.update_phe_info(self.map.PheMap)

                    swarm.sense_target()
                    self.nlistST.append(swarm.count_sensed_target())

                self.map.reboot_phe()
                swarm.init_agents(nUAVs)

                self.nlistlistST.append(self.nlistST)
                self.init_metric()

                print(str(i) + '-' + str(j) + '-rand' + ' finished!')  # 진행사항을 알기위한 콘솔 출력

            self.write_csv_metric0(self.nlistlistST, self.map.mapSize, self.map.scene, self.map.nT, nUAVs, 'Rand')
            self.init_upper_metric()

            for j in range(self.nRepeat):

                swarm.cal_movable_blocks()
                swarm.update_phe_info(self.map.PheMap)
                for k in range(self.nStep):
                    swarm.cal_and_move_phe()
                    self.map.update_phe(swarm.get_all_pos())
                    swarm.update_phe_info(self.map.PheMap)

                    # Metric 0 을 위한 타겟 수 기록
                    swarm.sense_target()
                    self.nlistST.append(swarm.count_sensed_target())

                self.map.reboot_phe()
                swarm.init_agents(nUAVs)

                self.nlistlistST.append(self.nlistST)
                self.init_metric() # 메트릭 관련 변수들(새 repeat 마다 초기화되어야하는것들) 초기화

                print(str(i) + '-' + str(j) + '-phe' + ' finished!')  # 진행사항을 알기위한 콘솔 출력

            self.write_csv_metric0(self.nlistlistST, self.map.mapSize, self.map.scene, self.map.nT, nUAVs, 'Phe')
            self.init_upper_metric()

            for j in range(self.nRepeat):
                swarm.cal_movable_blocks()
                swarm.update_phe_info(self.map.PheMap)
                for k in range(self.nStep):
                    swarm.cal_and_move_flex()
                    self.map.update_phe(swarm.get_all_pos())
                    swarm.update_phe_info(self.map.PheMap)

                    swarm.sense_target()
                    self.nlistST.append(swarm.count_sensed_target())

                self.map.reboot_phe()
                swarm.init_agents(nUAVs)

                self.nlistlistST.append(self.nlistST)
                self.init_metric()

                print(str(i)+'-'+str(j)+'-flex'+' finished!') # 진행사항을 알기위한 콘솔 출력

            self.write_csv_metric0(self.nlistlistST, self.map.mapSize, self.map.scene, self.map.nT, nUAVs, 'Flex')
            self.init_upper_metric() # 전체 stepxrepeat 끝날때마다 초기화되어야 하는 것들 초기화

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

    def init_metric(self):
        self.nlistST = []

    def init_upper_metric(self):
        self.nlistST = []
        self.nlistlistST = []

    # Met0: 타겟 수 측정을 위한 csv 파일에 작성 (data는 list of list)
    def write_csv_metric0(self, data, mapSize, scene, nT, nU, method):
        new_data = list(zip(*data))

        filename = 'Map'+str(mapSize[0])+'_Scene'+str(scene)+'_T'+str(nT)+'_U'+str(nU)+method+'_Met0.csv'
        f = open(filename, 'w', newline='')
        wr = csv.writer(f)

        for row in new_data:
            wr.writerow(row)

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