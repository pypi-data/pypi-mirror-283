from logging import warning
import numpy as np

class LinearSystem:
    # Classe simbolica che rappresenta un sistema lineare Ax = b

    def __init__(self, A: np.ndarray, b: np.ndarray):
        # Eseguo dei controlli per verificare che il sistema lineare sia ben definito
        assert len(A.shape) == 2, "A deve essere una matrice"
        assert len(b.shape) == 1, "b deve essere un vettore"
        assert A.shape[0] == b.shape[0], "A deve avere un numero di righe uguale a b"
        self.A = A.astype(np.double)
        self.b = b.astype(np.double)
        self.equations = A.shape[0]
        self.variables = A.shape[1]
    
    def is_strictly_diagonally_dominant(self):
        # La matrice A è strettamente diagonalmente dominante se il valore assoluto dell'elemento diagonale è maggiore della somma degli altri elementi della riga
        assert self.A.shape[0] == self.A.shape[1], "La matrice deve essere quadrata"
        n = self.A.shape[0]
        for i in range(n): 
            aii = self.A[i, i]  
            row = sum( [ self.A[i, j] for j in range(n) if j != i ] )
            if aii <= row: return False
        return True
    
    def __repr__(self):
        # Rappresentazione testuale simbolica del sistema lineare, usata per stampare in console
        return f"""LinearSystem(\nA=\n{self.A},\nb=\n{self.b},\nequations=\n{self.equations},\nvariables=\n{self.variables})"""

def jacobi(linear_system: LinearSystem, max_iter=10000, tolerance=1e-8, x0=None):
    #Se non diverge, il metodo di Jacobi calcola una soluzione tendente a quella reale

    # Essere strettamente diagonale dominante è una condizione sufficiente per la convergenza del metodo di Jacobi
    if not linear_system.is_strictly_diagonally_dominant():
        print("La matrice non è strettamente diagonale dominante, il metodo potrebbe non convergere")

    # Se x0 non è specificato, si inizializza con un vettore casuale
    if x0 is None:
        x = np.random.rand(linear_system.variables)
    else:
        x = x0.astype(np.double).copy()
    # Eseguo un massimo di max_iter iterazioni
    for iter in range(max_iter):
        # Aggiorno il vettore x delle soluzioni solo dopo il calcolo
        temp_x = x.copy()
        for i in range(linear_system.variables): # Ciclo per un numero pari al numero di variabili
            # Calcolo la somma degli elementi della riga i-esima eccetto l'elemento diagonale
            rowsum = sum([ linear_system.A[i, j] * temp_x[j] for j in range(linear_system.variables) if i != j ])
            # Aggiorno il valore della variabile x[i] con la formula di Jacobi
            x[i] = (linear_system.b[i] - rowsum) / linear_system.A[i,i]
        # Eseguo il controllo per il criterio di terminazione basato sull'errore
        if np.abs(np.sum(np.abs(np.dot(linear_system.A,x) -b))) < tolerance:
            break
    return iter, x

def gauss_seidel(linear_system: LinearSystem, max_iter=10000, tolerance=1e-8, x0=None):
    #Se non diverge, il metodo di Gauss Seidel calcola una soluzione tendente a quella reale

    # Essere strettamente diagonale dominante è una condizione sufficiente per la convergenza del metodo di Jacobi
    if not linear_system.is_strictly_diagonally_dominant():
        print("La matrice non è strettamente diagonale dominante, il metodo potrebbe non convergere")

    # Se x0 non è specificato, si inizializza con un vettore casuale
    if x0 is None:
        x = np.random.rand(linear_system.variables)
    else:
        x = x0.copy()
    # Eseguo un massimo di max_iter iterazioni
    for iter in range(max_iter):
        # Il vettore x delle soluzioni viene aggiornato durante il calcolo
        for i in range(linear_system.variables): # Ciclo per un numero pari al numero di variabili
            # Calcolo la somma degli elementi della riga i-esima eccetto l'elemento diagonale
            rowsum = sum([ linear_system.A[i, j] * x[j] for j in range(linear_system.variables) if i != j ])
            # Aggiorno il valore della variabile x[i] con la soluzione di Gauss Seidel
            x[i] = (linear_system.b[i] - rowsum) / linear_system.A[i,i]
        # Eseguo il controllo per il criterio di terminazione basato sull'errore
        if np.abs(np.sum(np.abs(np.dot(linear_system.A,x) -b))) < tolerance:
            break
    return iter, x



def _forward_substitution(S: LinearSystem):
    """ The forward substitution method take a lower
        triangular matrix A as input (coefficient matrix
        of a linear system) and a vector of costant terms b.
        The function computes the solution of the linear system.
    """
    assert S.is_squared(), "Needs a squared linear system."
    x = np.zeros(S.variables)
    for i in range(S.equations):
        tmp = S.b[i]
        # Given the index i=3, the range returns the
        # previous elements (j=0, j=1, j=2). When i=0,
        # we should set range(0) that is empty.
        for j in range( i if i - 1 >= 0 else 0 ): tmp -= S.A[i, j] * x[j]
        x[i] = tmp / S.A[i, i]
    return x

def _backward_substitution(S: LinearSystem):
    """ The backward substitution method take an upper
        triangular matrix A as input (coefficient matrix
        of a linear system) and a vector of costant terms b.
        The function computes the solution of the linear system.
    """
    assert S.is_squared(), "Needs a squared linear system."
    n = S.equations
    x = np.zeros(S.variables)
    for i in reversed(range(n)):
        tmp = S.b[i]
        # The row iterations are reversed, so we start from
        # the bottom of the matrix. We should also iterate
        # the columns in a reversed manner (recall we need
        # to compute the solution components in a give order).
        for j in range(n-1, i, -1): tmp -= S.A[i, j] * x[j]
        x[i] = tmp / S.A[i, i]
    return x

def gem_solve(S: LinearSystem):
    """ Perform the Gaussian elimination method.
    """
    assert S.is_squared(), "Needs a squared linear system."
    assert mx.determinant(S.A) != 0
    # assert can_apply_gem(A)
    L, U, P = mx.LU(S.A)
    # b = np.matmul(P, b)
    y =  _forward_substitution(LinearSystem(L, S.b))
    x = _backward_substitution(LinearSystem(U, y))
    return x

def can_apply_gem(A: np.ndarray):
    """ If all the principal minors of the matrix
        have a non-zero determinant, all the diagonals
        elements will be non-zero during the Gaussian
        elimination method.
    """
    pms = mx.get_matrix_principal_minors(A)
    for pm in pms:
        if mx.determinant(pm) == 0:
            return False
    return True



if __name__ == '__main__':
    A = np.array([[2,0,1,0],[0, 2, 0, 0],
    [1, 0, 2, 1],
    [0, 0, 1, 1]])
    b = np.array([3,2,4,2])
    S1 = LinearSystem(A, b)
    print(S1)
    print(jacobi(S1, x0=np.array([0,1,0,1])))