import math
from decimal import Decimal, getcontext

def calcula_mm1(lamb, mu):
    # Calculate traffic intensity (rho)
    rho = lamb / mu

    # Calculate probability of 0 jobs in the system (P0)
    P0 = 1 - rho

    # Calculate probability of n jobs in the system (Pn)
    def Pn(n):
        return (1 - rho) * (rho ** n)

    # Mean number of jobs in the system (E[n])
    E_n = rho / (1 - rho)

    # Variance of number of jobs in the system (Var[n])
    Var_n = rho / (1 - rho)**2

    # Mean number of jobs in the queue (E[nq])
    E_nq = rho**2 / (1 - rho)

    # Mean response time (E[r]) - Tempo no sistema (Fila + Serviço)
    E_r = 1 / (mu * (1 - rho))

    # Mean waiting time (E[w]) - Tempo SOMENTE na fila (CORRIGIDO)
    # A fórmula anterior estava igual a E_r. A correta multiplica por rho.
    E_w = rho / (mu * (1 - rho)) 

    E_s = 1 / mu 

    percentil = 90
    q = percentil / 100.0
    # Fórmula: E[r] * ln(100 / (100-percentil))
    r_90 = E_r * math.log(1 / (1 - q))

    # Print the results in a formatted way
    print(f"--- M/M/1 Queue Calculations ---")
    print(f"Inputs: Lambda={lamb:.4f}, Mu={mu:.4f}")
    print(f"Traffic Intensity (rho): {rho:.4f}")
    print(f"Probability of 0 jobs (P0): {P0:.4f}")
    for n in range(5):
        print(f"Probability of {n} jobs (P{n}): {Pn(n):.4f}")
    print(f"Mean number of jobs in the system (E[n]): {E_n:.4f}")
    print(f"Variance of number of jobs in the system (Var[n]): {Var_n:.4f}")
    print(f"Mean number of jobs in the queue (E[nq]): {E_nq:.4f}")
    print(f"Mean response time (E[r]): {E_r:.4f} s")
    print(f"Mean waiting time (E[w]): {E_w:.4f} s")
    print(f"Mean service time (E[s]): {E_s:.4f} s")
    print(f"Tempo de resposta 90-percentil: {r_90:.4f} s")

def calcula_mmc(lamb, mu, c):
    # 1. Parâmetros Básicos
    u = lamb / mu           # Intensidade de Tráfego (em Erlangs)
    rho = u / c             # Utilização por servidor (rho < 1 para estabilidade)
    E_s = 1 / mu            # Tempo médio de serviço

    print(f"--- Sistema M/M/{c} ---")
    print(f"Inputs: Lambda={lamb}, Mu={mu}, c={c}")
    print(f"Utilização (rho): {rho:.2%}")

    if rho >= 1:
        print("SISTEMA INSTÁVEL (rho >= 1). Fila crescerá infinitamente.")
        return

    # 2. Cálculo de P0 (Probabilidade de Ociosidade)
    # Somatório dos primeiros termos (n=0 até c-1)
    soma_termos = sum([(u**n) / math.factorial(n) for n in range(c)])
    
    # Termo final da série (para n >= c)
    termo_final = (u**c) / (math.factorial(c) * (1 - rho))
    
    P0 = 1 / (soma_termos + termo_final)
    
    # 3. Probabilidade de Fila (Erlang-C)
    # Probabilidade de que um job que chega tenha que esperar
    P_wait = termo_final * P0 

    # 4. Métricas de Desempenho
    # Número médio na fila (E[nq] ou Lq)
    E_nq = (P_wait * rho) / (1 - rho)
    
    # Número médio no sistema (E[n] ou L) = Fila + Em Serviço
    # Média em serviço é u (lambda/mu)
    E_n = E_nq + u
    
    # Tempo médio de espera na fila (E[w] ou Wq)
    E_w = E_nq / lamb
    
    # Tempo médio de resposta (E[r] ou W) = Espera + Serviço
    E_r = E_w + E_s

    varho = (((c * rho)**c) / (math.factorial(c) * (1 - rho))) * P0

    var_r = (1/(mu**2))*(1 + ((varho * (2-varho))/(c**2 * (1-rho)**2)))

    # --- Impressão dos Resultados ---
    print(f"Utilização média dos discos (U): {rho:.4f}")
    print(f"Probabilidade de sistema ocioso (P0): {P0:.4f}")
    print(f"Probabilidade de ter que esperar (P_wait): {P_wait:.4f}")
    print(f"Número médio de jobs no sistema (E[n]): {E_n:.4f}")
    print(f"Tempo médio de resposta (E[r]): {E_r:.4f} s")
    print(f"Probabilidade de enfileramento: {varho:.4f} = {varho * 100} %")
    print(f"Variancia: {var_r:.4f} s^2")
    print(f"E_nq: {E_nq:.4f}")
    print(f"Tempo médio de espera na fila: {E_w:.4f}")


