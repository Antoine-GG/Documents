import json

class Moteur:
  def __init__(self, isVitGauche, isVitDroite, isDirDroite, isDirGauche):
    self.isVitGauche = isVitGauche
    self.isVitDroite = isVitDroite
    self.isDirDroite = isDirDroite
    self.isDirGauche = isDirGauche
  #Ceci permet de print le contenu de l'objet et non son adresse mémoire
  def __str__(self):
      return f"isDirGauche: {self.isDirGauche}, isVitGauche: {self.isVitGauche}, isDirDroite: {self.isDirDroite}, isVitDroite: {self.isVitDroite},"

#JSON string, exemple de réception POST (request.json)
trajectoireJson = '''[
    {"isDirGauche":true, "isVitGauche":true, "isDirDroite":true, "isVitDroite":true},
    {"isDirGauche":true, "isVitGauche":true, "isDirDroite":true, "isVitDroite":true},
    {"isDirGauche":false, "isVitGauche":true, "isDirDroite":true, "isVitDroite":true},
    {"isDirGauche":false, "isVitGauche":true, "isDirDroite":true, "isVitDroite":true},
    {"isDirGauche":false, "isVitGauche":true, "isDirDroite":false, "isVitDroite":true},
    {"isDirGauche":false, "isVitGauche":true, "isDirDroite":false, "isVitDroite":true}
  ]'''

#Transforme le json en Array de dictionnaires
trajectoire = json.loads(trajectoireJson)

#Debug
print(f"Trajectoire Zero: {trajectoire[0]}")
print(f"Trajectoire Un: {trajectoire[1]}")

#Pour chaque dictionnaire de l'Array
for etape in trajectoire:
  #Transforme le dictionnaire en objet
  moteur = Moteur(etape['isDirGauche'], etape['isVitGauche'], etape['isDirDroite'], etape['isVitDroite'])
  #Debug
  print(f"Étape: {etape}")
  print(f"Moteur: {moteur}")