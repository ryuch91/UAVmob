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
    def __init__(self, map, agent_swarm):
        self.map = map
        self.agent_swarm = agent_swarm

    def run(self, steps):

        for i in range(steps):
            self.agent_swarm.update_phe_info(self.map.PheMap) #first info update
            agents_locs = self.agent_swarm.get_all_pos()
            self.map.update_phe(agents_locs)
            self.agent_swarm.cal_and_move()
            self.map.phe_decay() # pheromone decay


if __name__ == '__main__':
    # Generate Map
    map = Map(CONFIG['MapSize'])
    agent_swarm = AgentSwarm()
    agent_swarm.create_agents(CONFIG['SwarmSize'])
    new_sim = Simulation(map, agent_swarm)
    new_sim.run(CONFIG['TotalStep'])

    ## setup the figure, axis
    figsize = [map.size, map.size]
    cmapA = plt.get_cmap('winter')
    cmapP = plt.get_cmap('afmhot')
    x, y = mgrid[range(map.size), range(map.size)]
    z = zeros(figsize)

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

    for i, _x in enumerate(range(map.size)):
        for j, _y in enumerate(range(map.size)):
            z[i][j] += map.PheMap[(_x, _y)]

    fig, ax = plt.subplots(subplot_kw={'xticks':[], 'yticks':[]},facecolor=cmapP(0),figsize=array(figsize)/4)

    im = plt.contourf(x,y,z,cmap=cmapP)


    fig.tight_layout()
    fig.savefig('Test-fig015.png',bbox_inches='tight', facecolor=fig.get_facecolor())