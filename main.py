# from orquestrador import GeradorQuebraCabeca # (Em arquivo separado)

def main():
    print("--- Gerador de Formato de Quebra-Cabeça ---")
    try:
        altura = int(input("Digite a altura do quebra-cabeça: "))
        comprimento = int(input("Digite o comprimento do quebra-cabeça: "))
        qtd_estilos = int(input("Digite a quantidade de estilos de encaixe: "))

        if altura <= 0 or comprimento <= 0 or qtd_estilos <= 0:
            print("\nErro: Todos os valores devem ser números inteiros positivos.")
            return

        gerador = GeradorQuebraCabeca(altura, comprimento, qtd_estilos)
        
        print("\nGerando especificações...")
        especificacoes = gerador.gerar_grade_de_pecas()

        print("\n--- Saída para Máquina de Corte ---")
        print("Formato: y,x-Norte,Oeste,Leste,Sul")
        for linha in especificacoes:
            print(linha)

    except ValueError:
        print("\nErro: Por favor, insira apenas números inteiros válidos.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()
  
