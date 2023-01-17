#PROJET MT SIMULATOR 
import sys
from colorama import Fore, Style
import copy
import os

def lecture_machine(fichier): # "machines/nomfichier.txt"
    """renvoie sous forme de dictionnaire la machine de turing avec /
    ses instructions écrites comme dans machine turing simulator"""
    
    res = {"name" : '' , "init" : '', "accept" : '', "instr" : list()} #initialisation
    f = open(fichier, "r")
    
    for line in f:
        ajout = line.rstrip()
        
        if ajout.startswith("name"):
            res["name"] = ajout.split(':')[1].strip()
            
        elif ajout.startswith("init"):
            res["init"] = ajout.split(':')[1].strip()      #on enlève tous les espaces
            
        elif ajout.startswith("accept"):
            res["accept"] = ajout.split(':')[1].strip()    #on enlève tous les espaces
            
        else :
            if ajout != '' :                               #on ne prend pas en compte les lignes vides
                instruction = line.split(',')              #on sépare au niveau des virgules
                instruction = enlever_espace(instruction)
                res["instr"].append(instruction)
            
    f.close()
    return res



def enlever_espace(liste):
    """ enleve les espaces avant / apres chaque element de la liste"""
    
    res = list()
    for elem in liste :
        res.append(elem.strip())
    return res



def nombre_ruban(def_MT):
    """ fonction qui renvoie le nombre de ruban utilisé par la MT"""
    
    return len(def_MT['instr'][0])-1 



class MT(object):
    
    def __init__(self, nom, init, accept, instr, rubans) :
        
        self.nom = nom
        self.init = init
        self.accept = accept
        self.instr = instr
        self.rubans = [[] for i in range(rubans)]  #etat des bandes 
        self.courant = init                  # etat courant
        self.tete = [0 for i in range(rubans)]  #place de la tete de lecture pour chaque ruban dans l'ordre
        
        
    def mot(self, mot):
        """ met le mot sur le premier ruban de la machine de turing et /
        initie les autres rubans à un carré blanc """
        
        for i in range(len(self.rubans)):
            if i == 0:
                self.rubans[0] = list(mot)
            else :
                self.rubans[i] = ['_']
     
    
    def lire(self, i, j):
        """lit le caractère courant sur le ruban i place j"""
        
        rubans = self.rubans
        ruban = rubans[i]  # ruban i
        if 0 <= j < len(ruban): # on regarde si l'element que l'on veut lire est un carre vide ou une lettre
            return ruban[j]
        else:
            return '_'
        
    def ecrire(self, i, j, c):
        """ecrit le caractère c sur le ruban i à la place j"""
        
        rubans = self.rubans
        ruban = rubans[i]
        
        if c == '-':
            return ruban
        
        elif j < 0 :     #cas ou on veut inserer à gauche du ruban
            res = [c] + ruban
            
        else:
            ruban[j] = c
            res = ruban
        
        return res
    
    def bouger(self, i, j, inst):
        """ fonction qui donne la nouvelle tete du ruban i en fonction de /
        l'instruction donnée """
        
        if inst == '>' : 
            if j+1 == len(self.rubans[i]):
                self.rubans[i] = self.rubans[i] + ['_']
            return j+1
        
        elif inst == '-':
            return j
        
        elif inst == '<':
            if j == 0 :
                self.rubans[i] = ['_'] + self.rubans[i]
                return j 
            else :
                return j-1
                
        
    def affichage(self):
        """affiche l'état actuel de la machine de Turing ainsi que les bandes/
        avec en bleu la tête de lecture """
        
        print('etat courant : ' + self.courant)
        
        co = copy.deepcopy(self.rubans)
        for i in range(len(co)):
            for j in range(len(co[i])):
                c = self.tete[i]
                if j == c :
                    co[i][j] = Fore.BLUE + Style.BRIGHT + co[i][j] + Fore.RESET + Style.RESET_ALL
            print(', '.join(co[i]))
        print('\n')

        
    
      
def initialise_MT(fichier_MT, mot):
    """fonction qui initialise une machine de turing et renvoie l'état courant/
    l'état des bandes et la position des têtes de lecture"""
    
    info_MT = lecture_machine(fichier_MT)
    ruban = nombre_ruban(info_MT)
    
    res = MT (info_MT['name'],info_MT['init'], info_MT['accept'], info_MT['instr'], ruban )
    res.mot(mot)
    return res
       


def pas_a_pas(machine):
    """ fonction qui effectue une etape de calcul """
    
    etat = [machine.courant]
    tetes = machine.tete
    choix_instr = machine.instr
    nbr_ruban = len(tetes)
    
    for i in range(nbr_ruban):                # on lit chaque tete sur chaque ruban
        etat.append(machine.lire(i, tetes[i]))
    
    instruction = []                           # on cherche l'instruction soeur que l'on doit effectuer
    for i in range(0,len(choix_instr),2):
        if egalite(choix_instr[i],etat):
            instruction = choix_instr[i+1]
    if instruction == []:
        sys.exit("la machine ne reconnait pas le mot")
    machine.courant = instruction[0]
    
    for i in range(nbr_ruban):
            machine.ecrire(i, tetes[i], instruction[i+1])
            tetes[i] = machine.bouger(i, tetes[i], instruction[i+1+nbr_ruban])
    
    machine.affichage()
    return machine



def egalite(liste1, liste2):
    """ fonction qui renvoie true si les deux listes sont identiques"""
    if len(liste1) != len(liste2):
        return False 
    for i in range(len(liste1)):
        if liste1[i] != liste2[i]:
            return False
    return True


def simulation(fichier_MT, mot):
    """ simule le calcul de la machine de Turing jusqu'à atteindre l'état final"""
    
    MT = initialise_MT(fichier_MT, mot)
    print('\n'+'nom : '+ MT.nom)
    print('etat initiale : ' + MT.init)
    print('etat final : ' + MT.accept)
    
    co = copy.deepcopy(MT.rubans)
    for i in range(len(co)):
        for j in range(len(co[i])):
            c = MT.tete[i]
            if j == c :
                co[i][j] = Fore.BLUE + Style.BRIGHT + co[i][j] + Fore.RESET + Style.RESET_ALL
        print(', '.join(co[i]))
    print('\n')
    while MT.courant != MT.accept:
        MT = pas_a_pas(MT)
    
    print('mot reconnu ! ')
     
        
   
print('choisir une machine de turing : ') #enumeration des fichiers dans 
for elem in os.listdir('./machines'):     #machines
    print(elem)
choix = input("choix (sans le .txt) : ")
mot = input("rentrer un mot : ")
simulation('machines/'+ choix + '.txt', mot)

# question 5 test des machines
#simulation('machines/LEFTi.txt', '111001')
#simulation('machines/SEARCHia.txt', 'bbabba')
#simulation('machines/ERASEi.txt', '111001')
#simulation('machines/COPYij.txt', '111001')


    