# T-DAT-902-homepedia

## Prérequis
- Télécharger les données grâce aux liens fournis dans le fichier  
[Liens de téléchargement des données.md]()  

- Créer un répertoire `data` et y mettre fichiers téléchargés et dézippés
## Scapping.py :
[Bien dans ma ville]("https://www.bien-dans-ma-ville.fr/classement-ville/") site de référence de la donnée

⚠️ Certaines données ne sont pas complétement rangées, en raison de l'harchitecture du site. 
Elles sont dans ce cas sauvegardé en brute. 
**Scrappingwithlxml.py** est un version améliorée en cours de Scapping.py
Les deux permettent d'obtenir les liens de toutes les pages du site. 
**test_thread.py** Lance le parting de toutes les pages et récupère la donnée sous format json
