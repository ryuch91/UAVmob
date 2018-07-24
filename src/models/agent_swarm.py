from src.models.agent import Agent
from src.conf import CONFIG

class AgentSwarm:
    def __init__(self):
        self.agents = []

    def create_agents(self, agents_number):
        for i in range(agents_number):
            agent = Agent(CONFIG['Nest'])
            self.agents.append(agent)

    # return all agents' position in list
    def get_all_pos(self):
        locs = []
        for agent in self.agents:
            locs.append(agent.get_pos())
        return locs

    def get_all_agents(self):
        return self.agents

    # Give neighbor cell's pheromone info to each agent
    def update_phe_info(self, phe_map):
        max_size = CONFIG['MapSize']
        for agent in self.agents:
            blocks= []
            agent.clear_phe_map()
            x, y = agent.get_pos()
            blocks += [(x-1,y+1),(x,y+1),(x+1,y+1)]
            blocks += [(x-1,y),(x+1,y)]
            blocks += [(x-1,y-1),(x,y-1),(x+1,y-1)]

            # remove 'out-of-box' position key from blocks
            to_remove = [i for i, key in enumerate(blocks) if (-1 in key) or (max_size in key)]
            for idx in reversed(to_remove):
                del blocks[idx]

            blocks_set = set(blocks)
            blocks = list(blocks_set)
            for key in blocks:
                agent.phe_map[key] = phe_map[key]

    def cal_and_move(self):
        for agent in self.agents:
            next_pos = agent.cal_next_pos()
            agent.move_to(next_pos)