def calcula_mM1B(lamb, mu, B):
    # Calculate traffic intensity (rho)
    rho = lamb / mu

    # Calculate P0
    if rho != 1:
        P0 = (1 - rho) / (1 - rho**(B+1))
    else:
        P0 = 1 / (B + 1)

    # Calculate Pn
    def Pn(n):
        if n > B:
            return 0
        return (1 - rho) * (rho ** n) / (1 - rho**(B+1))

    # Mean number of jobs in the system (E[n])
    E_n = (rho / (1 - rho)) * ((B + 1) * (rho ** (B + 1)) / (1 - rho ** (B + 1)))

    # Mean number of jobs in the queue (E[nq])
    E_nq = (rho / (1 - rho)) * ((1 + B * (rho ** B)) / (1 - rho ** (B + 1)))

    # Effective arrival rate (lamb')
    lamb_prime = lamb * (1 - Pn(B))

    # Mean response time (E[r])
    E_r = E_nq / lamb_prime

    # Mean waiting time (E[w])
    E_w = E_r - 1 / mu

    # Print the results in a formatted way
    print(f"\n--- M/M/1/B Queue Calculations (B = {B}) ---")
    print(f"Traffic Intensity (rho): {rho:.4f}")
    print(f"Probability of 0 jobs (P0): {P0:.4f}")
    for n in range(5):
        print(f"Probability of {n} jobs (P{n}): {Pn(n):.4f}")
    print(f"Mean number of jobs in the system (E[n]): {E_n:.4f}")
    print(f"Mean number of jobs in the queue (E[nq]): {E_nq:.4f}")
    print(f"Effective arrival rate (lamb'): {lamb_prime:.4f}")
    print(f"Mean response time (E[r]): {E_r:.4f}")
    print(f"Mean waiting time (E[w]): {E_w:.4f}")


def calcula_mmm(lamb, mu, m):
    rho = lamb / (m * mu)
    if rho >= 1:
        print("Sistema instável (rho >= 1)")
        return

    # P0
    soma = sum((m * rho)**n / math.factorial(n) for n in range(m))
    termo = (m * rho)**m / (math.factorial(m) * (1 - rho))
    P0 = 1 / (soma + termo)

    def Pn(n):
        if n < m:
            return P0 * (m * rho)**n / math.factorial(n)
        else:
            return P0 * (m * rho)**m / math.factorial(m) * rho**(n - m)

    # Probabilidade de fila (ϱ do livro)
    Q = ((m * rho)**m / (math.factorial(m) * (1 - rho))) * P0

    E_nq = Q * rho / (1 - rho)
    E_n = m * rho + E_nq
    E_w = E_nq / lamb
    E_r = E_w + 1 / mu

    print(f"\n--- M/M/{m} ---")
    print(f"rho = {rho:.4f}")
    print(f"P0 = {P0:.4f}")
    for n in range(5):
        print(f"P{n} = {Pn(n):.4f}")
    print(f"E[n] = {E_n:.4f}")
    print(f"E[nq] = {E_nq:.4f}")
    print(f"E[r] = {E_r:.4f}")
    print(f"E[w] = {E_w:.4f}")

