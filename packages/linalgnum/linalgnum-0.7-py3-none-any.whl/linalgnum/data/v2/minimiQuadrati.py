# MINIMI QUADRATI 
# -> Interpolazione polinomio di grado n, con nodi m > n 

import numpy as np
import matplotlib.pyplot as plt

def scarto_quadratico_medio(coeff, x, y):
    n = len(x)
    scarto_quadratico = np.sum((y - np.polyval(coeff,x))**2)
    return np.sqrt(scarto_quadratico/n)

# Funzione per calcolare i coefficienti del polinomio di grado n
def fit_polynomial(x, y, degree):
    # Calcoliamo la matrice di Vandermonde
    A = np.vander(x, degree + 1)
    # Risolviamo il sistema dei minimi quadrati
    #coeffs, residuals, rank, s = np.linalg.lstsq(A, y, rcond=None)
    coeffs= np.polyfit(x,y,deg = degree)
    return coeffs

# Generiamo i dati (xk, yk) con una perturbazione di sin(x) nell'intervallo [0, 2π]
np.random.seed(42)  # Per la riproducibilità
x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x) + 0.1 * np.random.randn(100)  # Aggiungiamo una piccola perturbazione

# Calcoliamo i coefficienti per gradi da 1 a 8
polynomial_coeffs = {}
scarti_quadratici_medi = []
for n in range(1, 9):
    #coeffs = fit_polynomial(x, y, n)
    coeffs = np.polyfit(x,y,deg = n)
    polynomial_coeffs[n] = coeffs
    scarti_quadratici_medi.append(scarto_quadratico_medio(coeffs, x, y))
    print(f"Coefficienti polinomio di grado {n}: {coeffs}\nScarto quadratico medio: {scarto_quadratico_medio(coeffs, x, y)}\n")

# Visualizziamo i risultati
plt.figure(figsize=(14, 10))
plt.plot(x, y, 'o', label='Punti')
x_fit = np.linspace(0, 2 * np.pi, 100)
for n in range(1, 9):
    coeffs = polynomial_coeffs[n]
    y_fit = np.polyval(coeffs, x_fit)
    plt.plot(x_fit, y_fit, label=f'Polynomial degree {n}')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Interpolazione tramite Minimi Quadrati con diversi gradi')
plt.show()