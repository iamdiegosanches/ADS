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

# --- Configuração do Problema  ---
lamb = 1.0
mu = 0.5 

def arrival_fn(k):
    if k <= 7:
        return 2.9187
    elif k == 8 or k == 9:
        return 0.8333
    else:
        return 0

def service_fn(k):
    return k * mu

# Execução
resultado = resolver_birth_death(10, arrival_fn, service_fn)

print("\n--- Resultados ---")
probs = resultado['probabilidades']
for k, p in enumerate(probs):
    print(f"P_{k} (Probabilidade de {k} jobs): {p:.4f} ({p*100:.2f}%)")

print("\nMétricas:")
for k, v in resultado['metrics'].items():
    print(f"{k}: {v:.4f}")