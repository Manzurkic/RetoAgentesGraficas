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
                coords = [(25, 0), (27, 0)]
                celdaEnfrente = random.choice(coords)
            else:
                celdaEnfrente = (self.pos[0], newY)
            celdaDerecha = (self.pos[0]+1, self.pos[1])
            celdaIzquierda = (self.pos[0]-1, self.pos[1])
        elif self.frente == 1:
            newX = self.pos[0] + 1
            if newX >= self.model.grid.width:
                coords = [(0, 28), (0, 30)]
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

        if self.pos == (25, 27) or self.pos == (27, 27):
            if self.model.grid[23][32].color == 2 or self.model.grid[23][32].color == 3:
                return

        elif self.pos == (24, 28) or self.pos == (24, 30):
            if self.model.grid[29][26].color == 2 or self.model.grid[29][26].color == 3:
                return

        if self.pos == (27, 28) or self.pos == (25, 30):
            # 0 - derecho, 1 ó 2 - derecha ó izquierda
            proxMov = random.choice([0, 1, 2])
            if proxMov == 0 and self.model.grid.is_cell_empty(celdaEnfrente):
                self.model.grid.move_agent(self, celdaEnfrente)

            else:
                if self.frente == 0 and self.pos == (27, 28) and self.model.grid.is_cell_empty(celdaDerecha):
                    self.model.grid.move_agent(self, celdaDerecha)
                    # Hacer que el frente del coche gire cuando se gira hacia la derecha
                    self.frente += 1
                    # Solo hay cuatro direcciones posibles, regresar a direccion 0
                    if self.frente == 4:
                        self.frente = 0

                elif self.frente == 1 and self.pos == (25, 30) and self.model.grid.is_cell_empty(celdaIzquierda):
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
        semaforo1 = 0
        semaforo2 = 0
        for i in range(12, 25):
                if not self.model.grid.is_cell_empty((i, 28)):
                    semaforo1 += 1
                if not self.model.grid.is_cell_empty((i, 30)):
                    semaforo1 += 1

        for i in range(14, 28):
            if not self.model.grid.is_cell_empty((25, i)):
                semaforo2 += 1
            if not self.model.grid.is_cell_empty((27, i)):
                semaforo2 += 1

        if self.model.grid[23][32].color == 1 and self.model.grid[29][26].color == 3 and semaforo2 == 0 and (self.model.grid[23][32].pasos == 5 or self.model.grid[29][26].pasos == 5):
            self.model.grid[29][26].color = 3
            self.model.grid[29][26].pasos = 0
            self.model.grid[23][32].color = 3
            self.model.grid[23][32].pasos = 0

        elif self.model.grid[23][32].color == 3 and self.model.grid[29][26].color == 1 and semaforo1 == 0 and (self.model.grid[23][32].pasos == 5 or self.model.grid[29][26].pasos == 5):
            self.model.grid[29][26].color = 3
            self.model.grid[29][26].pasos = 0
            self.model.grid[23][32].color = 3
            self.model.grid[23][32].pasos = 0

        if self.model.grid[29][26].color == 3 and self.model.grid[23][32].color == 3 and self.pasos == 5:
            if semaforo1 >= semaforo2:
                self.model.grid[29][26].color = 1
            else:
                self.model.grid[23][32].color = 1
            return

        elif self.pasos > 5 and self.model.grid[29][26].color == 3 and self.model.grid[23][32].color == 3:
            self.pasos = 0

        elif self.model.grid[29][26].color == 1 and self.pasos == 22:
            self.model.grid[29][26].color = 2

        elif self.model.grid[23][32].color == 1 and self.pasos == 22:
            self.model.grid[23][32].color = 2

        elif self.model.grid[29][26].color == 2 and self.pasos == 32:
            self.model.grid[29][26].color = 3
            self.pasos = 0
            print('f')

        elif self.model.grid[23][32].color == 2 and self.pasos == 32:
            self.model.grid[23][32].color = 3
            self.pasos = 0
            print('f')


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

        for i in range(int(width/2 - 2)):
            x = i
            y = int(height/2)
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(height/2)):
            x = int(width/2 - 3)
            y = i
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(width/2 + 1), width):
            x = i
            y = int(height/2)
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(height/2)):
            x = int(width/2 + 1)
            y = i
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(width/2 - 2)):
            x = i
            y = int(height/2 + 4)
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(height/2 + 5), height):
            x = int(width/2 - 3)
            y = i
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(width/2 + 1), width):
            x = i
            y = int(height/2 + 4)
            coord = (x, y)
            listaCoords.append(coord)

        for i in range(int(height/2 + 5), height):
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
            #positions = [(25, 0), (27, 0), (0, 30), (0, 28),
            #             (25, 2), (27, 2), (2, 30), (2, 28),
            #             (25, 4), (27, 4), (4, 30), (4, 28)]
            positions = [(27,0),(25,0)]
            
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
            posSemaforos = [(23, 32), (29, 26)]
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

        agents = self.schedule.agents
        ps = []

        for a in agents:
            if isinstance(a, AgenteVehiculo):
                xy = a.pos
                p = [xy[0], xy[1], -1.67]
                ps.append(p)

        return ps
