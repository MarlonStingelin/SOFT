import random
from typing import List
# from abstracoes import IFabricaEstilos # (Em arquivo separado)
# from fabricas import FabricaEstiloConcreta # (Em arquivo separado)
# from gerenciador import GerenciadorDePrototipos # (Em arquivo separado)
# from componentes import Peca, BordaReta, Entrada, Saida, IEncaixe # (Em arquivo separado)

class GeradorQuebraCabeca:

    def __init__(self, altura: int, comprimento: int, qtd_estilos: int):
        self._altura = altura
        self._comprimento = comprimento
        self._fabricas_de_estilos: List[IFabricaEstilos] = [
            FabricaEstiloConcreta(i) for i in range(1, qtd_estilos + 1)
        ]
        self._gerenciador_prototipos = GerenciadorDePrototipos()
        self._inicializar_prototipos()
        
    def _inicializar_prototipos(self):
        self._gerenciador_prototipos.adicionar_prototipo("meio", Peca())
        
        pecas_com_bordas = {
            "borda_norte": {"norte": BordaReta()}, "borda_sul": {"sul": BordaReta()},
            "borda_leste": {"leste": BordaReta()}, "borda_oeste": {"oeste": BordaReta()},
            "canto_no": {"norte": BordaReta(), "oeste": BordaReta()},
            "canto_ne": {"norte": BordaReta(), "leste": BordaReta()},
            "canto_so": {"sul": BordaReta(), "oeste": BordaReta()},
            "canto_se": {"sul": BordaReta(), "leste": BordaReta()},
        }
        for nome, config in pecas_com_bordas.items():
            peca = Peca()
            for direcao, encaixe in config.items():
                peca.set_encaixe(direcao, encaixe)
            self._gerenciador_prototipos.adicionar_prototipo(nome, peca)

    def _determinar_tipo_peca(self, y: int, x: int) -> str:
        e_borda_norte = (y == 0)
        e_borda_sul = (y == self._altura - 1)
        e_borda_oeste = (x == 0)
        e_borda_leste = (x == self._comprimento - 1)

        if e_borda_norte and e_borda_oeste: return "canto_no"
        if e_borda_norte and e_borda_leste: return "canto_ne"
        if e_borda_sul and e_borda_oeste: return "canto_so"
        if e_borda_sul and e_borda_leste: return "canto_se"
        if e_borda_norte: return "borda_norte"
        if e_borda_sul: return "borda_sul"
        if e_borda_oeste: return "borda_oeste"
        if e_borda_leste: return "borda_leste"
        return "meio"

    def _criar_deck_de_fabricas_balanceado(self) -> List[IFabricaEstilos]:
        conexoes_horizontais = self._altura * (self._comprimento - 1)
        conexoes_verticais = self._comprimento * (self._altura - 1)
        total_conexoes = conexoes_horizontais + conexoes_verticais
        
        num_estilos = len(self._fabricas_de_estilos)
        deck = []
        
        for i in range(total_conexoes):
            fabrica = self._fabricas_de_estilos[i % num_estilos]
            deck.append(fabrica)
            
        random.shuffle(deck) 
        return deck

    def gerar_grade_de_pecas(self) -> List[str]:
        if not self._fabricas_de_estilos:
            raise ValueError("Nenhum estilo de encaixe foi definido.")

        deck_de_fabricas = self._criar_deck_de_fabricas_balanceado()

        grade_de_pecas = [[None for _ in range(self._comprimento)] for _ in range(self._altura)]

        for y in range(self._altura):
            for x in range(self._comprimento):
                tipo_peca = self._determinar_tipo_peca(y, x)
                peca_atual = self._gerenciador_prototipos.obter_peca_clonada(tipo_peca)
                peca_atual.set_posicao(y, x)
                grade_de_pecas[y][x] = peca_atual

                if y > 0:
                    vizinho_norte = grade_de_pecas[y-1][x]
                    encaixe_sul_vizinho = vizinho_norte.get_encaixe("sul")
                    id_fabrica_usada = (encaixe_sul_vizinho.get_tipo_id() -1) // 2
                    fabrica_usada = self._fabricas_de_estilos[id_fabrica_usada]
                    
                    if isinstance(encaixe_sul_vizinho, Entrada):
                        peca_atual.set_encaixe("norte", fabrica_usada.criar_saida())
                    else:
                        peca_atual.set_encaixe("norte", fabrica_usada.criar_entrada())
                
                if x > 0:
                    vizinho_oeste = grade_de_pecas[y][x-1]
                    encaixe_leste_vizinho = vizinho_oeste.get_encaixe("leste")
                    id_fabrica_usada = (encaixe_leste_vizinho.get_tipo_id() -1) // 2
                    fabrica_usada = self._fabricas_de_estilos[id_fabrica_usada]

                    if isinstance(encaixe_leste_vizinho, Entrada):
                        peca_atual.set_encaixe("oeste", fabrica_usada.criar_saida())
                    else:
                        peca_atual.set_encaixe("oeste", fabrica_usada.criar_entrada())

                for direcao in ["sul", "leste"]:
                    if peca_atual.get_encaixe(direcao) is None:
                        # reinicia o baralho
                        if not deck_de_fabricas:
                            deck_de_fabricas = self._criar_deck_de_fabricas_balanceado()
                        
                        fabrica = deck_de_fabricas.pop()
                        peca_atual.set_encaixe(direcao, random.choice([fabrica.criar_entrada(), fabrica.criar_saida()]))

        saidas_formatadas = [grade_de_pecas[y][x].gerar_saida_formatada() for y in range(self._altura) for x in range(self._comprimento)]
        return saidas_formatadas
