import numpy as np
import os

def carregar_e_resolver(arquivo_txt):
    if not os.path.exists(arquivo_txt):
        print(f"Erro: O arquivo '{arquivo_txt}' não foi encontrado.")
        return

    try:
        matriz_completa = np.loadtxt(arquivo_txt)
        
        # A recebe todas as linhas (:) e todas as colunas exceto a última (:-1)
        A = matriz_completa[:, :-1]
        
        # b recebe todas as linhas (:) e apenas a última coluna (-1)
        b = matriz_completa[:, -1]

        # Verifica singularidade
        if np.linalg.det(A) == 0:
            raise ValueError("A matriz é singular (determinante zero). Não há solução única.")

        x = np.linalg.solve(A, b)
        return x

    except ValueError as ve:
        print(f"Erro nos dados: {ve}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


nome_do_arquivo = 'system.txt'
resultado = carregar_e_resolver(nome_do_arquivo)

if resultado is not None:
    print("--- Matriz lida e sistema resolvido ---")
    
    print("\nSolução (x):")

    np.set_printoptions(precision=4, suppress=True) 
    print(resultado)

    soma = np.sum(resultado)
    print(f"\nSoma dos elementos = {soma:.4f}")