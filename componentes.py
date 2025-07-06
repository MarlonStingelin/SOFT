import copy
from abstracoes import IEncaixe, IPecaPrototipo 

class BordaReta(IEncaixe):
    def get_tipo_id(self) -> int:
        return 0

class Entrada(IEncaixe):
    def __init__(self, tipo_id: int):
        if tipo_id % 2 == 0 or tipo_id < 1:
            raise ValueError("ID de Entrada deve ser um número ímpar positivo.")
        self._tipo_id = tipo_id

    def get_tipo_id(self) -> int:
        return self._tipo_id

class Saida(IEncaixe):
    def __init__(self, tipo_id: int):
        if tipo_id % 2 != 0 or tipo_id < 2:
            raise ValueError("ID de Saída deve ser um número par positivo.")
        self._tipo_id = tipo_id

    def get_tipo_id(self) -> int:
        return self._tipo_id

class Peca(IPecaPrototipo):
    
    def __init__(self):
        self._pos_y: int = 0
        self._pos_x: int = 0
        self._encaixes: Dict[str, IEncaixe] = {
            "norte": None, "sul": None, "leste": None, "oeste": None
        }

    def clonar(self) -> IPecaPrototipo:
        return copy.deepcopy(self)

    def set_posicao(self, y: int, x: int):
        self._pos_y = y
        self._pos_x = x

    def set_encaixe(self, direcao: str, encaixe: IEncaixe):
        if direcao in self._encaixes:
            self._encaixes[direcao] = encaixe
        else:
            raise ValueError(f"Direção inválida: {direcao}")
            
    def get_encaixe(self, direcao: str) -> IEncaixe:
        return self._encaixes.get(direcao)

    def gerar_saida_formatada(self) -> str:
        n = self._encaixes["norte"].get_tipo_id()
        o = self._encaixes["oeste"].get_tipo_id()
        l = self._encaixes["leste"].get_tipo_id()
        s = self._encaixes["sul"].get_tipo_id()
        
        # Saída: y,x-n,o,l,s
        return f"{self._pos_y},{self._pos_x}-{n},{o},{l},{s}"
