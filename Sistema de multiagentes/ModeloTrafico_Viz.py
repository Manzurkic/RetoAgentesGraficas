"""
Visualización del sistema de multiagentes que simula
el tránsito en una pequeña ciudad

Solución al reto de TC2008B semestre AgostoDiciembre 2021
Autor: Equipo 6
"""

from ModeloTrafico import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portayal = {'Shape': 'rect',
                'Filled': 'true',
                'Layer': 0,
                'Color': 'red',
                'w': 1,
                'h': 1,
                'text': str(agent.unique_id)}

    if (isinstance(agent, AgenteBanqueta)):
        portayal['Color'] = 'grey'
    return portayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(TraficModel,
                       [grid],
                       'Modelo de tráfico',
                       {'N': 8, 'width': 10, 'height': 10})
server.port = 8521  # The default
server.launch()
