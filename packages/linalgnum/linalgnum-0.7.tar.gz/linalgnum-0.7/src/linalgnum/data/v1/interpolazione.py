import numpy as np
from nptyping import NDArray
from numpy import abs, sum, dot, linalg, zeros
import matplotlib.pyplot as plt


def check_square_matrix(A: NDArray) -> bool:
    # Controllo se la matrice è quadrata
    n, m = A.shape
    return n == m


def gauss_naive(x_points: NDArray, y_points: NDArray):
    # Il metodo di Gauss Naive risolve sistemi lineari. Trova i coefficienti del polinomio interpolante.

    # Creo la matrice di Vandermonde tramite la libreria numpy
    vander = np.vander(x_points, increasing=True)

    vander_copy = vander.copy()
    y_points_copy = y_points.copy()
    coeff_numpy = linalg.solve(vander_copy, y_points_copy)

    # La matrice A deve essere quadrata per applicare il metodo
    if not check_square_matrix(vander):
        raise ValueError("Matrice non quadrata, impossibile applicare il metodo")
    n = vander.shape[0]
    coeff = np.zeros(n)
    for k in range(n - 1):
        for i in range(k + 1, n):
            if vander[k][k] == 0:  # Controllo se l'elemento pivot è nullo
                raise ValueError("Elemento pivot nullo")
            m = vander[i][k] / vander[k][k]
            for j in range(k + 1, n):
                vander[i][j] -= m * vander[k][j]
            y_points[i] -= m * y_points[k]

    # Esecuzione del passo di sostituzione all'indietro
    for i in range(n - 1, -1, -1):
        coeff[i] = (y_points[i] - dot(vander[i, (i + 1):n], coeff[(i + 1):n])) / vander[i][i]

    return coeff, coeff_numpy


def coef_diff_div(_x: NDArray, _y: NDArray):
    n = len(_x)
    coef = np.zeros([n, n])
    coef[:, 0] = _y.copy()
    for j in range(1, n):
        for i in range(n - j):
            coef[i][j] = (coef[i + 1][j - 1] - coef[i][j - 1]) / (_x[i + j] - _x[i])
    return coef[0, :]


def newton_diff_div(coef: NDArray, x: NDArray, x_new: NDArray) -> float:
    n = len(x)
    p = coef[n - 1]
    for i in range(1, n + 1):
        p = coef[n - i] + (x_new - x[n - i]) * p
    return p


def compute_lagrange(x_val, _x, _i):
    n = len(_x)
    temp_value = 1.0
    for j in range(n):
        if _i != j:
            temp_value *= (x_val - _x[j]) / (_x[_i] - _x[j])
    return temp_value


def interp_lagrange(x_val, _x, _y):
    n = len(_x)
    value = 0.0
    if len(_y) != n:
        return
    for i in range(n):
        value += _y[i] * compute_lagrange(x_val, _x, i)
    return value


def main():
    print("Interpolazione con coefficienti indeterminati con Vandermonde-Gauss")
    x = np.array([-2, -1, 1, 3], dtype=float)  # ---> n punti => polinomio grado n-1
    y = np.array([4, 3, 2, 1], dtype=float)
    coeff, coeff_numpy = gauss_naive(x, y)

    print("Coefficients Gauss Naive: ", coeff)
    print("Coefficients Numpy: ", coeff_numpy)

    print("Interpolazione con Differenze Divise-Newton")
    coeff_numpy = np.polyfit(x, y, x.shape[0] - 1)
    x_space = np.linspace(np.min(x), np.max(x), 100)
    y_space_numpy = np.polyval(coeff_numpy, x_space)

    coeff_newton = coef_diff_div(x, y)
    y_space_newton = np.zeros(len(x_space))
    for i, value in enumerate(x_space):
        y_space_newton[i] = newton_diff_div(coeff_newton, x, value)
    print("Interpolazione con Lagrange")
    coeff_numpy = np.polyfit(x, y, x.shape[0] - 1)
    x_space = np.linspace(np.min(x), np.max(x), 100)
    y_space_numpy = np.polyval(coeff_numpy, x_space)

    y_space_lagrange = np.zeros(len(x_space))
    for i, value in enumerate(x_space):
        y_space_lagrange[i] = interp_lagrange(value, x, y)
    plt.plot(x, y, 'o')
    plt.plot(x_space, y_space_numpy, label="Numpy")
    plt.plot(x_space, y_space_newton, label="Newton")
    plt.plot(x_space, y_space_lagrange, label="Lagrange")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()