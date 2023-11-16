import math
import numpy as np
from PIL import Image

def logistic_chaotic_mapping(mu, x):
    return mu * x * (1-x)
    
def switch_rows(mu, x, image:np.ndarray):
    M, N = image.shape

    for i in range(M):
        x = logistic_chaotic_mapping(mu,x)
        j = math.floor(x * M)
        k1 = math.ceil((x * 1000)%256)
        k2 = math.ceil((x * 10000)%256)
        
        if j < i:
            j = i
        
        if i != j:
            for k in range(N):
                image[i][k] = image[i][k] ^ k1
            for k in range(N):
                image[j][k] = image[j][k] ^ k2
        else:
            for k in range(N):
                image[i][k] = image[i][k] ^ k1
        
        image[[i, j], :] = image[[j, i], :] 
        
        s = sum(image[i])/1000
        x, tmp = math.modf(x+s)

    return image

def deswitch_rows(mu, x, rimage):
    M = len(rimage)
    N = len(rimage[0])
    
    j = [0]*M
    k1 = [0]*M
    k2 = [0]*M
    
    for i in range(M):
        x = logistic_chaotic_mapping(mu,x)
        jj = math.floor(x * M)
        k1[i] = math.ceil((x * 1000)%256)
        k2[i] = math.ceil((x*10000)%256)
        if jj<i:
            j[i] = i
        else:
            j[i] = jj
        s = sum(rimage[i])/1000
        x, tmp = math.modf(x+s)

    i = M-1
    while i >= 0:
        if i != j[i]:
            for k in range(N):
                rimage[j[i]][k] = rimage[j[i]][k] ^ k1[i]
            for k in range(N):
                rimage[i][k] = rimage[i][k] ^ k2[i]
        else:
            for k in range(N):
                rimage[j[i]][k] = rimage[j[i]][k] ^ k1[i]
        
        rimage[[i, j[i]], :] = rimage[[j[i], i], :]
        i -= 1 
    return rimage

    
    