import numpy as np

def solve_linear_system(A, b):
    """
    Resolve um sistema linear A x = b
    usando o solver numérico do NumPy.

    Parâmetros:
        A (array NxN): matriz de coeficientes
        b (array N): vetor do lado direito

    Retorna:
        x (array N): solução do sistema
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    # Detecta e trata casos degenerados
    if np.linalg.det(A) == 0:
        raise ValueError("Sistema não possui solução única (matriz singular).")

    return np.linalg.solve(A, b)


# --------------------- EXEMPLO DE USO ---------------------

A = [
    [1, 1, 1, 1, 1, 1],
    [0.6, -2, 0, 0, 1, 0],
    [1.4, 1, -2, 0, 0, 1],
    [0, 0.3, 0, -2, 0, 0],
    [0, 0.7, 0.3, 2, -2, 0],
    [0, 0, 0.7, 0, 1, -2]
]

b = [1, 0, 0, 0, 0, 0]

x = solve_linear_system(A, b)

print("Solução:")
print(x)
