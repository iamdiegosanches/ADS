import numpy as np
import matplotlib.pyplot as plt

def erlang_b_vetorizado(m_max, A):
    """
    Calcula Erlang B para todos os valores de m de 0 até m_max.
    Retorna um array onde o índice é o número de servidores.
    """
    B_values = np.zeros(m_max + 1)
    B_values[0] = 1.0
    
    current_B = 1.0
    for m in range(1, m_max + 1):
        # Fórmula recursiva: B(m, A) = (A * B(m-1)) / (m + A * B(m-1))
        current_B = (A * current_B) / (m + A * current_B)
        B_values[m] = current_B
        
    return B_values

def plotar_grafico_exato():
    # --- Dados ---
    lamb = 140
    
    # Cargas
    A1 = lamb * 12  # 1680 Erlangs
    A2 = lamb * 18  # 2520 Erlangs
    
    # Definir intervalo do gráfico
    m_min, m_max = 1400, 2700
    m_range = np.arange(m_min, m_max)
    
    # Calcular probabilidades EXATAS para todo o intervalo
    # Calculamos até o m_max necessário
    pb_todos_12 = erlang_b_vetorizado(m_max, A1)
    pb_todos_18 = erlang_b_vetorizado(m_max, A2)
    
    # Recortar apenas a parte que queremos plotar
    pb_12 = pb_todos_12[m_min:m_max]
    pb_18 = pb_todos_18[m_min:m_max]
    
    # --- Plotagem ---
    plt.figure(figsize=(10, 6))
    
    plt.plot(m_range, pb_12, label=f'E[s]=12 min (A={A1})', color='blue', linewidth=2)
    plt.plot(m_range, pb_18, label=f'E[s]=18 min (A={A2})', color='red', linewidth=2)
    
    # Linhas de referência
    plt.axvline(x=1500, color='gray', linestyle='--', label='Atual (m=1500)')
    plt.axhline(y=0.05, color='green', linestyle=':', label='Meta 5%')
    
    # Destaque do ponto atual
    pb_atual = pb_todos_12[1500]
    plt.plot(1500, pb_atual, 'bo')
    plt.annotate(f'{pb_atual:.2%}', (1500, pb_atual), textcoords="offset points", xytext=(10,10), ha='center')

    plt.title('Probabilidade de Bloqueio (Erlang B) vs Número de Modems')
    plt.xlabel('Número de Modems')
    plt.ylabel('Probabilidade de Bloqueio')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig('Figure_1.png')
    plt.show()

plotar_grafico_exato()