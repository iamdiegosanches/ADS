import numpy as np

def solve_linear_system(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    if np.linalg.det(A) == 0:
        raise ValueError("Sistema não possui solução única (matriz singular).")

    return np.linalg.solve(A, b) 


# --------------------- EXEMPLO DE USO ---------------------

A = [
    [1, 1, 1, 1, 1, 1],
    [0.6, -2, 0, 0, 1, 0],
    [1.4, 1, -2, 0, 0, 2],
    [0, 0.3, 0, -2, 0, 0],
    [0, 0.7, 0.3, 2, -2, 0],
    [0, 0, 0.7, 0, 1, -2]
]

b = [1, 0, 0, 0, 0, 0]

x = solve_linear_system(A, b)

print("Solução:")
print(x)

s = 0
for i in x:
    s += i

print(f"Soma = {s} \n")


print("Utilizações: \n")

print("Utilização Esteira:")
print(0.1890+0.1134+0.3780)

print("Utilização Bike:") # se tem 1 indivíduo tem que dividir a probabilidade por 2
print(0.1134/2 + 0.0170 + 0.1134/2)

print("Utilização Eliptico: ")
print(0.3780+0.1134+0.1890)

