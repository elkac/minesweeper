import numpy as np
import random as rd
from tabulate import tabulate
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QMessageBox
)
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt

class minesweeper():
    def __init__(self, w, h, nb_mines):
        self.w = w
        self.h = h
        self.nb_mines = nb_mines
        
        self.grid = np.zeros((h, w, 2), dtype=int)
        
        self.revealed = 0
        self.end = False
        self.first_click = True
        
        self.mines = []
        
    def init_grid(self, first_click):
        l_init,c_init = first_click
        
        begin = neighbourhood_3x3(self.h,self.w,(l_init,c_init))
        begin.append((l_init,c_init))
        
        self.mines = self.unique_mines(begin)
        hidden = self.grid[:,:,0]
        for l,c in self.mines:
            hidden[l,c]=-1
            nbhs = neighbourhood_3x3(self.h,self.w,(l,c))
            for l_n,c_n in nbhs:
                if hidden[l_n,c_n] != -1:
                    hidden[l_n,c_n] += 1
                    
        self.first_click = False
        self.reveal_cell((l_init,c_init))
        
    def unique_mines(self, avoid):
        pos = [(i, j) for i in range(self.h) for j in range(self.w)]
        pos = [p for p in pos if p not in avoid]
        mines = rd.sample(pos, self.nb_mines)
        return mines
    
    # def display(self):
    #     displayed = self.grid[:,:,0].copy().astype(str)
    #     displayed[self.grid[:,:,1]==0] = '■'
    #     displayed[self.grid[:,:,1]==2] = '►'
    #     displayed[displayed=='0'] = ''
    #     displayed[displayed=='-1'] = '☼'
    #     displayed[displayed=='-2'] = '♣'
    #     print(tabulate(displayed, tablefmt="grid"))
        
    # def interaction(self):
    #     while True:
    #         inter = input("Choisissez une action :\nc -> Révéler une case\nf -> Mettre un drapeau\nr -> Enlever un drapeau\n>>> ")
            
    #         if inter in ['c', 'f', 'r']:
    #             break
    #         print("L'action doit être c, f ou r.")
        
    #     l,c = self.get_coords()
            
    #     if inter == 'c':
    #         self.reveal_cell((l,c))
    #     elif inter == 'f':
    #         self.put_flag((l,c))
    #     elif inter == 'r':
    #         self.remove_flag((l,c))
            
    # def get_coords(self):
    #     while True:
    #         coords = input("Remplissez les coordonnées de la case à modifier (ex : ligne 2 et colonne 3 -> 23) :\n>>> ")
            
    #         if len(coords) != 2:
    #             print("Les coordonnées doivent être composées de 2 caractères.\n")
    #             continue
            
    #         try:
    #             int_coords = int(coords)
    #         except:
    #             print("Les coordonnées doivent être des nombres entiers.\n")
    #             continue

    #         l,c = int(coords[0]), int(coords[1])
            
    #         if not (0 <= l < self.h and 0 <= c < self.w):
    #             print(f"Les coordonnées doivent être comprises entre :\n0 et {self.h-1} pour la ligne,\n0 et {self.w-1} pour la colonne.\n")
    #             continue
            
    #         break
        
    #     return l,c  
            
    def reveal_cell(self, coords):
        if self.end:
            return
        
        if self.first_click:
            self.init_grid(coords)
            
        l,c = coords
        if self.grid[l,c,1] == 0:
            if self.grid[l,c,0] == 0:
                self.grid[l,c,1] = 1
                self.revealed += 1
                
                for nbhd in neighbourhood_3x3(self.h, self.w, (l,c)):
                    self.reveal_cell(nbhd)
                    
            elif self.grid[l,c,0] == -1:
               self.grid[l,c,1] = 1
               self.loose()
               
            elif self.grid[l,c,0] == 0:
                pass
            else:
                self.grid[l,c,1] = 1
                self.revealed += 1
            
        if self.revealed == self.w*self.h - self.nb_mines and not self.end :
            self.win()
    
    def put_flag(self, coords):
        l,c = coords
        if self.grid[l,c,1] == 0:
            self.grid[l,c,1] = 2
        
    def remove_flag(self, coords):
        l,c = coords
        if self.grid[l,c,1] == 2:
            self.grid[l,c,1] = 0
            
    def win(self):
        self.end = True
        # self.grid[:,:,0][self.grid[:,:,0] == -1] = -2
        self.grid[:,:,1] = 1
        
    def loose(self):
        self.end = True
        self.grid[:,:,1] = 1

    # def game(self):
    #     self.end = False
    #     while not self.end:
    #         self.display()
    #         self.interaction()
    #     self.display()
        
        
