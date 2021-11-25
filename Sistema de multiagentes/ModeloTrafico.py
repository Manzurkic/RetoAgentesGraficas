"""
Sistema de multiagentes que simula el tránsito en
una pequeña ciudad

Solución al reto de TC2008B semestre AgostoDiciembre 2021
Autor: Equipo 6
"""

from mesa import Model, Agent
from mesa.space import SingleGrid
from mesa.time import RandomActivation
import random


class AgenteVehiculo(Agent):
    '''
    Agente que simula el comportamiento
    de un vehículo
    '''

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tipo = random.choice([1, 2, 3])

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=True
        )
        print(possible_steps)
        myPos = possible_steps[2]

        # Verificar los espacios que no están ocupados
        espaciosLibres = []
        for pos in possible_steps:
            espaciosLibres.append(self.model.grid.is_cell_empty(pos))

        if espaciosLibres == []:
            return
        else:
            newPos = (myPos[0], myPos[1]+1)
            if newPos[1] < self.model.grid.width and self.model.grid.is_cell_empty(newPos):
                self.model.grid.move_agent(self, (newPos))
            else:
                print("Acabó la simulación")
                return

    def step(self):
        self.move()


class AgenteBanqueta(Agent):
    '''
    En realidad no es un agente pero nos
    ayuda a simular la existencia de banquetas
    en la simulación
    '''

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass


class TraficModel(Model):
    '''
    Modelo para la simulación de tránsito
    '''

    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = SingleGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Crear banquetas
        numBanq = (width * 2) + (height * 2 - 4)
        listaPosLimite = []

        for col in [0, width-1]:
            for ren in range(height):
                listaPosLimite.append((col, ren))

        for col in range(1, width-1):
            for ren in [0, height-1]:
                listaPosLimite.append((col, ren))

        for i in range(numBanq):
            a = AgenteBanqueta(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, listaPosLimite[i])

        # Añadir los vehículos a las celdas
        c = 1
        for i in range(numBanq, numBanq + self.num_agents):
            a = AgenteVehiculo(i, self)
            self.schedule.add(a)

            x = c
            y = 1
            self.grid.place_agent(a, (x, y))
            c += 1

    def step(self):
        '''
        Avanzar el modelo un paso
        '''
        self.schedule.step()
