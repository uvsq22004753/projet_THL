#PROJET MT SIMULATOR 

#PARTIE 1


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
        
        
    def sous_forme_fichier(self):
        """écrit dans un fichier texte une machine turing"""
        
        f = open("machines/"+self.nom+".txt", "w")
        f.write("name : "+self.nom)
        f.write("\ninit : "+self.init)
        f.write("\naccept : "+self.accept)
        
        for i in range(0,len(self.instr),2): 

                f.write('\n'+', '.join(self.instr[i])+'\n')
                f.write(', '.join(self.instr[i+1])+'\n')
                
        f.close()

        
    
      
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
     
        
   
#print('choisir une machine de turing : ') #enumeration des fichiers dans 
#for elem in os.listdir('./machines'):     #machines
#    print(elem)
#choix = input("choix (sans le .txt) : ")
#mot = input("rentrer un mot : ")
#simulation('machines/'+ choix + '.txt', mot)

# question 5 test des machines
#simulation('machines/LEFTi.txt', '111001')
#simulation('machines/SEARCHia.txt', 'bbabba')
#simulation('machines/ERASEi.txt', '111001')
#simulation('machines/COPYij.txt', '111001')


# PARTIE 2

# on appelle de fonction apparait de cette façon dans un fichier .txt de M1 : 
    # q1, a
    # q2, M2
    
    #q1, a, _   cas où il y a plusieurs rubans
    #q1, M2, _
    
def simulation_appel(M1, M2):
    """ fonction qui simule un linker. On prend des machines faisant parties /
    de la classe MT -- pas dans l'énoncé mais une aide pour moi """
    
    
    while meme_etat(M1, M2):     #on change le nom des etats entre les deux machines 
        M2 = changer_nom_etat(M2)
    
    appel = False
    situation = [M1, appel]
    
    while M1.courant != M1.accept: 
        
        if not appel :     # dans le cas où on a une instruction qui n'appelle pas de machine
            situation = pas_a_pas_appel(M1, M2.nom)
            M1 = situation[0]
            appel = situation[1]
        
        else:  #dans le cas où on a une instruction qui utilise une autre machine
            for rubann in situation[2]:
                M2.rubans[rubann-1] = M1.rubans[rubann-1] # la machine doit reprendre là où l'on s'est arrêté
                M2.tete[rubann-1] = M1.tete[rubann-1]
                
                M1.courant = situation[3][0]  # l'état courant doit être mis à jour
            
            while M2.courant != M2.accept:  #on effectue les étapes de M2 et on met à jour M1 au fur et à mesure 
                M2 = pas_a_pas(M2)
                for rubann in situation[2]:
                    M1.rubans[rubann-1] = M2.rubans[rubann-1]
                    M1.tete[rubann-1] = M2.tete[rubann-1]
    
    M1.affichage()
    
    
