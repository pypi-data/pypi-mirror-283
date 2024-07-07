'''
Esercizio tipico sull'integrazione:
Si vuole stimare un integrale in \[a,b]  di una certa funzione f(x), imponendo una soglia di errore/precisione oppure un limite sul numero di intervalli N da utilizzare
Si chiede l'utilizzo di un preciso metodo di approssimazione (Simpson, Trapezi, etc...)
'''

import numpy as np
import sympy as sp
from scipy.integrate import quad

# Trapezi
def trapezi_compositi(f, a, b, max_iter, tol):
    for z in range(1, max_iter):
        n = z
        h = (b - a)/(n)
        x = np.linspace(a, b, n + 1)
        fx = f(x)
        integral_apx = h/2*(fx[0] + 2*np.sum(fx[1:n]) + fx[n]) # raccolta per h/2 COMPOSITI

        valesatto = quad(f, a, b)[0]
        err=float(abs(valesatto-integral_apx))
        
        
        if err< tol:
            print(f"Il numero di nodi necessari affinché l'errore assoluto, con il metedo dei trapezi, sia minore della tolleranza {tol} è: "+str(n + 1))
            print("Il valore approssimato dell'integrale è "+str(integral_apx))
            print("L'errore assoluto vale " +str(err))
            break
    return 0

# Simpson
def simpson_composito(f, a, b, max_iter, tol):
    for z in range(1, max_iter):
        n = z
        h = (b - a) / n 
        x = np.linspace(a, b, n + 1)

        integral_apx = 0.0
                
        for i in range(n):
            integral_apx += (f(x[i]) + f(x[i+1]) + 4* f((x[i] + x[i+1])/2.0)) / 6.0
        integral_apx *= h

        valesatto = quad(f, a, b)[0]
        err=float(abs(valesatto-integral_apx))
    
        if err< tol:
            print(f"Il numero di nodi necessari affinché l'errore assoluto, con il metedo di simpson sia minore della tolleranza {tol} è: "+str(n -2))
            print("Il valore approssimato dell'integrale è "+str(integral_apx))
            print("L'errore assoluto vale " +str(err))
            break
    return 0

# Simpson CON N FISSO
def simpson_composito_nfisso(f, a, b, n, tol):
        
        h = (b - a) / n 
        x = np.linspace(a, b, n + 1)
        integral_apx = 0.0
        for i in range(n):
            integral_apx += (f(x[i]) + f(x[i+1]) + 4* f((x[i] + x[i+1])/2.0)) / 6.0
        integral_apx = integral_apx*h
        valesatto = quad(f, a, b)[0]
        
        err=float(abs(valesatto-integral_apx))
        print(integral_apx)
    
        if err <= tol and err > 0:
            print(f"Il numero di nodi necessari affinché l'errore assoluto, con il metedo di simpson sia minore della tolleranza {tol} è: "+str(n))
            print("Il valore approssimato dell'integrale è "+str(integral_apx))
            print("L'errore assoluto vale " +str(err))
            print("Valore calcolato soprastimato")
        elif err <= tol and err < 0:
            print(f"Il numero di nodi necessari affinché l'errore assoluto, con il metedo di simpson sia minore della tolleranza {tol} è: "+str(n))
            print("Il valore approssimato dell'integrale è "+str(integral_apx))
            print("L'errore assoluto vale " +str(err))
            print("Valore calcolato sottostimato")
        elif err <= tol and err == 0:
            print(f"Il numero di nodi necessari affinché l'errore assoluto, con il metedo di simpson sia minore della tolleranza {tol} è: "+str(n))
            print("Il valore approssimato dell'integrale è "+str(integral_apx))
            print("L'errore assoluto vale " +str(err))
            print("Valore esatto")
        return 0

# Error bound Simspon CON FORMULA ERRORE DI QUADRATURA DA ADATTARE
def err_bound_DA_SPECIFICARE(df4, a, b):
    h = (b - a)**5/2880
    max_f4 = max([df4.subs(x, x_val) for x_val in range(a, b +1)])
    result = abs(-h * max_f4)
    return result


#ESEMPIO DATI INPUT 

f = lambda x: x * np.exp(-4*x)
    
# parametri
a = 0
b = 1
tol = 1e-3

#con sympy
# derivata 4 
x = sp.symbols("x")
y = sp.log(x)
df4 = sp.diff(y,x, 4)

#intervalli N FISSO
n1 = 10 
n2 = 20 
n3 = 40 
n4 = 80 

simpson_composito_nfisso(f, a, b, n1, tol)
simpson_composito_nfisso(f, a, b, n2, tol)
simpson_composito_nfisso(f, a, b, n3, tol)
simpson_composito_nfisso(f, a, b, n4, tol)
