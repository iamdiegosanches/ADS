import numpy as np

mu_cpu = 6.0
mu_fast = 4.0
mu_slow = 2.0

rate_cpu_to_fast = mu_cpu * 0.5
rate_cpu_to_slow = mu_cpu * 0.5

states = [
    (4,0,0),
    (3,1,0),
    (3,0,1),
    (2,2,0),
    (2,1,1),
    (2,0,2),
    (1,3,0),
    (1,2,1),
    (1,1,2),
    (1,0,3),
    (0,4,0),
    (0,3,1),
    (0,2,2),
    (0,1,3),
    (0,0,4)
]

dim = len(states)
A = np.zeros((dim, dim))
B = np.zeros(dim)

def get_idx(s):
    if s in states:
        return states.index(s)
    return None

for i, (c, f, s) in enumerate(states):
    
    rate_out = 0
    if c > 0: rate_out += mu_cpu
    if f > 0: rate_out += mu_fast
    if s > 0: rate_out += mu_slow
    
    A[i, i] = rate_out

    if c < 4 and f > 0:
        prev = (c+1, f-1, s)
        idx_prev = get_idx(prev)
        if idx_prev is not None:
            A[i, idx_prev] -= rate_cpu_to_fast

    if c < 4 and s > 0:
        prev = (c+1, f, s-1)
        idx_prev = get_idx(prev)
        if idx_prev is not None:
            A[i, idx_prev] -= rate_cpu_to_slow

    if c > 0 and f < 4:
        prev = (c-1, f+1, s)
        idx_prev = get_idx(prev)
        if idx_prev is not None:
            A[i, idx_prev] -= mu_fast # Subtrai taxa 4

    if c > 0 and s < 4:
        prev = (c-1, f, s+1)
        idx_prev = get_idx(prev)
        if idx_prev is not None:
            A[i, idx_prev] -= mu_slow


A[dim-1, :] = 1
B[dim-1] = 1

P = np.linalg.solve(A, B)

U_cpu = sum(P[i] for i, s in enumerate(states) if s[0] > 0)

X0 = U_cpu * mu_cpu

N = 4
R_min = N / X0
R_sec = R_min * 60

print("-" * 30)
print(f"{'Estado':<12} | {'Probabilidade':<10}")
print("-" * 30)
for i, prob in enumerate(P):
    print(f"{str(states[i]):<12} | {prob:.4f}")
print("-" * 30)
print(f"Utilização da CPU (U_cpu): {U_cpu:.4f} ({U_cpu*100:.1f}%)")
print(f"Throughput (X0):           {X0:.4f} tpm")
print(f"Tempo de Resposta (R):     {R_sec:.2f} segundos")