getcontext().prec = 1000
def calcula_mmmb(lamb, mu, m, B):
    # Convertendo para Decimal para evitar erro de overflow
    lamb = Decimal(lamb)
    mu = Decimal(mu)
    rho = lamb / (m * mu)
    
    # 1. Cálculo da Soma para P0
    soma = Decimal(0)
    
    # Parte 1: Somatório de 0 até m-1
    for n in range(m):
        # Usamos Decimal(math.factorial(n)) para o Python tratar como número exato
        termo = ((m * rho)**n) / Decimal(math.factorial(n))
        soma += termo

    # Parte 2: Somatório de m até B
    # Calculamos o termo base do fatorial de m uma vez só para economizar
    fatorial_m = Decimal(math.factorial(m))
    termo_base_m = ((m * rho)**m) / fatorial_m
    
    for n in range(m, B + 1):
        termo = termo_base_m * (rho**(n - m))
        soma += termo

    P0 = 1 / soma

    # 2. Função interna para Pn (adaptada para Decimal)
    def get_Pn(n):
        if n < m:
            return P0 * ((m * rho)**n) / Decimal(math.factorial(n))
        elif n <= B:
            return P0 * termo_base_m * (rho**(n - m))
        else:
            return Decimal(0)

    # 3. Cálculos Finais
    PB = get_Pn(B)
    lamb_eff = lamb * (1 - PB)

    # Nota: Converta n para Decimal nas multiplicações
    E_n = sum(Decimal(n) * get_Pn(n) for n in range(B + 1))
    E_nq = sum(max(Decimal(0), Decimal(n) - m) * get_Pn(n) for n in range(B + 1))
    
    # Evitar divisão por zero se lamb_eff for 0
    if lamb_eff > 0:
        E_r = E_n / lamb_eff
        E_w = E_nq / lamb_eff
    else:
        E_r = Decimal(0)
        E_w = Decimal(0)

    print(f"\n--- M/M/{m}/{B} ---")
    print(f"rho = {rho:.4f}")
    print(f"P0 = {P0:.4E}") # .4E usa notação científica se for muito pequeno
    print(f"PB = {PB:.4f}")
    print(f"E[n] = {E_n:.4f}")
    print(f"E[nq] = {E_nq:.4f}")
    print(f"E[r] = {E_r:.4f}")
    print(f"E[w] = {E_w:.4f}")


