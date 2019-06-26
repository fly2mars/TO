# This a Python version 2D SIMP code based on
# AN 88 LINE TOPOLOGY OPTIMIZATION CODE Nov, 2010.

import numpy as np
import numpy.linalg as llg
from scipy import sparse

## KE = generate_stiffness_mat(nu)

def generate_stiffness_mat(nu):
    A11 = np.array([[12, 3, -6, -3], [ 3, 12,  3,  0], [-6,  3, 12, -3], [-3,  0, -3, 12]])
    A12 = np.array(np.mat('-6 -3  0  3; -3 -6 -3 -6;  0 -3 -6  3;  3 -6  3 -6'));
    B11 = np.array(np.mat('-4  3 -2  9;  3 -4 -9  4; -2 -9 -4 -3;  9  4 -3 -4'));
    B12 = np.array(np.mat('2 -3  4 -9; -3  2  9 -2;  4  9  2  3; -9 -2  3  2'));
    #KE = 1/(1-nu^2)/24*([A11 A12;A12' A11]+nu*[B11 B12;B12' B11]); 
    AA = np.vstack( (np.hstack((A11, A12)), np.hstack((A12.conj().transpose(), A11)) )) ## [A11 A12; A12' A11]
    BB = np.vstack(( np.hstack((B11, B12)), np.hstack((B12.conj().transpose(), B11)) )) ## [B11 B12; B12' B11]

    KE = 1/(1-nu**2)/24*(AA + nu * BB)
    return np.asmatrix(KE)

## iK, jK, edofMat = generate_volume(nelx, nely)
def generate_volume(nelx, nely):    
    nodenrs = np.arange(1,(1+nelx)*(1+nely)+1).reshape(1+nely, 1+nelx, order='F').copy();
    edofVec = (2*nodenrs[0:-1, 0:-1] + 1).reshape(nelx * nely, 1, order='F');
    edofMat = np.tile(edofVec,[1,8]) + np.tile(np.hstack([np.hstack([[0,1], 2*nely + np.array([2,3,0,1])]),[-2,-1]]), [nelx*nely,1])
    edofMat -= 1   # python index start from  0 
    iK = np.kron(edofMat, np.ones([8,1])).reshape([64*nelx*nely,1])
    jK = np.kron(edofMat, np.ones([1,8])).reshape([64*nelx*nely,1])
    return iK, jK, edofMat

# FEA(KE, E0, Emin, xPhys, penal)
def FEA(KE, E0, Emin, xPhys, penal, freedofs, U):
    Ei = np.asmatrix(xPhys.flatten() ** penal*(E0-Emin))    
    sK = np.dot(KE.flatten().transpose(), Ei).reshape(64*nely*nelx, 1, order='F')
    row = iK[:,0].transpose()
    col = jK[:,0].transpose()
    data = np.asarray(sK)[:,0].transpose()
    K = sparse.csc_matrix((data, (row,col)));
    K = (K+K.conj().T)/2;

    A = K[np.ix_(freedofs,freedofs)]
    B = np.asmatrix(F[freedofs])
    U[freedofs] = llg.solve(A.toarray(),B)

def preFilter(rmin):
    nTotal = nelx*nely*(2*(np.ceil(rmin)-1)+1)**2    # nTotal = x*y*Neighbors_per_element
    iH = np.ones(int(nTotal))
    jH = np.ones(iH.shape)
    sH = np.zeros(iH.shape)

    k = 0
    for i in np.arange(0,nelx):
        for j in np.arange(0,nely):
            e = i*nely + j
            neighbor_size = np.ceil(rmin) - 1 # unit: element
            neighbor_x = np.arange(max(i-neighbor_size, 0), min(i+neighbor_size+1, nelx))
            neighbor_y = np.arange(max(j-neighbor_size, 0), min(j+neighbor_size+1, nely))
            for ni in neighbor_x:
                for nj in neighbor_y:
                    neighbor_e = ni * nely + nj
                    iH[k] = e
                    jH[k] = neighbor_e
                    sH[k] = max(0, rmin - np.sqrt((ni-i)**2 +(nj-j)**2 ))
                    k += 1

    H = sparse.csc_matrix((sH, (iH, jH)) )
    Hs = np.sum(H, axis=1)
    return H, Hs

def OC(nelx, nely, xPhys, volfrac, dc, ft):
    l1 = 0
    l2 = 100000 
    move = 0.2
    while (l2-l1)/(l1+l2) > 1e-3:
        lmid = 0.5*(l2+l1);
        xnew = np.maximum(0,np.maximum(x-move,np.minimum(1,np.minimum(x+move,np.multiply(x, np.sqrt(-dc/dv/lmid))))));
        print('xnew')
        print(xnew)
        if ft == 1:
            xPhys = xnew
        else:
            if ft == 2:
                xPhys = (H * xnew.flatten().T) / Hs;

        if np.sum(xPhys.flatten()) > volfrac*nelx*nely:
            l1 = lmid
        else:
            l2 = lmid
            

if __name__ == '__main__':
    Max_Loop = 100
    nelx,nely = [60,20]
    volfrac = 0.5
    penal = 3.0
    rmin = 1.2 
    ft = 1

    E0 = 1       # Young's modulus
    Emin = 1e-9
    nu = 0.3

    ## init boundary conditions
    row = np.array([1])
    col = np.array([0])
    data = np.array([-1])
    F = sparse.csc_matrix((data, (row, col)), shape=(2*(nelx+1)*(nely+1), 1)).toarray()
    U = np.zeros([2*(nely+1)*(nelx+1),1])
    fixeddofs = np.hstack((np.arange(1, 2*(nely+1), 2), [2*(nelx+1)*(nely+1)])) - 1
    alldofs = np.arange(1, 2*(nely+1)*(nelx+1) + 1) - 1
    freedofs = np.array([x for x in alldofs if x not in fixeddofs])

    ## volume repsetation
    iK, jK, edofMat = generate_volume(nelx, nely)

    ## design variables
    x = np.tile(volfrac,(nely,nelx))
    xPhys = x#.copy();

    KE = generate_stiffness_mat(nu)
    H, Hs = preFilter(rmin)
    #U = FEA(KE, E0, Emin, xPhys, penal, freedofs)

    ## Optimization
    loop = 0
    change = 1
    print(1)

    ## start interation
    while change > 0.01 and loop < Max_Loop:
        loop += 1
        FEA(KE, E0, Emin, xPhys, penal, freedofs, U)
        ## Objective function and sensitivity analysis
        print(loop)
        a = np.multiply(np.asmatrix(U[edofMat]) * (KE), np.asmatrix(U[edofMat]))
        ce = np.sum(a, axis=1).reshape(nely, nelx, order='F')
        c = np.sum(np.sum(np.multiply((Emin+xPhys**penal *(E0-Emin)), ce)))
        dc = np.multiply(-penal * (E0-Emin)*xPhys**(penal-1),ce)
        dv = np.ones((nely,nelx))
        
        ## Filtering and modificating the sensitive
        if ft == 1:
            dc =( H * np.multiply(x, dc).flatten(order='F').T / Hs ).reshape(nely, nelx, order='F') 
    
            
        ## Update
        OC(nelx, nely, xPhys, volfrac, dc, ft)
            
        change = np.max(np.abs(xPhys-x));
        x = xPhys
        
        print("loop: " + str(loop))
        print(x)
        print(change)
    print('End')
    


# ref: https://docs.scipy.org/doc/numpy-dev/user/numpy-for-matlab-users.html


