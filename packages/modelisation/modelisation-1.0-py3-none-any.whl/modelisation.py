# Bibliothèque pour modéliser des graphiques
# Version 1.0 du 05/07/2024
# Stéphane LAURENT (Lycée Valin (17))

# la touche 'Suppr' supprime la modélisation en cours
# la touche 'espace' affiche/ masque un réticule
# la touche 'm' affiche/ masque la légende de la modélisation


import matplotlib.pyplot as plt # importation d'un sous module (pyplot) de la bibliothèque matplotlib sous le nom plt
plt.rcParams['toolbar'] = 'None'
import numpy as np # Importation du module numpy afin de lire le contenu du fichier csv
from scipy.optimize import curve_fit
from matplotlib.path import Path
from matplotlib.widgets import LassoSelector
from matplotlib.widgets import Cursor    # pour afficher un réticule
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import warnings

# Bibliothèque  facultative
try:
    import addcopyfighandler  # pour copier la graphique dans le presse papier avec ctrl C
except:
    pass


class Modelisation:
    def __init__(self, modele_choisi, x, y, kwargs):
        self.x = x
        self.y = y
        self.modele_choisi = modele_choisi
        self.parametre = kwargs
                
        
        def onSelect(points_lasso):
            
            try:
                self.message_erreur.remove()
            except:
                pass
            
            self.ind = []
            path = Path(points_lasso)
            self.ind = np.nonzero(path.contains_points(self.tableau_points))[0]
            
            canvas.draw_idle()
            modelisation_points_lasso()
        
        
        def selection_lasso(x1, y1):
            
            # mettre les points du graphique en tableau Numpy [[x1 y1] [x2 y2]...]
            self.tableau_points = []
            l2 = []
            for i in range(len(x1)):
                l1 = []
                l1.append(x1[i])
                l1.append(y1[i])
                l2.append(l1)
            
            self.tableau_points = np.asarray(l2)
            self.lasso = LassoSelector(ax=plt.gca(), onselect=onSelect, props = {'color' : 'red', 'linewidth': 1.5, 'alpha': 0.8})
        
        
        def effacer_modelisation():
            
            # effacer la modélisation précédente si elle existe
            
            try:     
                a_supprimer = self.points_modelisation.pop() # supprimer la dernière droite affichée
                a_supprimer.pop().remove()
                
                self.legende.remove()
                
                if self.modele_choisi == "double_affine" and self.nbr_modelisation >= 1: # afficher la legende de la première droite
                    self.nbr_modelisation -=1
                    plt.gca().legend(handles=self.points_modelisation[0])
                    self.legende = plt.legend(loc = 'upper left', title = self.titre_legende, title_fontsize='large')
                    self.legende._legend_box.align = "left"
            except:
                pass
            
            plt.gcf().canvas.draw()
                
        
        def modelisation_points_lasso():
            
            xx = []
            yy = []
            
            for i in range(len(self.ind)):
                xx.append(self.x[self.ind[i]])
                yy.append(self.y[self.ind[i]])
            
            if len(xx) > 1: # il faut au moins deux points pour modéliser
                
                if self.modele_choisi != "double_affine":
                    effacer_modelisation()
                
                if self.modele_choisi == "lineaire" or self.modele_choisi == "linéaire":
                    afficher_modele_lineaire(xx, yy)
                
                if self.modele_choisi == "affine" :
                    afficher_modele_affine(xx, yy)
                
                if self.modele_choisi == "parabole" :
                    afficher_modele_parabole(xx, yy)
                    
                if self.modele_choisi == "exp_decroissante" :
                    afficher_modele_exp_decroissante(xx, yy)
                    
                if self.modele_choisi == "exp_croissante" :
                    afficher_modele_exp_croissante(xx, yy)
                
                if self.modele_choisi == "double_affine" :
                    
                    if self.nbr_modelisation < 2:
                        self.nbr_modelisation +=1
                        afficher_modele_affine(xx, yy)
                        
                    if self.nbr_modelisation == 2:
                        self.nbr_modelisation +=1
                        effacer_modelisation()
                        afficher_modele_affine(xx, yy)
                    
            return

             
        def touche_clavier(event):
            
            if event.key == "delete":
                effacer_modelisation()
                
                try:
                    self.message_erreur.remove()
                    plt.gcf().canvas.draw()
                except:
                    return
            
             #--------- Afficher / masquer un réticule libre ----------
            if event.key == " ": # barre d'espace
                
                if reticule.visible == False:           
                    reticule.visible = True
                    
                else:
                    reticule.visible = False
                                       
                                       
                plt.gcf().canvas.draw()
                
            #----------- Afficher / masquer la légende -------------- 
            
            if event.key == "m":
                try:
                    plt.gca().get_legend().set_visible(not plt.gca().get_legend().get_visible()) 
                    plt.gcf().canvas.draw()
                except:
                    pass
                
        
            
        
        def affichage_message_erreur(texte_erreur):
            self.message_erreur=plt.figtext(0.5, 0.5, texte_erreur, fontsize = 16, fontweight = 'bold', color = 'red', backgroundcolor = 'yellow',horizontalalignment = 'center', verticalalignment = 'center')
           
             
        
        
        def afficher_modele_lineaire(x1,y1):
            global a
            try:
                popt,pcov = curve_fit(lineaire, x1, y1) 
                a = popt[0]
                
                xmin, xmax = plt.gca().xaxis.get_view_interval() # valeurs extrêmes sur l'axe des x
                x_modelisation = np.linspace(0, xmax)
                y_modelisation = a * x_modelisation
                
                titre_legende = '$\\bf{y = a\/x}$'
                caracteristiques_modele = "a = " + "{0:.3g}".format(a)
                afficher_modelisation(x_modelisation, y_modelisation, titre_legende, caracteristiques_modele)
               
            except:
                affichage_message_erreur('Modélisation impossible !')
            return 
        
        def afficher_modele_affine(x1, y1):
            global a, b
            try:
                popt,pcov = curve_fit(affine, x1, y1) 
                a = popt[0]
                b = popt[1]
                
                xmin, xmax = plt.gca().xaxis.get_view_interval() # valeurs extrêmes sur l'axe des x
                x_modelisation = np.linspace(xmin, xmax)
                y_modelisation = a * x_modelisation + b
                      
                titre_legende = '$\\bf{y = a\/x + b}$'
                caracteristiques_modele = "a = " + "{0:.3g}".format(a) + "\nb = " + "{0:.3g}".format(b)
                afficher_modelisation(x_modelisation, y_modelisation, titre_legende, caracteristiques_modele)
            except:
                 affichage_message_erreur('Modélisation impossible !')
            return
         
        def afficher_modele_parabole(x1, y1):
            global a, b, c
            try:
                popt,pcov = curve_fit(parabole, x1, y1) 
                a = popt[0]
                b = popt[1]
                c = popt[2]
                
                xmin, xmax = plt.gca().xaxis.get_view_interval() # valeurs extrêmes sur l'axe des x
                x_modelisation = np.linspace(xmin, xmax)
                y_modelisation = a * x_modelisation**2 + b * x_modelisation + c
                
                titre_legende = '$\\bf{y = a\/x² + b\/x + c}$'
                caracteristiques_modele = "a = " + "{0:.3g}".format(a) + "\nb = " + "{0:.3g}".format(b) + "\nc = " + "{0:.3g}".format(c)
                afficher_modelisation(x_modelisation, y_modelisation, titre_legende, caracteristiques_modele)
            except:
                affichage_message_erreur('Modélisation impossible !')
            return 
        
        
        def afficher_modele_exp_decroissante(x1, y1):
            global a, b
            try:
                popt,pcov = curve_fit(exp_decroissante, x1, y1) 
                a = popt[0]
                b = popt[1]
                
                xmin, xmax = plt.gca().xaxis.get_view_interval() # valeurs extrêmes sur l'axe des x
                x_modelisation = np.linspace(xmin, xmax)
                y_modelisation = a * np.exp(-b * x_modelisation)
                
                titre_legende = '$\\bf{y = a\/\/exp(-bx )}$'
                caracteristiques_modele = "a = " + "{0:.3g}".format(a) + "\nb = " + "{0:.3g}".format(b)
                afficher_modelisation(x_modelisation, y_modelisation, titre_legende, caracteristiques_modele)
            except:
                affichage_message_erreur('Modélisation impossible !')
            return


        def afficher_modele_exp_croissante(x1, y1):
            global a, b
            try:
                popt,pcov = curve_fit(exp_croissante, x1, y1) 
                a = popt[0]
                b = popt[1]
                
                xmin, xmax = plt.gca().xaxis.get_view_interval() # valeurs extrêmes sur l'axe des x
                x_modelisation = np.linspace(xmin, xmax)
                y_modelisation = a * (1 - np.exp(-b * x_modelisation)) 
                
                titre_legende = '$\\bf{y = a\/\/(1 - exp(-bx))}$'
                caracteristiques_modele = "a = " + "{0:.3g}".format(a) + "\nb = " + "{0:.3g}".format(b)
                afficher_modelisation(x_modelisation, y_modelisation, titre_legende, caracteristiques_modele)
            except:
                affichage_message_erreur('Modélisation impossible !')
            return

        
        ### Modélisation ###

        def lineaire(x, a):
            return a * x

        def affine(x, a, b):
            return a * x + b

        def parabole(x, a, b, c):
            return a * x**2 + b*x + c

        def exp_decroissante(x, a, b):
            return a * np.exp(-b * x)

        def exp_croissante(x, a, b):
            return a * (1 - np.exp(-b * x)) 
        
        
        def afficher_modelisation(x_modelisation, y_modelisation, titre_legende, caracteristiques_modele):
            
            if self.modele_choisi == "double_affine":
                if self.nbr_modelisation > 1:
                    couleur = self.parametre.get('color2', 'green')
                else:
                    couleur = self.parametre.get('color', 'mediumblue')
            else:
                couleur = self.parametre.get('color', 'black')
                
            style_ligne = self.parametre.get('linestyle', 'dashed') #valeurs possibles : 'solid', 'dashed', 'dashdot', 'dotted'
            taille_ligne = float(self.parametre.get('linewidth', 1.5))
            
            self.points_modelisation.append(plt.plot(x_modelisation, y_modelisation, color=couleur, linestyle= style_ligne, linewidth=taille_ligne, label = caracteristiques_modele))
            
            self.legende = plt.legend(loc = 'upper left', title = titre_legende, title_fontsize='large')
            self.legende._legend_box.align = "left"
            
    
        
        ######################################################################
        
        self.points_modelisation = []
        
        self.modele_choisi = self.modele_choisi.strip() # supprime les espaces surperflus
        self.modele_choisi = self.modele_choisi.lower()
        
        liste_nom_modele_possible = ["exp croissante", "exp-croissante", "expcroissante"]
        if self.modele_choisi in liste_nom_modele_possible:
            self.modele_choisi = "exp_croissante"
        
        liste_nom_modele_possible = ["exp decroissante", "exp-decroissante", "exp décroissante", "exp-décroissante", "exp_décroissante", "expdécroissante", "expdecroissante"]
        if self.modele_choisi in liste_nom_modele_possible:
            self.modele_choisi = "exp_decroissante"
            
        if self.modele_choisi == "double-affine" or self.modele_choisi == "double affine":
            self.modele_choisi = "double_affine"
        
        
        if self.modele_choisi == "lineaire" or self.modele_choisi == "linéaire":
            afficher_modele_lineaire(self.x, self.y)
            selection_lasso(self.x, self.y)        
        
                
        elif self.modele_choisi == "affine":
            afficher_modele_affine(self.x, self.y)
            selection_lasso(self.x, self.y)              
            
        
        elif self.modele_choisi == "parabole":
            afficher_modele_parabole(self.x, self.y)
            selection_lasso(self.x, self.y)
            
        
        elif self.modele_choisi == "exp_decroissante":
            afficher_modele_exp_decroissante(self.x, self.y)
            selection_lasso(self.x, self.y)
            
            
        elif self.modele_choisi == "exp_croissante":
            afficher_modele_exp_croissante(self.x, self.y)
            selection_lasso(self.x, self.y)
             
        
        elif self.modele_choisi == "double_affine":
            self.nbr_modelisation = 0 # nombre de droite modélisées pour "double_affine"
            selection_lasso(self.x, self.y)
            
        else:
            affichage_message_erreur('Modélisation impossible\nmodèle inconnu !')
            
        canvas = plt.gca().figure.canvas
        plt.gcf().set_size_inches(10, 7.5)
        plt.gcf().canvas.manager.set_window_title('Modélisation V1.0')
        plt.gcf().canvas.mpl_connect("key_press_event", lambda e:touche_clavier(e))
        
        #### personnaliser la barre de navigation ####
        
        NavigationToolbar2Tk.toolitems = (
            ('Home', "Réinitialiser la vue d'origine", 'home', 'home'),
            ('Back', 'Retour à la vue précédente', 'back', 'back'),
            ('Forward', 'Passer à la vue suivante', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Déplacer avec le bouton gauche de la souris, zoom avec le droit', 'move', 'pan'),
            ('Zoom', 'Zoomer sur un rectangle', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
            ('Save', 'Enregistrer le graphique', 'filesave', 'save_figure'),
            )
        
        self.toolbar = NavigationToolbar2Tk(canvas) 
        self.toolbar.children['!button4'].pack_forget() # Supprimer un bouton
        

def modele(modele, x, y, **kwargs):
    global a, b, c
    a = ""
    b = ""
    c = ""
    
    objet = Modelisation(modele, x, y, kwargs) # pour assurer la compatibilité avec les versions précédentes
    
    
    if b != "" and c == "":
        return a, b
    elif b != "" and c != "":
        return a, b, c
    else:
        return a
    

reticule = Cursor(plt.gca(), useblit=True, color='black', linewidth=1, linestyle='dashed')
reticule.visible = False

warnings.filterwarnings(action='ignore') # empêcher l'affichage d'avertissement Python