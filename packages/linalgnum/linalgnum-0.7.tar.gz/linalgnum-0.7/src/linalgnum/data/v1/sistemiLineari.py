import numpy as np
from nptyping import NDArray
from numpy import abs, sum, dot, linalg, zeros


def check_square_matrix(A: NDArray) -> bool:
    # Controllo se la matrice è quadrata
    n, m = A.shape
    return n == m


def check_diagonal_dominant(A: NDArray) -> bool:
    # Controllo se la matrice è diagonale dominante: |a_ii| > sum(|a_ij|) per ogni i != j
    n, m = A.shape
    for i in range(n):
        if abs(A[i, i]) <= sum(abs(A[i, :])) - abs(A[i, i]):
            return False
    return True


# METODI DI ELIMINAZIONE DI GAUSS
def gauss_naive(A: NDArray, b: NDArray) -> NDArray:
    # Guass Naive, o metodo di eliminazione di Gauss, risolve un sistema lineare Ax = b
    # Controllo che A sia quadrata
    if not check_square_matrix(A):
        raise ValueError("Matrice A non quadrata, impossibile applicare il metodo")
    n = A.shape[0]
    x = zeros(n)
    for k in range(n - 1):
        for i in range(k + 1, n):
            # L'elemento pivot A[k][k] non deve essere nullo
            if A[k][k] == 0:
                raise ValueError("Elemento diagonale nullo")
            m = A[i][k] / A[k][k]
            for j in range(k + 1, n):
                A[i][j] -= m * A[k][j]
            b[i] -= m * b[k]
    # Esecuzione del passo di sostituzione all'indietro
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, (i + 1):n], x[(i + 1):n])) / A[i][i]
    return x


def gauss_seidel(A: NDArray, b: NDArray, x0: NDArray | None = None, tol: float = 1e-3, max_iter: int = 10000) -> (
        int, NDArray, list):
    # Gauss-Seidel, se converge, restituisce il numero di iterazioni, il vettore x e la lista dei residui
    # La matrice A deve essere quadrata per applicare il metodo
    if not check_square_matrix(A):
        raise ValueError("Matrice A non quadrata, impossibile applicare il metodo")
    # Condizione di convergenza: la matrice A deve essere diagonale dominante
    if not check_diagonal_dominant(A):
        print("Matrice A non diagonale dominante, il metodo POTREBBE non convergere")
    # Se x0 non è specificato, lo inizializzo a 0
    x = np.zeros_like(b) if x0 is None else x0.astype(float).copy()
    # Lista dei residui: ||b - Ax||
    residuals = []
    for curr_inter in range(1, max_iter + 1):
        for i in range(len(A)):
            s = 0
            for j in range(len(A)):
                if i != j:
                    s = s + A[i][j] * x[j]
            x[i] = (b[i] - s) / A[i][i]
        residual_norm = linalg.norm((b - dot(A, x)), 2)
        residuals.append(residual_norm)
        # Terminazione basata sul criterio del residuo
        if residual_norm < tol:
            return curr_inter, x, residuals
    return -1, np.array([]), []


def jacobi(A: NDArray, b: NDArray, x0: NDArray | None = None, tol: float = 1e-3, max_iter: int = 10000) -> (
        int, NDArray, list):
    # Jacobi, se converge, restituisce il numero di iterazioni, il vettore x e la lista dei residui
    # La matrice A deve essere quadrata per applicare il metodo
    if not check_square_matrix(A):
        raise ValueError("Matrice A non quadrata, impossibile applicare il metodo")
    # Condizione di convergenza: la matrice A deve essere diagonale dominante
    if not check_diagonal_dominant(A):
        print("Matrice A non diagonale dominante, il metodo POTREBBE non convergere")
    # Se x0 non è specificato, lo inizializzo a 0
    x = np.zeros_like(b) if x0 is None else x0.astype(float).copy()
    # Lista dei residui: ||b - Ax||
    residuals = []
    for curr_inter in range(1, max_iter + 1):
        prev_x = x
        for i in range(len(A)):
            s = 0
            for j in range(len(A)):
                if i != j:
                    s = s + A[i][j] * prev_x[j]
            x[i] = (b[i] - s) / A[i][i]
        residual_norm = linalg.norm((b - dot(A, x)), 2)
        residuals.append(residual_norm)
        # Terminazione basata sul criterio del residuo
        if residual_norm < tol:
            return curr_inter, x, residuals
    return -1, np.array([]), []


