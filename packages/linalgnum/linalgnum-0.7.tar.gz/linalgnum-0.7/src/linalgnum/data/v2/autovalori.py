#CERCHI DI GERSCHGORIN
import numpy as np
import matplotlib.pyplot as plt

def GerschCircles(A):
    n,m = A.shape
    if n != m:
        print("error, not a square matrix")
        return
    disks = []
    for i in range(n):
        center = A[i][i]
        radius = sum(np.abs(A[i][j]) for j in range(n) if i!=j)

        disks.append((center, radius))
    return disks

def drawCircles(disks):

    plt.figure()
    plt.title('Gershgorin Circles', fontsize=18)
    plt.xlabel('Re')
    plt.ylabel('Im')
    color = [0.8, 1, 1]
    plt.grid(True)

    ev = np.linalg.eigvals(A)

    #asse x -> 2*pigreco
    x_sequence = np.linspace(0, 2*np.pi, 101)
    #i unità immaginaria per plot spazio complessi C
    i = np.exp(x_sequence*1j)

    for k in range(len(disks)):
        circle = disks[k][0] + disks[k][1]*i
        plt.fill(np.real(circle), np.imag(circle), color = [0.5,1,1])
        plt.plot(np.real(circle), np.imag(circle), 'k-')
        plt.plot(np.real(disks[k][0]), np.imag(disks[k][0]), 'bx')

    plt.plot(np.real(ev), np.imag(ev),'ro', label='autovalori')
    plt.legend()
    plt.axis('equal')
    plt.show()

#ESEMPIO GERSCHGORIN
A = np.array([[8,-2,1,0], [-2,2,-1,1], [1,-1,3,-1], [0,1,-1,-5]])
disks = GerschCircles(A)
print(disks)
drawCircles(disks)

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

#METODO DELLE POTENZE

def MetodoPotenze(A,x0,tol, maxN):
    
    iterazioni = 0
    flag = True
    
    y = x0/np.linalg.norm(x0,2)
    l = np.dot(y.T,np.dot(A,y))
    
    while(flag and iterazioni < maxN):
        iterazioni+=1
        l_old = l
        
        x = np.dot(A,y)
        y = x/np.linalg.norm(x,2)

        l = np.dot(y.T,np.dot(A,y))
    
        error = np.abs(1 - l/l_old)

        if error < tol:
            break

    return iterazioni, l, y



#ESEMPIO POWERM
A = np.array([[5,3,0,2,4],
              [1,9,2,6,3],
              [3,0,10,0,2],
              [0,5,2,-2,5],
              [0,3,5,2,15]])

x0 = np.array([1,1,1,1,1])
B = np.dot(A.T, A)
tol = 1e-10

iters,ev,vv= MetodoPotenze(B,x0,tol,40)
print(iters)
print(ev)
print(vv)

ev,vv = np.linalg.eig(B)
print(ev)
print(vv)


#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

#METODO DELLE POTENZE INVERSE 

def MetodoPotenzeInv(A,x0,tol,maxN):
    
    iterazioni = 0
    flag = True
    
    y = x0/np.linalg.norm(x0,2)
    l = np.dot(y.T,np.dot(np.linalg.inv(A),y))
    
    while(flag and iterazioni < maxN):
        iterazioni+=1
        l_old = l
        
        x = np.dot(np.linalg.inv(A),y)
        y = x/np.linalg.norm(x,2)

        l = np.dot(y.T,np.dot(np.linalg.inv(A),y))
        l_inv = 1/l
        error = np.abs(1 - l/l_old)

        if error < tol:
            break
        
    return iterazioni, l, l_inv, y

#ESEMPIO POWERMINV

A = np.array([[5,3,0,2,4],
              [1,9,2,6,3],
              [3,0,10,0,2],
              [0,5,2,-2,5],
              [0,3,5,2,15]])

x0 = np.array([1,1,1,1,1])
B = np.dot(A.T, A)
tol = 1e-10

iters,ev,ev_inv,vv= MetodoPotenzeInv(B,x0,tol,40)
print(iters)
print(ev)
print(ev_inv)
print(vv)


