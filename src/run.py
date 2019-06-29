import matplotlib.pyplot as plt
import matplotlib.colors as clrs
from matplotlib import animation
from numpy import array, mgrid, zeros, linspace
from numpy.random import choice

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

    # nUAV x 반복횟수 만큼 시뮬 진행. 각 시뮬은 step 수 만큼 진행
    def run(self):

        # 3개의 UAV 개수에 대해 실험 진행
        for i in range(len(self.nUAVs)):
            # UAV 생성 및 초기화
            nUAVs = self.nUAVs[i]
            swarm = AgentSwarm(nUAVs)
            swarm.set_map_info(self.map.Obs, self.map.mapSize)

            for j in range(self.nRepeat):

                #각 시뮬 순서 : 1.이동가능방향계산/2.페로몬정보전달/3.무빙-전체페로몬맵업뎃-전달 반복/4.페로맵리셋/5.스웜리셋
                # swarm.cal_movable_blocks()
                # swarm.update_phe_info(self.map.PheMap)
                # for k in range(self.nStep):
                #     swarm.cal_and_move_rand()
                #     self.map.update_phe(swarm.get_all_pos())
                #     swarm.update_phe_info(self.map.PheMap)
                #     self.draw('rand',i,j,k) # 테스트용 그리기
                #     swarm.print_path()# 테스트용 출력
                # self.map.reboot_phe()
                # swarm.init_agents(nUAVs)


                swarm.cal_movable_blocks()
                swarm.update_phe_info(self.map.PheMap)
                for k in range(self.nStep):
                    swarm.cal_and_move_phe()
                    self.map.update_phe(swarm.get_all_pos())
                    swarm.update_phe_info(self.map.PheMap)
                    self.draw('phe',i, j, k)  # 테스트용 그리기
                self.map.reboot_phe()
                self.map.print_pheMap()
                swarm.init_agents(nUAVs)
                #
                #
                # swarm.cal_movable_blocks()
                # swarm.update_phe_info(self.map.PheMap)
                # for k in range(self.nStep):
                #     swarm.cal_and_move_flex()
                #     self.map.update_phe(swarm.get_all_pos())
                #     swarm.update_phe_info(self.map.PheMap)
                #     self.draw('flex',i, j, k)  # 테스트용 그리기
                # self.map.reboot_phe()
                # swarm.init_agents(nUAVs)

                print(str(i)+'-'+str(j)+' finished!') # 진행사항을 알기위한 콘솔 출력

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