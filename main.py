"""
Minesweeper (Démineur)

Implémentation du jeu du démineur en Python, jouable en mode console
ou avec une interface graphique PyQt5.

Contient :
- la logique du jeu (classe Minesweeper)
- l'interface graphique (classe MinesweeperGUI)
- l'écran de sélection de difficulté
- un mode console totalement fonctionnel
"""


import numpy as np
import random as rd
from tabulate import tabulate
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QGridLayout, QMessageBox, QComboBox, QVBoxLayout, QLabel
)
from PyQt5.QtCore import Qt


### LOGIQUE DU JEU
class minesweeper():
    """
    Classe représentant la logique du jeu du Démineur.

    Parameters
    ----------
    w : int
        Nombre de colonnes de la grille.
    h : int
        Nombre de lignes de la grille.
    nb_mines : int
        Nombre total de mines à  placer.

    Attributes
    ----------
    grid : ndarray (h, w, 2)
        Grille du jeu. Première couche : contenu (-1 = mine, 0..8 = indices)
        Deuxième couche : état de la cellule (0 = caché, 1 = révélé, 2 = drapeau)
    first_click : bool
        Empêche de placer une mine sur le premier clic.
    """
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
        """
        Initialise la grille après le premier clic.

        Parameters
        ----------
        first_click : tuple(int, int)
            Coordonnées (l, c) du premier clic à  protéger.
        """
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
        """
        Génère aléatoirement des mines hors de la zone interdite.

        Parameters
        ----------
        avoid : list of tuple
            Liste des positions où aucune mine ne doit apparaitre.

        Returns
        -------
        list of tuple
            Coordonnées des mines.
        """
        pos = [(i, j) for i in range(self.h) for j in range(self.w)]
        pos = [p for p in pos if p not in avoid]
        mines = rd.sample(pos, self.nb_mines)
        return mines
            
    def reveal_cell(self, coords):
        """
        Révèle une cellule et propage si nécessaire (case vide).

        Parameters
        ----------
        coords : tuple(int, int)
            Coordonnées de la cellule à  révéler.
        """
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
               self.end_game()
               
            elif self.grid[l,c,0] == 0:
                pass
            else:
                self.grid[l,c,1] = 1
                self.revealed += 1
            
        if self.revealed == self.w*self.h - self.nb_mines and not self.end :
            self.end_game()
    
    def put_flag(self, coords):
        """Place un drapeau sur une case cachée."""
        l,c = coords
        if self.grid[l,c,1] == 0:
            self.grid[l,c,1] = 2
        
    def remove_flag(self, coords):
        """Retire un drapeau."""
        l,c = coords
        if self.grid[l,c,1] == 2:
            self.grid[l,c,1] = 0
            
    def end_game(self):
        """Déclenche la fin de partie."""
        self.end = True
        self.grid[:,:,1] = 1
        
        
        
### INTERFACE GRAPHIQUE
class MinesweeperGUI(QWidget):
    """
    Interface graphique PyQt5 du jeu du Démineur.
    """
    def __init__(self, w=9, h=9, nb_mines=10):
        super().__init__()

        self.game = minesweeper(w, h, nb_mines)
        self.w = w
        self.h = h

        self.initUI()

    def initUI(self):
        """Crée l'affichage interactif."""
        self.setWindowTitle("Démineur")
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
        """Gère les clics gauche et droit."""
        if self.game.end:
            return

        if event.button() == Qt.LeftButton:
            self.game.reveal_cell(coords)

        elif event.button() == Qt.RightButton:
            l, c = coords
            if self.game.grid[l, c, 1] == 0:
                self.game.put_flag(coords)
            elif self.game.grid[l, c, 1] == 2:
                self.game.remove_flag(coords)

        self.update_display()

        if self.game.end:
            self.finish_game()

    def update_display(self):
        """Met à  jour visuellement chaque bouton."""
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
        """Affiche la fenêtre de fin de partie."""
        if self.game.revealed == self.w * self.h - self.game.nb_mines:
            QMessageBox.information(self, "Victoire", "Bravo ! Tu as gagné !")
        else:
            QMessageBox.critical(self, "Défaite", "Perdu ! Tu as touché une mine.")




