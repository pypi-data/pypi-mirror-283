import numpy as np
import matplotlib.pyplot as plt

#1 INTERPOLAZIONE COEFFICIENTI INDETERMINATI CON VANDERMONDE-> SISTEMI LINEARI

def GaussNaive(A, b):
    
    #Controllo che A sia quadrata
    n,m = A.shape
    if(n != m):
        print("Matrice A non quadrata, impossibile applicare il metodo")
        return 
    
    x = np.zeros(n)
    for k in range(n-1):
        for i in range(k+1, n):
            if(A[k][k] == 0):                             #condizione elemento pivot (A[k][k] != 0) 
                print("null diagonal element")
                return
            m = A[i][k] / A[k][k]                    
            for j in range(k+1,n):
                A[i][j] = A[i][j] -m*A[k][j] 
            b[i] = b[i] -m*b[k]
    
    #step di sostituzione all'indietro
    for i in range (n-1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, (i+1):n], x[(i+1):n]))/A[i][i]

    return x


x = np.array([-2,-1,1,3])
y = np.array([4,3,2,1]);

A = [ [p ** i for i in range(len(x))  ]  for p in x ] # Matrice di Vandermonde
A = np.array(A)

a = GaussNaive(A, y)
print(a)

#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#2 INTERPOLAZIONE DI LAGRANGE    

def compute_lagrange(xval,x,i):
    n = len(x)
    temp_value=1.0
    for j in range(n):
        if(i!=j): 
            temp_value*=(xval-x[j])/(x[i]-x[j])
    return temp_value

def interp_lagrange(xval,x,y):
    n = len(x)
    value=0.0
    if(len(y) != n):
        return
    for i in range(n):
        value += y[i]*compute_lagrange(xval,x,i)
    return value

#ESEMPIO
x = np.array([7,8,9,10]) # ---> n punti => polinomio grado n-1
y = np.array([3,1,1,9])

#CHECK FUNZIONI LIBRERIA
check = np.polyfit(x,y,3)
x_range = np.linspace(x[0], x[3], 100)
yy_np = np.polyval(check,x_range)
#print(yy_np)

#LAGRANGE
yy_lagrange = np.zeros(len(x_range))
for i,value in enumerate(x_range):
    yy_lagrange[i] = interp_lagrange(value, x, y) 
print(yy_lagrange)



#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#
#------------------------------------------------------------------------------#

#3 INTERPOLAZIONE DIFFERENZE DIVISE- NEWTON 

def coef_differenze_div(x,y):
    
    n = len(x)
    coef = np.zeros([n,n])
    coef[:,0] = y
    
    for j in range(1,n):
        for i in range(n-j):
            coef[i][j] = (coef[i+1][j-1] - coef[i][j-1]) / (x[i+j] - x[i])
    return coef[0,:]

def newton_differenze_div(coef, x, x_new):
    
    n=len(x) 
    p = coef[n-1]
    
    for i in range(1,n+1):
        p = coef[n-i] + (x_new - x[n-i])*p
        
    return p

#ESEMPIO
x = np.array([7,8,9,10]) # ---> n punti => polinomio grado n-1
y = np.array([3,1,1,9])

#CHECK FUNZIONI LIBRERIA
check = np.polyfit(x,y,3)
x_range = np.linspace(x[0], x[3], 100)
yy_np = np.polyval(check,x_range)
#print(yy_np)

#NEWTON
coef = coef_differenze_div(x,y)
yy_newton = np.zeros(len(x_range))
for i,value in enumerate(x_range):
    yy_newton[i] = newton_differenze_div(coef, x, value)
print(yy_newton)