class MinesweeperGUI(QWidget):
    def __init__(self, w=9, h=9, nb_mines=10):
        super().__init__()

        self.game = minesweeper(w, h, nb_mines)
        self.w = w
        self.h = h

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Démineur PyQt")
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.buttons = {}

        for l in range(self.h):
            for c in range(self.w):
                btn = QPushButton("■")
                btn.setFixedSize(35, 35)
                btn.setStyleSheet("font-size: 18px; font-weight: bold;")

                btn.mousePressEvent = lambda event, l=l, c=c: self.handle_click(event, (l, c))

                self.grid_layout.addWidget(btn, l, c)
                self.buttons[(l, c)] = btn

        self.show()

    def handle_click(self, event, coords):
        if self.game.end:
            return

        if event.button() == Qt.LeftButton:  # clic gauche -> révéler
            self.game.reveal_cell(coords)

        elif event.button() == Qt.RightButton:  # clic droit -> drapeau
            l, c = coords
            if self.game.grid[l, c, 1] == 0:
                self.game.put_flag(coords)
            elif self.game.grid[l, c, 1] == 2:
                self.game.remove_flag(coords)

        self.update_display()

        if self.game.end:
            self.finish_game()

    def update_display(self):
        for l in range(self.h):
            for c in range(self.w):
                value = self.game.grid[l, c, 0]
                state = self.game.grid[l, c, 1]
                btn = self.buttons[(l, c)]

                if state == 0:
                    btn.setText("■")
                elif state == 2:
                    btn.setText("⛳")
                    btn.setStyleSheet("color: red; font-size: 18px; font-weight: bold;")
                elif state == 1:
                    if value == -1:
                        btn.setText("💣")
                    elif value == 0:
                        btn.setText("")
                    else:
                        btn.setText(str(value))
                        btn.setStyleSheet("font-size: 18px; font-weight: bold; color: blue;")

                    btn.setEnabled(False)

    def finish_game(self):
        if self.game.revealed == self.w * self.h - self.game.nb_mines:
            QMessageBox.information(self, "Victoire", "🎉 Bravo ! Tu as gagné !")
        else:
            QMessageBox.critical(self, "Défaite", "💥 Perdu ! Tu as touché une mine.")

    
def neighbourhood_3x3(h, w, coords):
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


def display_board(game):
    for l in range(game.h):
        row = ""
        for c in range(game.w):
            state = game.grid[l, c, 1]
            val = game.grid[l, c, 0]

            if state == 0:
                row += " . "
            elif state == 2:
                row += " F "
            elif state == 1:
                if val == -1:
                    row += " * "
                elif val == 0:
                    row += "   "
                else:
                    row += f" {val} "
        print(row)
    print()

def console_play():
    game = minesweeper(9, 9, 10)

    while not game.end:
        display_board(game)
        action = input("Action (r pour reveal / f pour flag) : ")
        l = int(input("ligne : "))
        c = int(input("colonne : "))

        if game.first_click:
            game.init_grid((l, c))
        else:
            if action == "r":
                game.reveal_cell((l, c))
            elif action == "f":
                if game.grid[l, c, 1] == 2:
                    game.remove_flag((l, c))
                else:
                    game.put_flag((l, c))

    display_board(game)



def start_gui():
    app = QApplication([])
    window = MinesweeperGUI(9, 9, 10)
    window.show()
    app.exec_()


if __name__ == "__main__":
    print("Choisir le mode :")
    print("1 - Console")
    print("2 - Interface graphique PyQt5")
    mode = input("Votre choix : ")

    if mode == "1":
        console_play()
    elif mode == "2":
        start_gui()
    else:
        print("Choix invalide")