import unittest
import collections
from typing import List, Dict

from orquestrador import GeradorQuebraCabeca

def _parse_saida(saida_formatada: List[str], altura: int, comprimento: int) -> List[List[Dict]]:

    if not saida_formatada:
        return []
        
    grade = [[None for _ in range(comprimento)] for _ in range(altura)]
    for linha in saida_formatada:
        pos, encaixes_str = linha.split('-')
        y, x = map(int, pos.split(','))
        n, o, l, s = map(int, encaixes_str.split(','))
        grade[y][x] = {
            "y": y, "x": x,
            "norte": n, "oeste": o, "leste": l, "sul": s
        }
    return grade

# Testes

class TestGeradorQuebraCabeca(unittest.TestCase):

    def setUp(self):
        self.altura = 10
        self.comprimento = 10
        self.qtd_estilos = 3
        self.gerador = GeradorQuebraCabeca(self.altura, self.comprimento, self.qtd_estilos)
        self.saida_formatada = self.gerador.gerar_grade_de_pecas()
        self.grade_analisavel = _parse_saida(self.saida_formatada, self.altura, self.comprimento)

    def test_garantir_distribuicao_de_estilos(self):
        #Teste 1: Garante que a distribuição de estilos de encaixe é balanceada.

        contagem_estilos = collections.defaultdict(int)
        total_conexoes_internas = 0

        for peca in self.saida_formatada:
            _, encaixes_str = peca.split('-')
            for encaixe_id in map(int, encaixes_str.split(',')):
                if encaixe_id > 0: 
                    estilo_id = (encaixe_id - 1) // 2 + 1
                    contagem_estilos[estilo_id] += 1
                    total_conexoes_internas += 1
        
        total_conexoes_unicas = total_conexoes_internas // 2
        media_esperada = total_conexoes_unicas / self.qtd_estilos

        for estilo, contagem in contagem_estilos.items():
            self.assertAlmostEqual(contagem / 2, media_esperada, delta=2,
                                   msg=f"Estilo {estilo} tem distribuição desbalanceada.")

    def test_garantir_distribuicao_entradas_e_saidas(self):
        #Teste 2: Garante que a distribuição de entradas (ímpar) e saídas (par) é balanceada.

        entradas = 0
        saidas = 0
        for peca_str in self.saida_formatada:
            _, encaixes_str = peca_str.split('-')
            for encaixe_id in map(int, encaixes_str.split(',')):
                if encaixe_id > 0:
                    if encaixe_id % 2 != 0:
                        entradas += 1
                    else:
                        saidas += 1
        
        self.assertEqual(entradas, saidas, msg="O número de entradas e saídas não é igual.")

    def test_garantir_que_os_encaixes_encaixam(self):
        #Teste 3: Garante que peças vizinhas se encaixam corretamente.

        y_rand, x_rand = (self.altura // 2, self.comprimento // 2)
        peca_atual = self.grade_analisavel[y_rand][x_rand]

        # testa com o vizinho norte de cima 
        vizinho_norte = self.grade_analisavel[y_rand - 1][x_rand]
        encaixe_norte_atual = peca_atual['norte']
        encaixe_sul_vizinho = vizinho_norte['sul']
        self.assertEqual(abs(encaixe_norte_atual - encaixe_sul_vizinho), 1,
                         msg="Encaixe Norte-Sul não é complementar.")

        # testa com o vizinho oeste esquerda 
        vizinho_oeste = self.grade_analisavel[y_rand][x_rand - 1]
        encaixe_oeste_atual = peca_atual['oeste']
        encaixe_leste_vizinho = vizinho_oeste['leste']
        self.assertEqual(abs(encaixe_oeste_atual - encaixe_leste_vizinho), 1,
                         msg="Encaixe Oeste-Leste não é complementar.")

    def test_garantir_quantidade_ideal_de_pecas_por_tipo(self):
        #Teste 4: Garante que a quantidade de peças de canto, borda e meio está correta.

        contagem = {'canto': 0, 'borda': 0, 'meio': 0}
        for peca_str in self.saida_formatada:
            _, encaixes_str = peca_str.split('-')
            zeros = encaixes_str.count('0')
            if zeros == 2:
                contagem['canto'] += 1
            elif zeros == 1:
                contagem['borda'] += 1
            elif zeros == 0:
                contagem['meio'] += 1
        
        cantos_esperados = 4
        bordas_esperadas = 2 * (self.altura - 2) + 2 * (self.comprimento - 2)
        meio_esperado = (self.altura - 2) * (self.comprimento - 2)

        self.assertEqual(contagem['canto'], cantos_esperados, msg="Número incorreto de peças de canto.")
        self.assertEqual(contagem['borda'], bordas_esperadas, msg="Número incorreto de peças de borda.")
        self.assertEqual(contagem['meio'], meio_esperado, msg="Número incorreto de peças de meio.")

    def test_garantir_que_peca_do_meio_nao_tem_lados_retos(self):
        # Teste 5: Garante que uma peça do meio não tem encaixes do tipo 0.

        peca_meio = self.grade_analisavel[self.altura // 2][self.comprimento // 2]
        
        self.assertNotIn(0, [peca_meio['norte'], peca_meio['oeste'], peca_meio['leste'], peca_meio['sul']],
                         msg="Uma peça do meio não deveria ter lados retos (tipo 0).")

if __name__ == '__main__':
    unittest.main(verbosity=2)
