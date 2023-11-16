import math
import numpy as np

def logistic_chaotic_mapping(mu, x):
    return mu * x * (1-x)
    
def switch_columns(mu, x, image:np.ndarray):
    M, N = image.shape

    for i in range(N):
        x = logistic_chaotic_mapping(mu,x)
        j = math.floor(x * N)
        k1 = math.ceil((x * 1000)%256)
        k2 = math.ceil((x * 10000)%256)
        
        if j < i:
            j = i
        
        if i != j:
            for k in range(M):
                image[k][i] = image[k][i] ^ k1
            for k in range(M):
                image[k][j] = image[k][j] ^ k2
        else:
            for k in range(M):
                image[k][i] = image[k][i] ^ k1
        
        image[:, [i, j]] = image[:, [j, i]]
        
        s = np.sum(image[:, i])
            
        s /= 1000
        
        x, tmp = math.modf(x+s)

    return image

def deswitch_columns(mu, x, cimage:np.ndarray):
    M, N = cimage.shape
    
    j = [0]*N
    k1 = [0]*N
    k2 = [0]*N
    
    for i in range(N):
        x = logistic_chaotic_mapping(mu,x)
        jj = math.floor(x * M)
        k1[i] = math.ceil((x * 1000)%256)
        k2[i] = math.ceil((x*10000)%256)
        if jj<i:
            j[i] = i
        else:
            j[i] = jj

        s = np.sum(cimage[:, i])
        s /= 1000
        x, tmp = math.modf(x+s)

    i = N-1
    while i >= 0:
        if i != j[i]:
            for k in range(M):
                cimage[k][j[i]] = cimage[k][j[i]] ^ k1[i]
            for k in range(M):
                cimage[k][i] = cimage[k][i] ^ k2[i]
        else:
            for k in range(M):
                cimage[k][j[i]] = cimage[k][j[i]] ^ k1[i]
        
        
        cimage[:, [i, j[i]]] = cimage[:, [j[i], i]]
            
        i -= 1 
    return cimage



    