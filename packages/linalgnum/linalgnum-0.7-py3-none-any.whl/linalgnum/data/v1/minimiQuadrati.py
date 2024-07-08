import numpy as np
from sys import argv
import matplotlib.pyplot as plt


def formula_sistemi_lineari(x, y):
    n = len(x)
    A = np.vstack([x, np.ones(n)]).T
    return np.linalg.lstsq(A, y, rcond=None)[0]


# Metodo 1
def formula_diretta_qr(x, y):
    n = len(x)

    A = np.vstack([x ** 2, x, np.ones(n)]).T

    # decomposizione qr 

    Q, R = np.linalg.qr(A)

    return np.linalg.inv(R) @ Q.T @ y


# Metodo 2
def formula_diretta_regressione(x, y):
    n = len(x)

    A = np.vstack([x ** 2, x, np.ones(n)]).T

    # Formula diretta < concetto di regressione >
    # β = (X^T X)^-1 X^T Y
    return np.linalg.inv(A.T @ A) @ A.T @ y


# Metodo 3
def formula_diretta_pseudoinversa(x, y):
    n = len(x)

    A = np.vstack([x ** 2, x, np.ones(n)]).T

    return np.linalg.pinv(A) @ y


# Equazione Secondo Grado: ax^2 + bx + c
def polinomio_secondo_grado(a, b, c, x_values):
    return a * x_values ** 2 + b * x_values + c


# Equazione Primo Grado: ax + b
def polinomio_primo_grado(a, b, x_values):
    return a * x_values + b


def scarto_quadratico_medio(a, b, c, x, y):
    n = len(x)
    scarto_quadratico = np.sum((y - polinomio_secondo_grado(a, b, c, x)) ** 2)
    return np.sqrt(scarto_quadratico / n)


def scarto_quadratico_medio_with_coeff(coeff, x, y):
    n = len(x)
    scarto_quadratico = np.sum((y - np.polyval(coeff, x)) ** 2)
    return np.sqrt(scarto_quadratico / n)


# Funzione per calcolare i coefficienti del polinomio di grado n
def fit_polynomial(x, y, degree):
    # Calcoliamo la matrice di Vandermonde
    A = np.vander(x, degree + 1)
    # Risolviamo il sistema dei minimi quadrati
    #coeffs, residuals, rank, s = np.linalg.lstsq(A, y, rcond=None)
    coeffs = np.polyfit(x, y, deg=degree)
    return coeffs


def minimi_quadrati_prof(x,y,degree):
    coeffs = np.polyfit(x,y,deg = degree)
    print(f"Coefficienti polinomio di grado {degree}: {coeffs}\nScarto quadratico medio: {scarto_quadratico_medio(coeffs, x, y)}\n")

# INPUT #

input = argv[1]
if input == "26-06-2018":  # Tipo A: trovare retta + parabola
    # Punti dati
    x = np.array([-1, -0.5, 0, 0.25, 1])
    y = np.array([-0.125, -0.5, 0, 0.25, 1])
    x_val = np.linspace(-1.2, 1.2, 100)

    a_quad, b_quad, c_quad = formula_diretta_qr(x, y)
    a_liner, b_liner = formula_sistemi_lineari(x, y)

    print("Coeff con QR - Parabola - ")
    print("a: ", a_quad)
    print("b: ", b_quad)
    print("c: ", c_quad)

    print("\n")

    print("Coeff - Retta - ")
    print("a: ", a_liner)
    print("b: ", b_liner)

    y_val_quadratico = polinomio_secondo_grado(a_quad, b_quad, c_quad, x_val)
    y_val_lineare = polinomio_primo_grado(a_liner, b_liner, x_val)

    # plotting #
    plt.scatter(x, y, color="red")
    plt.plot(x_val, y_val_quadratico, "k-")
    plt.plot(x_val, y_val_lineare, "r-")

    plt.show()
elif input == "02-07-2019":  # Tibo B: Coeff + sistema.eq.normali + metodo risolutivo
    x = np.array([0, 1, 2, 4])
    y = np.array([4, 3, 2, 1])

    a, b, c = formula_diretta_qr(x, y)

    print("Coeff con QR")
    print("a: ", a)
    print("b: ", b)
    print("c: ", c)

    x_val = np.linspace(0, 4, 100)
    y_val = polinomio_secondo_grado(a, b, c, x_val)

    sigma = scarto_quadratico_medio(a, b, c, x, y)
    print("Scarto Quadratico Medio: ", sigma)

    # plotting # 
    plt.scatter(x, y, color="red")
    plt.plot(x_val, y_val, "k-")

    plt.show()
elif input == "12-07-2022":  # Tibo B: Coeff + sistema.eq.normali + metodo risolutivo
    x = np.array([0, 1, 2, 3])
    y = np.array([1, 1.5, 2.5, 5])

    a, b, c = formula_diretta_qr(x, y)

    print("Coeff con QR")
    print("a: ", a)
    print("b: ", b)
    print("c: ", c)

    x_val = np.linspace(0, 3, 100)
    y_val = polinomio_secondo_grado(a, b, c, x_val)

    sigma = scarto_quadratico_medio(a, b, c, x, y)
    print("Scarto Quadratico Medio: ", sigma)

    # plotting # 
    plt.scatter(x, y, color="red")
    plt.plot(x_val, y_val, "k-")

    plt.show()
elif input == "27-09-2022":  # Tibo B: Coeff + sistema.eq.normali + metodo risolutivo
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([0.5, 0, -0.5, 0.3, 2])

    coeff = formula_diretta_regressione(x, y)
    coeff2 = formula_diretta_pseudoinversa(x, y)
    coeff3 = formula_diretta_qr(x, y)
    a, b, c = coeff
    a2, b2, c2 = coeff2
    a3, b3, c3 = coeff3

    x_val = np.linspace(np.min(x), np.max(x) + .1, 100)
    y_val = polinomio_secondo_grado(a, b, c, x_val)

    poly = polinomio_secondo_grado(a, b, c, x)

    sigma = scarto_quadratico_medio(a, b, c, x, y)
    print("Scarto quadratico Medio: ", sigma)

    print("a: ", a)
    print("b: ", b)
    print("c: ", c)

    print("\n")

    print("Coeff con Pseudo Inversa")
    print("a: ", a2)
    print("b: ", b2)
    print("c: ", c2)

    print("\n")

    print("Coeff con Qr")
    print("a: ", a3)
    print("b: ", b3)
    print("c: ", c3)

    # plotting #
    plt.scatter(x, y, color="red")
    plt.plot(x_val, y_val, "k-")

    plt.show()
