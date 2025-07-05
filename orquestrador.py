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
            "borda_norte": {"norte": BordaReta()},
            "borda_sul": {"sul": BordaReta()},
            "borda_leste": {"leste": BordaReta()},
            "borda_oeste": {"oeste": BordaReta()},
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

    def gerar_grade_de_pecas(self) -> List[str]:
        if not self._fabricas_de_estilos:
            raise ValueError("Nenhum estilo de encaixe foi definido.")

        grade_de_pecas = [[None for _ in range(self._comprimento)] for _ in range(self._altura)]

        for y in range(self._altura):
            for x in range(self._comprimento):
                tipo_peca = self._determinar_tipo_peca(y, x)
                peca_atual = self._gerenciador_prototipos.obter_peca_clonada(tipo_peca)
                peca_atual.set_posicao(y, x)
                grade_de_pecas[y][x] = peca_atual

                # Norte
                if y > 0:
                    vizinho_norte = grade_de_pecas[y-1][x]
                    encaixe_sul_vizinho = vizinho_norte.get_encaixe("sul")
                    fabrica_usada = self._fabricas_de_estilos[ (encaixe_sul_vizinho.get_tipo_id() // 2) -1 ]
                    
                    if isinstance(encaixe_sul_vizinho, Entrada):
                        peca_atual.set_encaixe("norte", fabrica_usada.criar_saida())
                    else:
                        peca_atual.set_encaixe("norte", fabrica_usada.criar_entrada())
                
                # Oeste
                if x > 0:
                    vizinho_oeste = grade_de_pecas[y][x-1]
                    encaixe_leste_vizinho = vizinho_oeste.get_encaixe("leste")
                    fabrica_usada = self._fabricas_de_estilos[ (encaixe_leste_vizinho.get_tipo_id() // 2) -1 ]

                    if isinstance(encaixe_leste_vizinho, Entrada):
                        peca_atual.set_encaixe("oeste", fabrica_usada.criar_saida())
                    else:
                        peca_atual.set_encaixe("oeste", fabrica_usada.criar_entrada())

                # Abaixo Leste e Sul
                for direcao in ["sul", "leste"]:
                    if peca_atual.get_encaixe(direcao) is None:
                        fabrica = random.choice(self._fabricas_de_estilos)
                        peca_atual.set_encaixe(direcao, random.choice([fabrica.criar_entrada(), fabrica.criar_saida()]))

        # Saída
        saidas_formatadas = []
        for y in range(self._altura):
            for x in range(self._comprimento):
                saidas_formatadas.append(grade_de_pecas[y][x].gerar_saida_formatada())
        
        return saidas_formatadas
