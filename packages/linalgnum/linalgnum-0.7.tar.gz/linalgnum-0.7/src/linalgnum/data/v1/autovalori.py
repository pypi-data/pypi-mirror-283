import numpy as np
import matplotlib.pyplot as plt
from nptyping import NDArray
from numpy import abs, sum, dot, linalg, zeros


def check_square_matrix(A: NDArray) -> bool:
    # Controllo se la matrice è quadrata
    n, m = A.shape
    return n == m


# GERSCHGORIN
def gersh_disks(A: NDArray):
    # Localizza gli autovalori di una matrice A attraverso i cerchi di Gershgorin
    # La matrice A deve essere quadrata per applicare il metodo
    if not check_square_matrix(A):
        raise ValueError("Matrice A non quadrata, impossibile applicare il metodo")
    n = A.shape[0]
    # Contenitore dei cerchi di Gershgorin
    # Disco: <centro, raggio>
    disks = []
    for i in range(n):
        center = A[i][i]
        # Raggio del cerchio di Gershgorin
        radius = sum([abs(A[i][j]) for j in range(n) if i != j])
        disks.append((center, radius))
    numpy_ev = np.linalg.eigvals(A)
    print("Cerchi di Gershgorin: ", disks)
    print("Autovalori calcolati con numpy: ", numpy_ev)
    # Visualizzazione grafica dei cerchi di Gershgorin
    plt.figure()
    plt.grid(True)
    plt.axis('equal')
    plt.title('Cerchi di Gershgorin')
    plt.xlabel('Re')
    plt.ylabel('Im')
    # Definizione dei cerchi
    x_axis = np.linspace(0, 2 * np.pi, 100)  # Pi-greco
    i = np.exp(1j * x_axis)  # 1j => l'unità immaginaria
    for k in range(len(disks)):
        c_k = disks[k][0] + disks[k][1] * i
        plt.fill(np.real(c_k), np.imag(c_k), color=[0.8, 0.8, 0.8])
        plt.plot(np.real(c_k), np.imag(c_k), 'k-', np.real(disks[k][0]), np.imag(disks[k][0]), 'kx')
    # Definizione degli autovalori
    plt.plot(np.real(numpy_ev), np.imag(numpy_ev), 'ro', label='Autovalori NumPy')
    plt.legend()
    plt.show()


def power_method(A: NDArray, x0: NDArray | None = None, tol: float = 1e-3, max_iter: int = 1000):
    # Il metodo delle potenze è un metodo iterativo per calcolare il valore assoluto del più grande autovalore e il corrispondente autovettore

    def calc_eig_items(x: NDArray):
        # Calcola autovalore e autovettore
        vector = x / linalg.norm(x, 2)
        value = dot(vector.T, dot(A, vector))
        return vector, value

    x0 = x0 if x0 is not None else np.random.rand(A.shape[0])
    # Approssimazione iniziale
    vector, value = calc_eig_items(x0)
    for curr_iter in range(1, max_iter):
        old_value = value
        x = dot(A, vector)
        vector, value = calc_eig_items(x)
        # Calcolo errore
        error = np.abs(1 - value / old_value)
        if error < tol:
            return curr_iter, vector, value
    return -1, None, None

def power_method_inv(A: NDArray, x0: NDArray | None = None, tol: float = 1e-3, max_iter: int = 1000):
    # Il metodo delle potenze inverso è un metodo iterativo per calcolare il valore assoluto del più piccolo autovalore e il corrispondente autovettore

    def calc_eig_items(x: NDArray):
        # Calcola autovalore e autovettore
        vector = x / linalg.norm(x, 2)
        value = dot(vector.T, dot(linalg.inv(A), vector))
        return vector, value

    x0 = x0 if x0 is not None else np.random.rand(A.shape[0])
    # Approssimazione iniziale
    vector, value = calc_eig_items(x0)
    for curr_iter in range(1, max_iter):
        old_value = value
        x = dot(linalg.inv(A), vector)
        vector, value = calc_eig_items(x)
        # Calcolo errore
        error = abs(1 - value / old_value)
        if error < tol:
            return curr_iter, vector, value
    return -1, None, None

def main():
    print("Ricerca dei cerchi Gershgorin e confronto con gli autovalori calcolati con NumPy")
    A = np.array([[8, -2, 1, 0], [-2, 2, -1, 1], [1, -1, 3, -1], [0, 1, -1, -5]], dtype=float)
    gersh_disks(A)
    print("Approssimazione autovalore massimo e autovettore")
    x0 = np.array([1, 1, 1, 1], dtype=float)
    Ab = np.dot(A.T, A)
    tol = 1e-4
    interazioni, power_vector, power_value = power_method(Ab, x0, tol)
    numpy_value, numpy_vector = np.linalg.eig(Ab)
    if interazioni != -1:
        print(f"Numero di iterazioni: {interazioni}")
        print(f"Massimo Autovettore Approssimato: {power_vector}")
        print(f"Autovettori Numpy: {numpy_vector}")
        print(f"Massimo Autovalore Approssimato: {power_value}")
        print(f"Autovalori Numpy: {numpy_value}")
    else:
        print("Il metodo non converge")
    print("Approssimazione autovalore minimo e autovettore")
    x0 = np.array([1, 1, 1, 1], dtype=float)
    Ab = np.dot(A.T, A)
    tol = 1e-4
    interazioni, power_vector, power_value = power_method_inv(Ab, x0, tol)
    numpy_value, numpy_vector = np.linalg.eig(Ab)
    if interazioni != -1:
        print(f"Numero di iterazioni: {interazioni}")
        print(f"Minimo Autovettore Approssimato: {power_vector}")
        print(f"Autovettori Numpy: {numpy_vector}")
        print(f"Minimo Autovalore Approssimato: {power_value}")
        print(f"Autovalori Numpy: {numpy_value}")
    else:
        print("Il metodo non converge")

if __name__ == '__main__':
    main()