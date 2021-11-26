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
        self.frente = 0       # 0 - arriba, 1 - derecha, 2 - abajo, 3 - izquierda

    def move(self):

        if self.frente == 0:
            newY = self.pos[1] + 1
            #celdaEnfrente = (self.pos[0], self.pos[1]+1)
            if newY >= self.model.grid.height:
                coords = [(11, 0), (12, 0)]
                celdaEnfrente = random.choice(coords)
            else:
                celdaEnfrente = (self.pos[0], newY)
            celdaDerecha = (self.pos[0]+1, self.pos[1])
            celdaIzquierda = (self.pos[0]-1, self.pos[1])
        elif self.frente == 1:
            newX = self.pos[0] + 1
            if newX >= self.model.grid.width:
                coords = [(0, 11), (0, 12)]
                celdaEnfrente = random.choice(coords)
            else:
                celdaEnfrente = (newX, self.pos[1])
            #celdaEnfrente = (self.pos[0]+1, self.pos[1])
            celdaDerecha = (self.pos[0], self.pos[1]-1)
            celdaIzquierda = (self.pos[0], self.pos[1]+1)
        elif self.frente == 2:
            newY = self.pos[1] - 1
            if newY <= 0:
                celdaEnfrente = (self.pos[0], self.model.grid.height)
            else:
                celdaEnfrente = (self.pos[0], newY)
            celdaDerecha = (self.pos[0]-1, self.pos[1])
            celdaIzquierda = (self.pos[0]+1, self.pos[1])
        elif self.frente == 3:
            newX = self.pos[0] - 1
            if newX <= 0:
                celdaEnfrente = (self.model.grid.width, self.pos[1])
            else:
                celdaEnfrente = (newX, self.pos[1])
            celdaDerecha = (self.pos[0], self.pos[1]+1)
            celdaIzquierda = (self.pos[0], self.pos[1]-1)

        # if self.model.grid.is_cell_empty(celdaEnfrente):
        #    self.model.grid.move_agent(self, celdaEnfrente)

        if self.pos == (11, 10) or self.pos == (12, 10):
            if self.model.grid[9][14].color == 2 or self.model.grid[9][14].color == 3:
                return

        elif self.pos == (10, 11) or self.pos == (10, 12):
            if self.model.grid[14][9].color == 2 or self.model.grid[14][9].color == 3:
                return

        if self.pos == (12, 11) or self.pos == (11, 12):
            # 0 - derecho, 1 ó 2 - derecha ó izquierda
            proxMov = random.choice([0, 1, 2])
            if proxMov == 0 and self.model.grid.is_cell_empty(celdaEnfrente):
                self.model.grid.move_agent(self, celdaEnfrente)

            else:
                if self.frente == 0 and self.pos == (12, 11) and self.model.grid.is_cell_empty(celdaDerecha):
                    self.model.grid.move_agent(self, celdaDerecha)
                    # Hacer que el frente del coche gire cuando se gira hacia la derecha
                    self.frente += 1
                    # Solo hay cuatro direcciones posibles, regresar a direccion 0
                    if self.frente == 4:
                        self.frente = 0

                elif self.frente == 1 and self.pos == (11, 12) and self.model.grid.is_cell_empty(celdaIzquierda):
                    self.model.grid.move_agent(self, celdaIzquierda)
                    self.frente = 0

        elif self.model.grid.is_cell_empty(celdaEnfrente):
            self.model.grid.move_agent(self, celdaEnfrente)

        else:
            return

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
        self.color = 3
        self.pasos = 0

    def step(self):
        self.pasos += 1
        if self.model.grid[14][9].color == 3 and self.model.grid[9][14].color == 3 and self.pasos == 5:
            semaforo1 = 0
            semaforo2 = 0
            for i in range(0, 11):
                if not self.model.grid.is_cell_empty((i, 11)):
                    semaforo1 += 1
                if not self.model.grid.is_cell_empty((i, 12)):
                    semaforo1 += 1

            for i in range(0, 11):
                if not self.model.grid.is_cell_empty((11, i)):
                    semaforo2 += 1
                if not self.model.grid.is_cell_empty((12, i)):
                    semaforo2 += 1

            if semaforo1 >= semaforo2:
                self.model.grid[14][9].color = 1
            else:
                self.model.grid[9][14].color = 1
            return

        elif self.pasos > 5 and self.model.grid[14][9].color == 3 and self.model.grid[9][14].color == 3:
            self.pasos = 0

        elif self.model.grid[14][9].color == 1 and self.pasos == 11:
            self.model.grid[14][9].color = 2

        elif self.model.grid[9][14].color == 1 and self.pasos == 11:
            self.model.grid[9][14].color = 2

        elif self.model.grid[14][9].color == 2 and self.pasos == 16:
            self.model.grid[14][9].color = 3
            self.pasos = 0
            print('f')

        elif self.model.grid[9][14].color == 2 and self.pasos == 16:
            self.model.grid[9][14].color = 3
            self.pasos = 0
            print('f')

        else:
            return


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
        j = 0
        for i in range(numBanq, numBanq + self.num_agents):
            positions = [(12, 0), (11, 0), (0, 12), (0, 11),
                         (12, 2), (11, 2), (2, 12), (2, 11),
                         (12, 4), (11, 4), (4, 12), (4, 11),
                         (12, 6), (11, 6), (6, 12), (6, 11),
                         (12, 8), (11, 8), (8, 12), (8, 11),
                         (12, 10), (11, 10), (10, 12), (10, 11)]
            #positions = [(12, 0), (11, 0), (0, 12), (0, 11)]
            a = AgenteVehiculo(i, self)
            if positions[j][0] < positions[j][1]:
                a.frente = 1
            self.schedule.add(a)
            x = positions[j][0]
            y = positions[j][1]
            self.grid.place_agent(a, (x, y))
            j += 1

        j = 0
        for i in range(numBanq + self.num_agents, numBanq + self.num_agents + 2):
            posSemaforos = [(9, 14), (14, 9)]
            a = AgenteSemaforo(i, self)
            self.schedule.add(a)
            x = posSemaforos[j][0]
            y = posSemaforos[j][1]
            self.grid.place_agent(a, (x, y))
            j += 1

    def step(self):
        '''
        Avanzar el modelo un paso
        '''
        self.schedule.step()
