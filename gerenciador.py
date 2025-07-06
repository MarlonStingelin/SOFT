from typing import Dict
from abstracoes import IPecaPrototipo 

class GerenciadorDePrototipos:
    #cópias de peças
    def __init__(self):
        self._prototipos: Dict[str, IPecaPrototipo] = {}

    def adicionar_prototipo(self, chave: str, peca: IPecaPrototipo):
        self._prototipos[chave] = peca

    def obter_peca_clonada(self, chave: str) -> IPecaPrototipo:
        prototipo = self._prototipos.get(chave)
        if not prototipo:
            raise ValueError(f"Protótipo com a chave '{chave}' não encontrado.")
        return prototipo.clonar()
      
