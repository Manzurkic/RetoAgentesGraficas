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
        self.direccion = 0    # 0 - derecho, 1 - derecha
        self.frente = 0       # 0 - arriba, 1 - abajo, 2 - izq, 3 - der

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False
        )

        if self.frente == 0:
            celdaEnfrente = (self.pos[0], self.pos[1]+1)
            celdaDerecha = (self.pos[0]+1, self.pos[1])
            # if celdaEnfrente[1] > self.model.grid.height

        elif self.frente == 1:
            celdaEnfrente = (self.pos[0], self.pos[1]-1)
            celdaDerecha = (self.pos[0]-1, self.pos[1])
        elif self.frente == 2:
            celdaEnfrente = (self.pos[0]-1, self.pos[1])
            celdaDerecha = (self.pos[0], self.pos[1]+1)
        elif self.frente == 3:
            celdaEnfrente = (self.pos[0]+1, self.pos[1])
            celdaDerecha = (self.pos[0], self.pos[1]-1)

        if not self.model.grid.out_of_bounds(celdaEnfrente) and self.model.grid.is_cell_empty(celdaEnfrente):
            self.model.grid.move_agent(self, celdaEnfrente)

        elif not self.model.grid.out_of_bounds(celdaDerecha) and self.model.grid.is_cell_empty(celdaDerecha):
            self.model.grid.move_agent(self, celdaDerecha)

        else:
            print("xd")
            return

        '''
        self.direccion = random.choice([0, 1, 2, 3])
        if self.direccion == 0:
            newPos = (self.pos[0], self.pos[1]+1)
            if not self.model.grid.out_of_bounds(newPos):
                if self.model.grid.is_cell_empty(newPos):
                    self.model.grid.move_agent(self, (newPos))

        if self.direccion == 1:
            newPos = (self.pos[0], self.pos[1]-1)
            if not self.model.grid.out_of_bounds(newPos):
                if self.model.grid.is_cell_empty(newPos):
                    self.model.grid.move_agent(self, (newPos))

        if self.direccion == 2:
            newPos = (self.pos[0]-1, self.pos[1])
            if not self.model.grid.out_of_bounds(newPos):
                if self.model.grid.is_cell_empty(newPos):
                    self.model.grid.move_agent(self, (newPos))

        if self.direccion == 1:
            newPos = (self.pos[0]+1, self.pos[1])
            if not self.model.grid.out_of_bounds(newPos):
                if self.model.grid.is_cell_empty(newPos):
                    self.model.grid.move_agent(self, (newPos))
        '''

    def step(self):
        self.move()


class AgenteSemaforo(Agent):
    '''
    Agente que simula el comportamiento de los
    semáforos
    '''

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # 1 - verde, 2 - amarillo, 3 - rojo
        self.color = random.choice([1, 2, 3])

    def step(self):
        pass


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
        numBanq = (width*2 - 2) + (height*2 - 2)
        listaCoords = []

        for i in range(int(width/2 - 1)):
            x = i
            y = int(height/2 - 2)
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(height/2 - 2)):
            x = int(width/2 - 2)
            y = i
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(width/2 + 1), width):
            x = i
            y = int(height/2 - 2)
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(height/2 - 2)):
            x = int(width/2 + 1)
            y = i
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(width/2 - 1)):
            x = i
            y = int(height/2 + 1)
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(height/2 + 2), height):
            x = int(width/2 - 2)
            y = i
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(width/2 + 1), width):
            x = i
            y = int(height/2 + 1)
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(height/2 + 2), height):
            x = int(width/2 + 1)
            y = i
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(len(listaCoords)):
            a = AgenteBanqueta(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, listaCoords[i])

        # Añadir los vehículos a las celdas
        for i in range(numBanq, numBanq + self.num_agents):
            a = AgenteVehiculo(i, self)
            self.schedule.add(a)
            x = 0
            y = 12
            self.grid.place_agent(a, (x, y))

    def step(self):
        '''
        Avanzar el modelo un paso
        '''
        self.schedule.step()