def jacobi_senza_b(A: NDArray) -> None:
    # Jacobi converge se la matrice di iterazione ha raggio spettrale minore di 1

    # Estraggo la matrice diagonale di A
    D = np.diag(np.diag(A))
    # Ottengo la matrice dei resti
    R = A - D
    # Eseguo la moltiplicazione riga per colonna per ottenere la matrice di iterazione
    iter_matrix = -np.linalg.inv(D) @ R
    # Calcolo gli autovalori della matrice di iterazione
    eigenvalues = np.linalg.eigvals(iter_matrix)
    # Trovo il raggio spettrale
    spectral_radius = np.round(max(abs(eigenvalues)), 2)
    print("Raggio spettrale: ", spectral_radius)
    print("Jacobi converge (RS < 1): ", spectral_radius < 1)

def gauss_seidel_senza_b(A: NDArray) -> None:
    # GS converge se la matrice di iterazione ha raggio spettrale minore di 1

    # Estraggo la matrice triangolare inferiore di A
    L = np.tril(A)
    # Ottengo il negativo della matrice per L
    U= A - L
    # Eseguo la moltiplicazione riga per colonna per ottenere la matrice di iterazione
    iter_matrix = -np.linalg.inv(L) @ U
    # Calcolo gli autovalori della matrice di iterazione
    eigenvalues = np.linalg.eigvals(iter_matrix)
    # Trovo il raggio spettrale
    spectral_radius = np.round(max(abs(eigenvalues)), 2)
    print("Raggio spettrale: ", spectral_radius)
    print("Gauss Seidel converge (RS < 1): ", spectral_radius < 1)


def tests():
    print("GAUSS NAIVE")
    A = np.array([[1.0, 1.0, 1.0], [1.0, -1.0, -1.0], [1.0, -2.0, 3.0]], dtype=float)
    A2 = A.copy()
    b = np.array([1.0, 1.0, -5.0], dtype=float)
    b2 = b.copy()
    x = gauss_naive(A, b)
    x_numpy = linalg.solve(A2, b2)
    print("Soluzione Gauss ", x)
    print("Soluzione Numpy ", x_numpy)
    print("JACOBI")
    a = np.array([[2.0, 0.0, 1.0, 0.0], [0.0, 2.0, 0.0, 0.0], [1.0, 0.0, 2.0, 1.0], [0.0, 0.0, 1.0, 1.0]], dtype=float)
    b = np.array([3.0, 2.0, 4.0, 2.0], dtype=float)
    x0 = np.array([0.0, 1.0, 0.0, 1.0], dtype=float)
    tol = 0.000001
    iterazioni, x, residui = jacobi(a, b, x0, tol)
    if iterazioni != -1:
        print("Jacobi converge in ", iterazioni, " iterazioni")
        print("Soluzione Jacobi ", x)
        print("Residui ", residui)
    else:
        print("Jacobi non converge")
    print("GAUSS-SEIDEL")
    a = np.array([[3.0, 0.0, 4.0], [7.0, 4.0, 2.0], [-1.0, -1.0, -2.0]], dtype=float)
    b = np.array([7.0, 13.0, -4.0], dtype=float)
    iterazioni, x, residui = gauss_seidel(a, b)
    if iterazioni != -1:
        print("Gauss-Seidel converge in ", iterazioni, " iterazioni")
        print("Soluzione Gauss-Seidel ", x)
        print("Residui ", residui)
    else:
        print("Gauss-Seidel non converge")

def main():
    print("Esame 27/10/2016")
    # Calcolare xk per k [0,10] e residui
    # In caso di soluzione esatta stampare |x_k - x| per k [0,10]
    A = np.array([[3, 0, 4], [7, 4, 2], [-1, -1, -2]], dtype=float)
    b = np.array([7, 13, -4], dtype=float)
    x0 = np.array([0, 0, 0], dtype=float)
    iterazioni, x, residui = gauss_seidel(A, b, x0, max_iter=10)
    if iterazioni != -1:
        print("Gauss-Seidel converge in ", iterazioni, " iterazioni")
        print("Soluzione Gauss-Seidel ", x)
        print("Residui ", residui)
    else:
        print("Gauss-Seidel non converge")
    iterazioni, x, residui = jacobi(A, b, x0, max_iter=10)
    if iterazioni != -1:
        print("Jacobi converge in ", iterazioni, " iterazioni")
        print("Soluzione Jacobi ", x)
        print("Residui ", residui)
    else:
        print("Jacobi non converge")
    print("Esame 11/07/2017")
    # Studiare la convergenza di Jacobi e Gauss-Seidel tramite raggio spettrale
    A = np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]], dtype=float)
    jacobi_senza_b(A)
    gauss_seidel_senza_b(A)


if __name__ == '__main__':
    # tests()
    main()

