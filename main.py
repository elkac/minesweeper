import numpy as np
import random as rd

def grid_creation(w, h, nb_mines):
    M = np.zeros((h,w))
    
    mines = [(rd.randint(0,h),rd.randint(0,w)) for i in range(nb_mines)]
    for l,c in mines:
        M[l,c]=-1
        nbhs = neighbourhood_3x3(w,h,(l,c))
        for l_n,c_n in nbhs:
            if M[l_n,c_n] != -1:
                M[l_n,c_n] += 1
    return M


    
    
def neighbourhood_3x3(w, h, coords):
    l,c = coords
    if coords == (0,0):
        nbhd = [(0,1),(1,0),(1,1)]
    elif coords == (0,w-1):
        nbhd = [(0,w-2),(1,w-2),(1,w-1)]
    elif coords == (h-1,0):
        nbhd = [(h-2,0),(h-2,1),(h-1,1)]
    elif coords == (h-1,w-1):
        nbhd = [(h-2,w-2),(h-2,w-1),(h-1,w-2)]
    elif l == 0:
        nbhd = [(0,c-1),(0,c+1),(1,c-1),(1,c),(1,c+1)]
    elif l == h-1:
        nbhd = [(h-2,c-1),(h-2,c),(h-2,c+1),(h-1,c-1),(h-1,c+1)]
    elif c == 0:
        nbhd = [(l-1,0),(l-1,1),(l,1),(l+1,0),(l+1,1)]
    elif c == w-1:
        nbhd = [(l-1,w-2),(l-1,w-1),(l,w-2),(l+1,w-2),(l+1,w-1)]
    else :
        nbhd = [(l-1,c-1),(l-1,c),(l-1,c+1),(l,c-1),(l,c+1),(l+1,c-1),(l+1,c),(l+1,c+1)]
    return nbhd