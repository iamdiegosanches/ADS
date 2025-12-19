import math

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

# Executando com os valores do Problema 31.3
calcula_mm1(lamb=5/3, mu=2.0)

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


def calcula_mmmb(lamb, mu, m, B):
    rho = lamb / (m * mu)

    soma = sum((m * rho)**n / math.factorial(n) for n in range(m))
    soma += sum((m * rho)**m * rho**(n - m) / math.factorial(m) for n in range(m, B + 1))
    P0 = 1 / soma

    def Pn(n):
        if n < m:
            return P0 * (m * rho)**n / math.factorial(n)
        elif n <= B:
            return P0 * (m * rho)**m / math.factorial(m) * rho**(n - m)
        else:
            return 0

    PB = Pn(B)
    lamb_eff = lamb * (1 - PB)

    E_n = sum(n * Pn(n) for n in range(B + 1))
    E_nq = sum(max(0, n - m) * Pn(n) for n in range(B + 1))
    E_r = E_n / lamb_eff
    E_w = E_nq / lamb_eff

    print(f"\n--- M/M/{m}/B (B={B}) ---")
    print(f"rho = {rho:.4f}")
    print(f"P0 = {P0:.4f}")
    print(f"PB = {PB:.4f}")
    print(f"E[n] = {E_n:.4f}")
    print(f"E[nq] = {E_nq:.4f}")
    print(f"E[r] = {E_r:.4f}")
    print(f"E[w] = {E_w:.4f}")


def calcula_mmm():
    print("calcula teoria de filas mmm")

# Example of usage:
lamb = 5  # Arrival rate (jobs per unit time)
mu = 6  # Service rate (jobs per unit time)
B = 3  # Number of buffers in M/M/1/B queue

calcula_mm1(lamb, mu)
calcula_mM1B(lamb, mu, B)
calcula_mmm(lamb, mu, m=2)
calcula_mmmb(lamb, mu, m=2, B=5)
