from random import *
from math import sqrt
from functools import partial
from tkinter import *
import webbrowser

class Case:
    def __init__(self, bombes_adj, bombe=bool, revele=bool, drapeau=bool):
        """crée l'objet case contenant : le numéro de la case le nombre de bombes adjacentes,
        si la case contient une bombe,si la case est révélee, si un drapeau a été posé sur la case"""
        self.bombes_adj = bombes_adj
        self.bombe = bombe
        self.revele = revele
        self.drapeau = drapeau

    def __repr__(self):
        """affiche les informations de la case"""
        return f"bombes adjacentes : {self.bombes_adj} , bombe : {self.bombe}, case révélée : {self.revele} , drapeau : {self.drapeau}"


class Grille:
    def __init__(self, difficulte):
        """constructeur"""
        #création fenêtre et frames tkinter + import textures
        self.window = Tk()
        self.window.configure(bg='#88e172')
        self.frame_i = Frame(self.window)
        self.frame_g = Frame(self.window)
        self.frame_u = Frame(self.window)
        self.pelle = PhotoImage(file='textures/pelle.png')
        self.drapeau_b = PhotoImage(file='textures/drapeau2.png')
        self.herbe = PhotoImage(file='textures/herbe.png')
        self.drapeau = PhotoImage(file='textures/drapeau.png')
        self.bombe = PhotoImage(file="textures/bombe.png")
        self.titre = PhotoImage(file='textures/titre.png')
        self.numero = [PhotoImage(file="textures/0.png"), PhotoImage(file="textures/1.png"), PhotoImage(file="textures/2.png"), PhotoImage(file="textures/3.png"), PhotoImage(file="textures/4.png"),PhotoImage(file="textures/5.png"),PhotoImage(file="textures/6.png"), PhotoImage(file="textures/7.png"), PhotoImage(file="textures/8.png")]

        # définit le nb de cases et de bombes et la taille de la grille tkinter en fonction de la difficulté
        if difficulte == 1:
            self.window.geometry("300x300-600+100")
            self.cases = 36
            self.bombes = 10
            self.drapeaux = 10

        elif difficulte == 2:
            self.window.geometry("500x550-600+40")
            self.cases = 256
            self.bombes = 40
            self.drapeaux = 40
        else:
            self.window.geometry("700x1200-500+0")
            self.cases = 576
            self.bombes = 100
            self.drapeaux = 100

        # le nombre de cases dans une ligne / colonne (pareil car grille carrée)
        self.l_t = int(sqrt(self.cases))  # = 6 / 16 / 24

        # créer grille de cases
        n = 1
        self.grille_c = self.cases * []
        for i in range(self.cases):
            self.grille_c.append(Case(0, False, False, False))
            n += 1

        # rajoute bombes
        b_places = 0
        while b_places != self.bombes:
            i = randint(1, self.cases - 1)
            if not self.grille_c[i].bombe:
                self.grille_c[i].bombe = True
                b_places += 1

        # cherche bombes adjacentes
        for j in range(self.cases):
            # trouve les indices des cases adjacentes dans la grille

            # case du haut
            if 0 <= j - self.l_t <= self.cases - 1:
                up = j - self.l_t
                if self.grille_c[up].bombe:
                    self.grille_c[j].bombes_adj += 1
                # case du coin haut gauche
                if up % self.l_t != 0:
                    if self.grille_c[up - 1].bombe:
                        self.grille_c[j].bombes_adj += 1
                # case du coin haut droit
                if (up + 1) % self.l_t != 0:
                    if self.grille_c[up + 1].bombe:
                        self.grille_c[j].bombes_adj += 1
            # case du bas
            if 0 <= j + self.l_t <= self.cases - 1:
                down = j + self.l_t
                if self.grille_c[down].bombe:
                    self.grille_c[j].bombes_adj += 1
                # case du coin bas gauche
                if down % self.l_t != 0:
                    if self.grille_c[down - 1].bombe:
                        self.grille_c[j].bombes_adj += 1
                # case du coin bas droite
                if (down + 1) % self.l_t != 0:
                    if self.grille_c[down + 1].bombe:
                        self.grille_c[j].bombes_adj += 1
            # case à gauche
            if 1 <= j - 1 <= self.cases - 1 and j % self.l_t != 0:
                if self.grille_c[j - 1].bombe:
                    self.grille_c[j].bombes_adj += 1
            # case à droite
            if 0 <= j + 1 <= self.cases - 1 and (j + 1) % self.l_t != 0:
                if self.grille_c[j + 1].bombe:
                    self.grille_c[j].bombes_adj += 1



    # visuel Tkinter
    def game(self):
        """affiche une grille, la mets à jour si modifiée, et détermine la victoire ou défaite"""
        def update(self, n):
            """s'active quand un bouton est cliqué et le met à jour (affiche drapeau, nb de bombes adjacentes ou bombe) si la condition de victoire
            ou défaite est remplie la déclare"""
            x = n // self.l_t
            y = n % self.l_t
            def mettre_drapeau(self, n):
                """pose un drapeau si il n'y en a pas déjà un, actualise le nb de drapeaux restants"""
                if not self.grille_c[n].revele:
                    if not self.grille_c[n].drapeau:
                        if self.drapeaux != 0:
                            self.grille_c[n].drapeau = True
                            #remplace l'anciend bouton par un nouveau avec un visuel différent
                            self.grille_b[n] = Button(self.frame_g, image=self.drapeau, command=partial(update, self, n))
                            self.grille_b[n].grid(row=x, column=y)
                            self.drapeaux -= 1

                    else:
                        self.grille_c[n].drapeau = False
                        # remplace l'anciend bouton par un nouveau avec un visuel différent
                        self.grille_b[n] = Button(self.frame_g, image=self.herbe, command=partial(update, self, n))
                        self.grille_b[n].grid(row=x, column=y)
                        self.drapeaux += 1



            def creuser(self, n):
                """révèle la case, déclare victoire si dernière case révélée, ou défaite si bombe révélée"""
                self.grille_c[n].revele = True
                if self.grille_c[n].bombe:
                    boom = PhotoImage(file='textures/BOOM.png')
                    #affiche toutes les bombes
                    for i in range(self.cases):
                        if self.grille_c[i].bombe:
                            x1 = i // self.l_t
                            y1 = i % self.l_t
                            self.grille_b[i] = Button(self.frame_g, image=self.bombe, command=partial(update, self, i))
                            self.grille_b[i].grid(row=x1, column=y1)
                    #écran de défaite
                    perdu = Toplevel(self.window)
                    perdu.configure(bg='#88e172')
                    perdu.geometry('-700+90')
                    perdu.iconbitmap('textures/augustin_drapeau.ico')
                    b_perdu = Button(perdu, image=boom, command=self.window.destroy)
                    b_perdu.pack()
                    perdu.mainloop()
                else:
                    # remplace l'anciend bouton par un nouveau avec un visuel différent
                    self.grille_b[n] = Button(self.frame_g, image=self.numero[self.grille_c[n].bombes_adj], command=partial(update, self, n))
                    self.grille_b[n].grid(row=x, column=y)
                    #si tous les drapeaux posés, regarde si toutes cases non minées révélée, déclare victoire si oui
                    if self.drapeaux == 0:
                        t = 0
                        for i in range(self.cases):
                            if self.grille_c[i].revele:
                                t += 1
                        if t == self.cases - self.bombes:
                            #écran victoire
                            victory = PhotoImage(file='textures/victory.png')
                            gagne = Toplevel(self.window)
                            gagne.configure(bg='#88e172')
                            gagne.iconbitmap('textures/augustin_drapeau.ico')
                            b_gagne = Button(gagne, image=victory, command=self.window.destroy)
                            b_gagne.pack()
                            gagne.mainloop()
            #création boutons pour creuser ou poser drapeau
            bouton_drapeau = Button(self.frame_u, image=self.drapeau_b, command=partial(mettre_drapeau, self, n))
            bouton_pelle = Button(self.frame_u, image=self.pelle, command=partial(creuser, self, n))
            bouton_pelle.grid(row=0, column=0)
            bouton_drapeau.grid(row=0, column=1)



        #crée grille boutons pour visuel
        self.grille_b = []
        s = 0
        for i in range(self.cases):
            if s == 0:
                if self.grille_c[i].bombes_adj == 0:
                    self.grille_b.append(Button(self.frame_g, image=self.numero[self.grille_c[i].bombes_adj], command=partial(update, self, i)))
                else:
                    s = 1
                    self.grille_b.append(Button(self.frame_g, image=self.herbe, command=partial(update, self, i)))
            else:
                self.grille_b.append(Button(self.frame_g, image=self.herbe, command=partial(update, self, i)))
        for i in range(self.l_t):
            for j in range(self.l_t):
                self.grille_b[i * self.l_t + j].grid(row=i, column=j)
        def clic(self):
            """mystère..."""
            webbrowser.open("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQsr9pjZ32fuqPGAy3QJubW7jZ4i96mNafiGg&usqp=CAU")
        Button(self.frame_i, image=self.titre,command=partial(clic, self)).pack()
        self.frame_i.pack()
        self.frame_g.pack(expand=YES)
        self.frame_u.pack()
        Label(self.frame_i, text=f"bombes à trouver : {self.bombes}").pack()
        self.window.mainloop()

    def __repr__(self):
        """affiche l'entièreté des cases et leurs informations"""
        g = ""
        c = 0
        for i in self.grille_c:
            g += f"{c}:"
            g += (str(i))
            g += "\n"
            c += 1
        return g

g = Grille(2)
g.game()
