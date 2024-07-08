import numpy as np 
import matplotlib.pyplot as plt 

def metodoNewton(f, f1, x0, tol):

   k = 0
   x_old = x0
   while(True):
      x = x_old - f(x_old)/f1(x_old)
      print(abs(x - x_old), k)
      if abs(x - x_old) <= tol:
         break
      
      k+=1

      x_old = x

   return k, x_old

# Esercizio di intersezione di due funzioni f1 e f2 si riconduce a zeri della funzione differenza f3= f1-f2 
def intersezione_funzioni(x, y1, y2):

   n = len(x)
   inter_x = []
   inter_y = []

   for i in range(n):
      if np.isclose(y1[i], y2[i], atol=0.1):
         print(y1[i], y2[i])
         inter_x.append(x[i])
         inter_y.append(y1[i])
   
   return inter_x,inter_y

# Funzioni e Derivazioni, come espressioni lambda
f1 = lambda x: np.log(x)
f2 = lambda x: (-1)*x + 2
f12 = lambda x: np.log(x) + x -2 #-> proprietà metodo di newton, zeri della funzione differenza (f1-f2)
df12 = lambda x: 1/x + 1

# x e y
x = np.linspace(1,5, 100) # calcolo i punti della x
y1 = f1(x) # calcolo i punti della y (prima funzione)
y2 = f2(x) # calcolo i punti della y (seconda funzione)
y12 = f12(x)
tol = 1e-6
x0 = 1.5

# Metodi
inter_x, inter_y = intersezione_funzioni(x, y1, y2)
print(f"Punti di intersezione delle due rette: x: {inter_x}, y: {inter_y}")
iter, aprx_sol = metodoNewton(f12, df12, x0, tol)
print(f"iterazioni: {iter}  \napprossimazione soluzione: {aprx_sol}")

# plot del grafico
plt.plot(x, y1, color = "orange")
plt.plot(x, y2, color = "blue")
plt.scatter(inter_x, inter_y, color = "red")

plt.show()

#PUNTO FISSO

def punto_fisso(f, dx, x0, alpha, tol, nmax):
    x = [None] * (nmax + 1)
    x[1] = x0
    for i in range(1, nmax):
        fk = f(x[i])
        fdx = dx(x[i])
        x[i+1] = x[i] - fk / fdx
        if abs(x[i+1] - alpha) < tol:
            break
    print("L'iterazione ha converto in ", i, "passi")
    print("I valori di x sono: ", x[1:i+2])
    xs = x[1:i+2]
    xz = np.zeros(len(xs))
    xx = np.linspace(-3, 3, 100)
    y = xx
    yy = 1 + xx - np.power(xx, 2) / 4
    
    print(xs)
    print(xz)
    print(xx)
    print(y)
    print(yy)
    
    plt.plot(xx, y, xx, yy, -2,-2, "ro", 2,2, "ro", xs, xz, '*')



import numpy as np
import matplotlib.pyplot as plt

f = lambda x: (x**2)/4 -1
dx = lambda x: x/2

punto_fisso(f, dx, 1.5, 2, 1e-4, 5)