def linker(M1, M2):
    """ fonction qui simule un linker. On prend des machines faisant parties /
    de la classe MT -- marche pour même  nombre de rubans -- on oublie pas /
    que l'on se place dans l'alphabet binaire"""
    
    Mres = MT('linker_'+M1.nom, M1.init, M1.accept, [], len(M1.rubans))
    
    while meme_etat(M1, M2):     #on change le nom des etats entre les deux machines 
        M2 = changer_nom_etat(M2)
    
    for i in range(0,len(M1.instr),2):
        appel = appel_existe(M1.instr[i+1], M2.nom)
        if len(appel) == 0:  # cas où on ne tombe pas sur un appel de machine
            
            Mres.instr += [M1.instr[i]]
            Mres.instr += [M1.instr[i+1]]
            
        else :  #cas où on tombe sur un appel de machine
            if len(M2.rubans) == len(M1.rubans): # si même nombre de ruban
                
                co = copy.deepcopy(M2.instr)
                for j in range(0,len(M2.instr),2):
                    if  co[j][0] == M2.init:
                        co[j][0] = M1.instr[i][0]
                    
                    if  co[j+1][0] == M2.init:
                        co[j+1][0] = M1.instr[i][0]
                
                    if  co[j+1][0] == M2.accept:
                        co[j+1][0] = M1.instr[i+1][0]
                
                    Mres.instr += [co[j]]
                    Mres.instr += [co[j+1]]
            
            else:
                for j in range(0, len(M2.instr), 2): #sinon
                    
                    for alphabet in ['1','0','_']:
                
                        base_lire = [ alphabet for i in range(len(M1.rubans)+1)]
                        base_ecrire = [alphabet for i in range(len(M1.rubans)+1)] + ['-' for i in range(len(M1.rubans))]
                    
                        base_lire[0] = M2.instr[j][0]
                        base_ecrire[0] = M2.instr[j+1][0]
                    
                        if  M2.instr[j][0] == M2.init:
                            base_lire[0] = M1.instr[i][0]
                    
                        if  M2.instr[j+1][0] == M2.init:
                            base_ecrire[0] = M1.instr[i][0]
                
                        if  M2.instr[j+1][0] == M2.accept:
                            base_ecrire[0] = M1.instr[i+1][0]
                    
                        pos_instr_M2 = 1
                    
                        for k in range(1,len(base_lire)):
                            for l in appel:
                            
                                if k == l :
                                    base_lire[k] = M2.instr[j][pos_instr_M2]

                                    base_ecrire[k] = M2.instr[j+1][pos_instr_M2]
                                    base_ecrire[k+len(M1.rubans)] = M2.instr[j+1][pos_instr_M2+len(M2.rubans)]
                                
                                    pos_instr_M2 += 1
                                
                                Mres.instr += [base_lire]
                                Mres.instr += [base_ecrire]
            
    Mres.sous_forme_fichier()
    return(Mres)
            
    
def meme_etat(M1, M2):
    """fonction qui verifie si deux machines ont bien des noms d'états/
    différents"""
    
    etat_M1 = [elem[0] for elem in M1.instr]
    etat_M2 = [elem[0] for elem in M2.instr if elem[0] not in etat_M1]
    
    if len(etat_M2) == 0:
        return True
    return False
    
    

def changer_nom_etat(machine):
    """fonction qui rajoute P au nom de chaque etat pour les différencier /
    des états d'une autre machine"""
    
    for elem in machine.instr :
        elem[0] = elem[0]+'P'
    
    machine.courant = machine.courant + 'P'
    machine.init = machine.init + 'P'
    machine.accept = machine.accept + 'P'
    
    return machine




def appel_existe(liste, nom):
    """fonction qui vérifie si l'instruction appelle l'autre machine /
    de turing et si oui renvoie l'indice à lequel on l'appel"""
    
    res = []
    for i in range(len(liste)):
        if liste[i] == nom:
            res += [i]
    return res


    
def pas_a_pas_appel(machine, nom):
    """amélioration de pas à pas pour des machines qui appellent /
    d'autres machines - marche pour même nombre de rubans"""
    
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
    
    ou = appel_existe(instruction, nom)
    
    if len(ou) != 0:
        return [machine, True, ou, instruction]
        
    if instruction == []:
        sys.exit("la machine ne reconnait pas le mot")
    machine.courant = instruction[0]
    
    for i in range(nbr_ruban):
            machine.ecrire(i, tetes[i], instruction[i+1])
            tetes[i] = machine.bouger(i, tetes[i], instruction[i+1+nbr_ruban])
    
    machine.affichage()
    return [machine, False]

M1 = initialise_MT('./machines/envers_2rubans_test.txt', '')
M2 = initialise_MT('./machines/LEFTi.txt','')
linker(M1,M2)
simulation('machines/linker_envers.txt','1000')

M3 = initialise_MT('./machines/envers_2rubans_test1.txt', '')
M4 = initialise_MT('./machines/ERASEi.txt','')
linker(M3,M4)
simulation('machines/linker_envers.txt','1000')

M5 = initialise_MT('./machines/1_par_0_test.txt', '')
M6 = initialise_MT('./machines/LEFTi.txt','')
linker(M5,M6)
simulation('machines/linker_7.0.3.txt','1000')  
