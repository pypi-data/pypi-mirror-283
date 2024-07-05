#GAUSS NAIVE
from numpy.linalg import solve
from numpy.linalg import norm
import numpy as np

#METODI DI ELIMINAZIONE DI GAUSS
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

#GAUSSNAIVE TEST
A=np.array([[1.0,1.0,1.0],[1.0,-1.0,-1.0],[1.0,-2.0,3.0]])
A2 = A.copy()
#A2 = np.array([[1.0,1.0,1.0],[1.0,-1.0,-1.0],[1.0,-2.0,3.0]])
b=np.array([1.0,1.0,-5.0])
b2=b.copy()
#b2 = np.array([1.0,1.0,-5.0])

x = GaussNaive(A,b)
x_real = np.linalg.solve(A2,b2)

print("Gausss ", x)
print("Numpy ", x_real)

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

#Jacobi: Metodo iterativo
def Jacobi(A,b,x0,tol):

   x = np.copy(x0)
   iterazione = 0

   while  (np.abs(np.sum(np.abs(np.dot(a, x) - b)))) > tol:

      prev_x = x
      for i in range(len(A)):
         s = 0
         
         for j in range(len(A)):
            if not (i == j):
               s = s + A[i][j]*prev_x[j]

         x[i] = float((b[i] - s)/A[i][i])

      iterazione += 1

   return x,iterazione

#JACOBI TEST
a = np.array([[2.0,0.0,1.0,0.0],
              [0.0,2.0,0.0,0.0],
              [1.0,0.0,2.0,1.0],
              [0.0,0.0,1.0,1.0]])
b = np.array([3.0,2.0,4.0,2.0])

x0 = np.array([0.0,1.0,0.0,1.0])
tol = 0.000001

x,iterazioni= Jacobi(a,b,x0,tol)
print(x)
print(iterazioni)

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

# GAUSS-SEIDEL


def GaussSeidel(A,b,x0,tol):
   x = x0
   iter = 0

   while (np.abs(np.sum(np.abs(np.dot(a, x) - b)))) > tol:
      for i in range(len(A)):
         s = 0
         for j in range(len(A)):
            if i != j:
               s = s + A[i][j] * x[j]
         x[i] = (b[i] - s)/A[i][i]
      iter = iter + 1
   
   return x,iter


# GAUSS-SEIDEL TEST
a = np.array([[3.0, 0.0, 4.0],
              [7.0, 4.0, 2.0],
              [-1.0, -1.0, -2.0]])
b = np.array([7.0, 13.0, -4.0])



x0 = np.zeros(len(b))
x, iter = GaussSeidel(a, b, x0, 1e-3)

print(x)
print(iter)