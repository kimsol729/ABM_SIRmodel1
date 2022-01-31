from mesa.visualization.ModularVisualization import ModularServer
from SEIRmodel import SEIRmeaslesModel
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import CanvasGrid


def agent_portrayal(agent):
    portrayal = {"Shape" : "circle","Filled":"true","r":0.5}

    if agent.state == 0:
        portrayal["Color"] = "Green"
        portrayal["Layer"] = 0
    elif agent.state ==1:
        portrayal["Color"] = "Orange"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.3
    elif agent.state ==2:
        portrayal["Color"] = "Red"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.3
    else:
        portrayal["Color"] = "Black"
        portrayal["Layer"] = 3 
        portrayal["r"] = 0.2
    return portrayal

grd = CanvasGrid(agent_portrayal,10,10,500,500)
chart = ChartModule(
    [{"Label":"Susceptible","Color" : "Green"},
    {"Label":"Expose","Color" : "Orange"},
    {"Label":"Infectious","Color" : "red"},
    {"Label":"Recover","Color" : "black"}],data_collector_name="datacollector"
)
#={"Susceptible":sum_S,"Expose":sum_E,"Infectious":sum_I,"Recover":sum_R})
server = ModularServer(SEIRmeaslesModel,[grd,chart])
server.port = 8521