def calcula_mmm(lamb, mu, m):
    # 1. Parâmetros e Intensidade de Tráfego (rho)
    rho = lamb / (m * mu)
    
    # 3. Verificação de estabilidade
    if rho >= 1:
        print(f"--- M/M/{m} Queue ---")
        print(f"Sistema instável (rho = {rho:.4f} >= 1). A fila crescerá indefinidamente.")
        return

    # 4. Probabilidade de zero jobs no sistema (P0)
    # Soma dos termos onde n < m
    soma_inicial = sum(((m * rho)**n) / math.factorial(n) for n in range(m))
    # Termo onde n >= m
    termo_final = ((m * rho)**m) / (math.factorial(m) * (1 - rho))
    
    P0 = 1 / (soma_inicial + termo_final)

    # 6. Probabilidade de entrar na fila (varrho nas imagens)
    # P(>= m jobs)
    prob_queue = (((m * rho)**m) / (math.factorial(m) * (1 - rho))) * P0

    # 7. Número médio de jobs no sistema (E[n])
    E_n = (m * rho) + (rho * prob_queue) / (1 - rho)

    # 8. Variância do número de jobs no sistema (Var[n])
    # Termo entre colchetes da fórmula 8
    term_bracket = ((1 + rho - (rho * prob_queue)) / ((1 - rho)**2)) + m
    Var_n = (m * rho) + (rho * prob_queue * term_bracket)

    # 9. Número médio de jobs na fila (E[nq])
    E_nq = (rho * prob_queue) / (1 - rho)

    # 10. Variância do número de jobs na fila (Var[nq])
    Var_nq = (rho * prob_queue * (1 + rho - (rho * prob_queue))) / ((1 - rho)**2)

    # 11. Utilização média de cada servidor (U)
    U = rho # Conforme item 11 da imagem

    # 13. Tempo médio de resposta (E[r])
    # E[r] = (1/mu) * (1 + prob_queue / (m(1-rho)))
    E_r = (1 / mu) * (1 + prob_queue / (m * (1 - rho)))

    # 14. Variância do tempo de resposta (Var[r])
    term_var_r = (prob_queue * (2 - prob_queue)) / ((m**2) * ((1 - rho)**2))
    Var_r = (1 / (mu**2)) * (1 + term_var_r)

    # 16. Tempo médio de espera na fila (E[w])
    # E[w] = E[nq] / lambda = prob_queue / (m * mu * (1 - rho))
    E_w = prob_queue / (m * mu * (1 - rho))

    # 17. Variância do tempo de espera (Var[w])
    Var_w = (prob_queue * (2 - prob_queue)) / ((m**2) * (mu**2) * ((1 - rho)**2))

    # Função auxiliar para calcular Pn (Probabilidade de n jobs) - Item 5
    def get_Pn(n):
        if n < m:
            return P0 * ((m * rho)**n) / math.factorial(n)
        else:
            return P0 * ((m * rho)**m) / math.factorial(m) * (rho**(n - m))

    # Percentil 90 do tempo de espera (Item 19)
    # 90-Percentile = (E[w] / prob_queue) * ln(10 * prob_queue)
    if prob_queue > 0:
        percentile_90_w = (E_w / prob_queue) * math.log(10 * prob_queue)
    else:
        percentile_90_w = 0

    # Prints formatados
    print(f"\n--- M/M/{m} Queue Calculations ---")
    print(f"Inputs: Lambda={lamb:.4f}, Mu={mu:.4f}, m={m}")
    print(f"Traffic Intensity (rho): {rho:.4f}")
    print(f"Server Utilization (U): {U:.4f}")
    print(f"Probability of 0 jobs (P0): {P0:.4f}")
    print(f"Probability of queueing (varrho): {prob_queue:.4f}")
    
    print("-" * 30)
    for n in range(m + 4): # Mostra probabilidades até m+3
        print(f"Probability of {n} jobs (P{n}): {get_Pn(n):.4f}")
    print("-" * 30)
    
    print(f"Mean jobs in system (E[n]): {E_n:.4f}")
    print(f"Variance jobs in system (Var[n]): {Var_n:.4f}")
    
    print(f"Mean jobs in queue (E[nq]): {E_nq:.4f}")
    print(f"Variance jobs in queue (Var[nq]): {Var_nq:.4f}")
    
    print(f"Mean response time (E[r]): {E_r:.4f} s")
    print(f"Variance response time (Var[r]): {Var_r:.4f} s^2")
    
    print(f"Mean waiting time (E[w]): {E_w:.4f} s")
    print(f"Variance waiting time (Var[w]): {Var_w:.4f} s^2")
    print(f"90th Percentile waiting time: {percentile_90_w:.4f} s")

# Example of usage:
lamb = 0.1667  # Arrival rate (jobs per unit time)
c = 3
mu = 20  # Service rate (jobs per unit time)
B = 50  # Number of buffers in M/M/1/B queue (T-I)

#calcula_mm1(lamb=56.67, mu=100)
#calcula_mM1B(lamb, mu, B)
#calcula_mmc(lamb=0.1667, mu=0.1, c=5)
#calcula_mmm(lamb=0.6, mu=0.2, m=8)
calcula_mmmb(lamb=140, mu=(1/12), m=1612, B=1612)
