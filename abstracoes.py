from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from componentes import IPecaPrototipo

class IEncaixe(ABC):
    
    @abstractmethod
    def get_tipo_id(self) -> int:
        pass

class IFabricaEstilos(ABC):

    @abstractmethod
    def criar_entrada(self) -> IEncaixe:
        pass

    @abstractmethod
    def criar_saida(self) -> IEncaixe:
        pass

class IPecaPrototipo(ABC):

    @abstractmethod
    def clonar(self) -> 'IPecaPrototipo':
        pass

    @abstractmethod
    def set_posicao(self, y: int, x: int):
        pass

    @abstractmethod
    def set_encaixe(self, direcao: str, encaixe: IEncaixe):
        pass
    
    @abstractmethod
    def get_encaixe(self, direcao: str) -> IEncaixe:
        pass

    @abstractmethod
    def gerar_saida_formatada(self) -> str:
        pass

  
