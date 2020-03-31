
from queue import Empty, Full, PriorityQueue, Queue

from trasto.infrastructure.memory.repositories import LoggerRepository
from trasto.model.entities import (Prioridad,
                                   ResultadoAccionRepositoryInterace, Tarea,
                                   TareaRepositoryInterface)
from trasto.model.value_entities import ResultadoAccion                                   

QUEUE_TIMEOUT = 10

tareas = PriorityQueue(maxsize=10)
comandos = Queue()

tareas_para_ejecutar = Queue()
resultados_accion = Queue()



class TareaRepository(TareaRepositoryInterface):

    def __init__(self):
        self.logger = LoggerRepository('tarea_repo')

    def next_tarea(self):
        while True:
            try:
                self.logger.debug("esperando por tarea")
                yield tareas.get(block=True, timeout=QUEUE_TIMEOUT)
            except Empty:
                pass


    def append(self, tarea: Tarea):
        try:
            tareas.put(tarea)
        except:
            self.logger.crit("Cola de tareas llena!!!!")
    


class ResultadoAccionRepository(ResultadoAccionRepositoryInterace):
    def __init__(self):
        self.logger = LoggerRepository('resultados_accion_repo')

    def next_resultado(self):
        while True:
            try:
                yield resultados_accion.get(block=True, timeout=QUEUE_TIMEOUT)
            except Empty:
                pass
        

    def send_resultado(self, tarea: Tarea, resultado: ResultadoAccion):
        try:
            tarea.set_resultado(resultado)
            resultados_accion.put(tarea)
        except Full:
            self.logger.crit("Cola resultado accion llena!!!!")

