from abstracoes import IFabricaEstilos, IEncaixe 
from componentes import Entrada, Saida 

class FabricaEstiloConcreta(IFabricaEstilos):
    def __init__(self, estilo_id: int):
        if estilo_id <= 0:
            raise ValueError("ID do Estilo deve ser um inteiro positivo.")
        self._estilo_id = estilo_id

    def criar_entrada(self) -> IEncaixe:
        tipo_id = (2 * self._estilo_id) - 1
        return Entrada(tipo_id)

    def criar_saida(self) -> IEncaixe:
        tipo_id = 2 * self._estilo_id
        return Saida(tipo_id)
