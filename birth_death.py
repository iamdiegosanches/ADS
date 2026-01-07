def resolver_birth_death(capacidade_max, func_lambda, func_mu):
    coeficientes = [1.0]
    produtorio_atual = 1.0

    print(f"{'k':<5} | {'lambda(k-1)':<12} | {'mu(k)':<10} | {'Razão':<10}")
    print("-" * 45)

    for k in range(1, capacidade_max + 1):
        taxa_chegada_anterior = func_lambda(k - 1)
        taxa_servico_atual = func_mu(k)

        if taxa_servico_atual == 0:
            raise ValueError(f"A taxa de serviço (mu) no estado {k} não pode ser zero.")

        # Cálculo do produtório
        razao = taxa_chegada_anterior / taxa_servico_atual
        produtorio_atual *= razao
        coeficientes.append(produtorio_atual)
        
        print(f"{k:<5} | {taxa_chegada_anterior:<12} | {taxa_servico_atual:<10} | {razao:.4f}")

    # Normalização (P0)
    soma_coeficientes = sum(coeficientes)
    p0 = 1.0 / soma_coeficientes
    probabilidades = [coef * p0 for coef in coeficientes]

    # Métricas
    L = sum(k * p for k, p in enumerate(probabilidades))
    X = sum(func_mu(k) * probabilidades[k] for k in range(1, capacidade_max + 1))
    R = L / X if X > 0 else 0

    return {
        "probabilidades": probabilidades,
        "metrics": {"L": L, "X": X, "R": R}
    }

# --- Configuração do Problema M/M/2/3 ---
lamb = 1.0
mu = 1.0  # Taxa de UM servidor

def arrival_fn(k):
    return lamb

def service_fn(k):
    if k == 0: return 0.0
    if k == 1:
        return mu       # Apenas 1 servidor ativo
    else:
        return 2 * mu   # 2 servidores ativos (para k=2 e k=3)

# Execução
resultado = resolver_birth_death(3, arrival_fn, service_fn)

print("\n--- Resultados M/M/2/3 ---")
probs = resultado['probabilidades']
for k, p in enumerate(probs):
    print(f"P_{k} (Probabilidade de {k} jobs): {p:.4f} ({p*100:.2f}%)")

print("\nMétricas:")
for k, v in resultado['metrics'].items():
    print(f"{k}: {v:.4f}")