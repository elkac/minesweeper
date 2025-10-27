import numpy as np
import random as rd
from tabulate import tabulate


class minesweeper():
    def __init__(self, w, h, nb_mines):
        self.w = w
        self.h = h
        self.nb_mines = nb_mines
        
        self.grid = np.zeros((h,w,2), dtype=int)
        
        hidden = self.grid[:,:,0]
        self.mines = self.unique_mines()
        for l,c in self.mines:
            hidden[l,c]=-1
            nbhs = neighbourhood_3x3(w,h,(l,c))
            for l_n,c_n in nbhs:
                if hidden[l_n,c_n] != -1:
                    hidden[l_n,c_n] += 1
        self.game()
        
    def unique_mines(self):
        pos = [(i, j) for i in range(self.h) for j in range(self.w)]
        mines = rd.sample(pos, self.nb_mines)
        return mines
                    
    def display(self):
        displayed = self.grid[:,:,0].copy().astype(str)
        displayed[self.grid[:,:,1]==0] = '■'
        displayed[self.grid[:,:,1]==2] = '►'
        displayed[displayed[:,:]=='0'] = ''
        displayed[displayed[:,:]=='-1'] = '☼'
        print(tabulate(displayed, tablefmt="grid"))
        
    def interaction(self):
        while True:
            inter = input("Choisissez une action :\nc -> Révéler une case\nf -> Mettre un drapeau\nr -> Enlever un drapeau\n>>> ")
            
            if inter in ['c', 'f', 'r']:
                break
            print("L'action doit être c, f ou r.")
        
        while True:
            coords = input("Remplissez les coordonnées de la case à modifier (ex : ligne 2 et colonne 3 -> 23) :\n>>> ")
            
            if len(coords) != 2:
                print("Les coordonnées doivent être composées de 2 caractères.\n")
                continue
            
            try:
                int_coords = int(coords)
            except:
                print("Les coordonnées doivent être des nombres entiers.\n")
                continue

            l,c = int(coords[0]), int(coords[1])
            
            if not (0 <= l < self.h and 0 <= c < self.w):
                print(f"Les coordonnées doivent être comprises entre :\n0 et {self.h-1} pour la ligne,\n0 et {self.w-1} pour la colonne.\n")
                continue
            
            break
            
        if inter == 'c':
            self.reveal_cell((l,c))
        elif inter == 'f':
            self.put_flag((l,c))
        elif inter == 'r':
            self.remove_flag((l,c))
            
    def reveal_cell(self, coords):
        l,c = coords
        if self.grid[l,c,1] == 0:
            if self.grid[l,c,0] == 0:
                self.grid[l,c,1] = 1
                self.revealed += 1
                
                for nbhd in neighbourhood_3x3(self.w, self.h, (l,c)):
                    self.reveal_cell(nbhd)
                    
            elif self.grid[l,c,0] == -1:
               self.grid[l,c,1] = 1
               self.end = True
               print("Perdu... tu as fait exploser une mine ☼")
               
            elif self.grid[l,c,0] == 0:
                pass
            else:
                self.grid[l,c,1] = 1
                self.revealed += 1
            
        if self.revealed == self.w*self.h - self.nb_mines:
            self.end = True
            print("Bravo, tu as trouvé toutes les mines !")
    
    def put_flag(self, coords):
        l,c = coords
        if self.grid[l,c,1] == 0:
            self.grid[l,c,1] = 2
        
    def remove_flag(self, coords):
        l,c = coords
        if self.grid[l,c,1] == 2:
            self.grid[l,c,1] = 0
            
    def create_mines(self):
        self.display()
        self.interaction()            
    def game(self):
        self.end = False
        self.revealed = 0
        self.create_mines()
        while not self.end:
            self.interaction()
            self.display()

    
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




if __name__ == "__main__":
    width = 7
    height = 7
    nb_mines = 6
    
    grid = minesweeper(width, height, nb_mines)