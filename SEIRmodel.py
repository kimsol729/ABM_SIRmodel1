from mesa import Agent,Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector


def sum_S(model):
    return sum([1 for agent in model.schedule.agents if agent.state==0])

def sum_E(model):
    return sum([1 for agent in model.schedule.agents if agent.state==1])

def sum_I(model):
    return sum([1 for agent in model.schedule.agents if agent.state==2])

def sum_R(model):
    return sum([1 for agent in model.schedule.agents if agent.state==3])


class SEIRmeaslesModel(Model):
    """Set up the SEIR model of the transmission dynamics of measles in a closed population using difference equations:        
    We assume that individuals mix randomly and parameter values are given as follows: 
    Population 100 people
    Pre-infectious period 8 days
    Infectious period 7 days
    Basic reproduction number 13--
    Initial values (S,E,I,R)=(99,0,1,0) """

    def __init__(self,S=99,E=0,I=1,R=0,width = 10,height = 10):
        self.num_S = S
        self.num_E = E
        self.num_I = I
        self.num_R = R
        self.grid = MultiGrid(height,width,True) #Torus True?
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(model_reporters={"Susceptible":sum_S,"Expose":sum_E,"Infectious":sum_I,"Recover":sum_R})

        #Creating agents
        for i in range(self.num_S):
            a = SEIRagent(i,self,0)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a,(x,y))

        for i in range(self.num_E):
            a = SEIRagent(S+i,self,1)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a,(x,y))

        for i in range(self.num_I):
            a = SEIRagent(S+E+i,self,2)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a,(x,y))

        for i in range(self.num_R):
            a = SEIRagent(S+E+I+i,self,3)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a,(x,y))

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def run_model(self):
            self.step()

class SEIRagent(Agent):
    def __init__(self,unique_id,model,states):
        super().__init__(unique_id, model)
        self.state = states
        self.beta = 1 # transmissibility
        self.pre_infec = 7 # pre infectious period
        self.infec = 8 # infectious period
        self.inf_t = 0 # 개인이 감염에 걸린 시기

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,moore = False,include_center = False
        )
        new_pos = self.random.choice(possible_steps)
        self.model.grid.move_agent(self,new_pos)

    
    def Flow(self):
        if self.state == 1 and self.model.schedule.steps == self.inf_t+self.pre_infec:
            self.state = 2

        elif self.state == 2:
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            if len(cellmates)>1:
                for other in cellmates:
                    if other.state == 0 and self.model.random.random()<=self.beta:
                        other.state = 1
                        other.inf_t = self.model.schedule.steps

            if self.inf_t + self.pre_infec + self.infec == self.model.schedule.steps:
                self.state = 3

    def step(self):
        self.move()
        self.Flow()