### OUTILS
    
def neighbourhood_3x3(h, w, coords):
    """
    Calcule les voisins 3x3 autour d'une case.

    Parameters
    ----------
    h, w : int
        Dimensions de la grille.
    coords : tuple
        (l, c) coordonnée de centre.

    Returns
    -------
    list of tuple
        voisins valides
    """
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

def choose_difficulty():
    difficulty_levels = {
        "facile": {"h": 8, "w": 10, "nb_mines": 10},
        "moyen":  {"h": 14, "w": 18, "nb_mines": 40},
        "difficile": {"h": 20, "w": 24, "nb_mines": 100}
    }
    
    print("Choisissez un niveau : facile / moyen / difficile")
    while True:
        level = input("Niveau : ").lower()
        if level in difficulty_levels:
            params = difficulty_levels[level]
            return params["w"], params["h"], params["nb_mines"]
        print("Niveau invalide, réessayez...")
        


### MODE CONSOLE

def console_play():
    """Lance le jeu en mode console."""
    w, h, nb_mines = choose_difficulty()
    game = minesweeper(w, h, nb_mines)
    
    def display_board():
        displayed = game.grid[:, :, 0].copy().astype(str)
        displayed[game.grid[:, :, 1] == 0] = '■'
        displayed[game.grid[:, :, 1] == 2] = '►'
        displayed[displayed == '0'] = ''
        displayed[displayed == '-1'] = '☼'
        print(tabulate(displayed, tablefmt="grid"))
    
    while not game.end:
        display_board()
        while True:
            action = input("Action (c pour reveal / f pour flag / r pour enlever drapeau) : ")
            if action in ['c', 'f', 'r']:
                break
            print("L'action doit être c, f ou r.")

        while True:
            coords = input("Entrez les coordonnées (ligne puis colonne, ex 23) : ")
            # if len(coords) != 2:
            #     print("Les coordonnées doivent être composées de 2 caractères.")
            #     continue
            try:
                l, c = int(coords[0]), int(coords[1])
            except ValueError:
                print("Les coordonnées doivent être des nombres entiers.")
                continue
            if not (0 <= l < game.h and 0 <= c < game.w):
                print(f"Coordonnées invalides : 0 <= ligne < {game.h}, 0 <= colonne < {game.w}")
                continue
            break

        if game.first_click:
            game.init_grid((l, c))
        else:
            if action == "c":
                game.reveal_cell((l, c))
            elif action == "f":
                game.put_flag((l, c))
            elif action == "r":
                game.remove_flag((l, c))

    display_board()
    if game.revealed == game.w * game.h - game.nb_mines:
        print("Bravo ! Tu as gagné !")
    else:
        print("Perdu... tu as fait exploser une mine.")



### MODE GRAPHIQUE

class DifficultyWindow(QWidget):
    """Fenêtre de sélection de niveau pour PyQt."""
    def __init__(self, start_callback):
        super().__init__()
        self.start_callback = start_callback
        self.setWindowTitle("Choix de la difficulté")

        layout = QVBoxLayout()

        self.combo = QComboBox()
        self.combo.addItems(["Facile", "Moyen", "Difficile"])

        play_button = QPushButton("Jouer")
        play_button.clicked.connect(self.launch_game)

        layout.addWidget(QLabel("Choisissez votre niveau :"))
        layout.addWidget(self.combo)
        layout.addWidget(play_button)

        self.setLayout(layout)
        self.resize(200, 120)

    def launch_game(self):
        choice = self.combo.currentText().lower()

        difficulty = {
            "facile":  (8, 10, 10),
            "moyen":   (14, 18, 40),
            "difficile": (20, 24, 100)
        }

        h, w, mines = difficulty[choice]
        self.start_callback(h, w, mines)
        self.close()
        
def start_gui():
    """Lance l'interface graphique."""
    app = QApplication([])
    def start_game(h, w, mines):
        window = MinesweeperGUI(h, w, mines)
        window.show()
    difficulty_window = DifficultyWindow(start_game)
    difficulty_window.show()
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