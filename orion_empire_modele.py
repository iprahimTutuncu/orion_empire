import random

import math
from helper import Helper as hlp
from mathPlus import *

###
from c_Barrack import *
from c_Mine import *
from c_Ville import *
from c_Pulsar import *
from c_Planete import *
from c_Etoile import *
from c_Systeme import *
from c_Vaisseau import *
from c_Ferme import *
from c_Generatrice import *
from c_StationGalactique import *  ###########################################################  MODIF TRISTAN
from c_Joueur import *
from c_IA import *


class Modele():
	def __init__(self, parent, joueurs, dd):
		self.parent = parent
		self.id = Id.prochainid()
		# self.createurId=self.parent.createurId
		self.diametre, self.densitestellaire, qteIA = dd
		self.nbsystemes = int(self.diametre ** 2 / self.densitestellaire)
		print(self.nbsystemes)
		self.ias = []  # IA
		self.joueurs = {}
		self.joueurscles = joueurs
		self.actionsafaire = {}
		self.pulsars = []
		self.systemes = []
		self.terrain = []
		self.creersystemes(int(qteIA))  # nombre d'ias a ajouter

	def creersystemes(self, nbias):  # IA ajout du parametre du nombre d'ias a ajouter

		for i in range(self.nbsystemes):
			x = random.randrange(self.diametre * 10) / 10
			y = random.randrange(self.diametre * 10) / 10
			self.systemes.append(Systeme(self, x, y))

		for i in range(math.floor(
						self.nbsystemes / 3)):  # -------------- ajoute un nombre de pulsars dependant du nombre de systemes
			x = random.randrange(self.diametre * 10) / 10
			y = random.randrange(self.diametre * 10) / 10
			self.pulsars.append(Pulsar(self, x, y))

		liste = []
		for p in self.pulsars:
			liste.append(p)

		index = 0

		while index < len(self.pulsars):
			p = random.choice(liste)
			if len(liste) == 1 or p != self.pulsars[index]:
				self.pulsars[index].destination = p
				liste.remove(p)
				index += 1

		np = len(self.joueurscles) + nbias  # on ajoute le nombre d'ias
		planes = []
		systemetemp = self.systemes[:]

		#
		# Test d'asignation de systemes meres
		#

		while np:
			p = random.choice(systemetemp)
			if p not in planes and len(p.planetes) > 0:  # Premirer planete entre automatiquement
				if len(planes) == 0:
					planes.append(p)
					systemetemp.remove(p)
					np -= 1
				else:
					ok = True
					for sy in planes:
						a = hlp.calcDistance(sy.x, sy.y, p.x, p.y)
						if a < self.diametre / 50 * self.densitestellaire:  # Verifi distance entre planete choisi et autres planetes
							ok = False
							break
					if ok:
						planes.append(p)
						systemetemp.remove(p)
						np -= 1

		couleurs = ["cyan", "goldenrod", "orangered", "greenyellow",
		            "dodgerblue", "yellow2", "maroon1", "chartreuse3",
		            "firebrick1", "MediumOrchid2", "DeepPink2", "blue"]  # IA ajout de 3 couleurs

		for i in self.joueurscles:
			self.joueurs[i] = Joueur(self, i, planes.pop(0), couleurs.pop(0))

		for i in range(nbias):  # IA
			nomia = "IA_" + str(i)
			self.joueurscles.append(nomia)
			ia = IA(self, nomia, planes.pop(0), couleurs.pop(0))
			self.joueurs[nomia] = ia  # IA
			self.ias.append(ia)  # IA

	def creervaisseauGalactique(self, systeme):  # ! Changer nom
		self.parent.actions.append([self.parent.monnom, "creervaisseauGalactique", systeme])

	def creerstationGalactique(self,
	                           systeme):  #############################################################  MODIF TRISTAN
		self.parent.actions.append([self.parent.monnom, "creerstationGalactique", systeme])

	def prochaineaction(self, cadre):  # Loop
		if cadre in self.actionsafaire:
			for i in self.actionsafaire[cadre]:
				self.joueurs[i[0]].actions[i[1]](i[2])
			del self.actionsafaire[cadre]

		for i in self.joueurscles:
			self.joueurs[i].prochaineaction()

		for i in self.ias:
			i.analysesituation()

		for i in self.pulsars:
			i.evoluer()

		for i in self.systemes:
			for p in i.planetes:
				p.orbiter()

		self.parent.vue.modecourant.updateRessources(self.joueurs[self.parent.monnom])  # !

	def changeetatsystem(self, nom, systeme):  # ! ------------------------------ AJOUTER M�THODE
		self.parent.changeetatsystem(nom, systeme)

	def changerproprietaire(self, nom, couleur, syst):
		self.parent.changerproprietaire(nom, couleur, syst)

	def dechargerVaisseauGalactique(self, id,
	                                systeme):  # ! ------------------------------------------------------ METHODE A AJOUTER
		self.parent.actions.append([self.parent.monnom, "dechargervausseaugalactique", (id, systeme)])
		# print("ENVOIE DEMANDE DECHARGEMENT")

	def upgradeVitesseVaisseau(self, id, boost):  # ! MODIF ICI
		# print("DEMANDE UPGRADE VITESSE VAISSEAU",id)
		self.parent.actions.append([self.parent.monnom, "upgradevitessevaisseau", (id, boost)])

	def chargedansvaisseaugalactique(self, vg, vs):
		self.parent.actions.append([self.parent.monnom, "chargedansvaisseaugalactique", (vg, vs)])