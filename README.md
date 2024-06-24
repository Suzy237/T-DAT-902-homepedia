### README: Lancement de l'Application Homepedia

#### Structure du Projet

Voici les principaux répertoires et fichiers du projet:

- **app/** : Contient le code source de l'application.
- **config/** : Contient les fichiers de configuration pour Hadoop et Spark. Ce dossier n'est pas encore implémenté : TODO car le .env n'est pas toujours pris en compte (Spark ne le prend pas totalement en compte, donc besoin d'implémenter le config).
- **spark/** : Contient les Dockerfiles pour configurer les nœuds maître et travailleurs de Spark.
- **docker-compose.yml** : Fichier de configuration Docker Compose pour orchestrer les différents services.
- **.env** : Fichier d'environnement contenant les variables nécessaires à l'application.
- **app/.env** : Fichier .env spécifique à l'application.

#### Étapes de Lancement

1. **Cloner le dépôt** (si ce n'est pas déjà fait) :

   ```bash
   git clone <URL-du-dépôt> (branch fullstack-app)
   cd T-DAT-902-homepedia-fullstack-app
   ```

2. **Lancer l'application avec Docker Compose** :
   Assurez-vous d'être dans le répertoire principal du projet où se trouve le fichier `docker-compose.yml`.

   ```bash
   docker-compose up -d --force-recreate --build
   ```

3. **Accéder à l'application** :
   Une fois les conteneurs démarrés, l'application sera accessible à l'adresse suivante : `http://localhost:8000`.

4. **Accéder au site en production** :
   Le site est également accessible en production à l'adresse suivante : `http://homepedia.icaro.fr`.

#### Détails des Répertoires et Fichiers Clés

- **app/** :

  - `Dockerfile` : Définit l'image Docker pour l'application.
  - `composer.json` et `package.json` : Fichiers de gestion des dépendances pour PHP (Laravel) et JavaScript (Node.js), respectivement.
  - `public/` : Contient les fichiers accessibles publiquement (HTML, CSS, JS, etc.).
  - `resources/` : Contient les vues et autres ressources de Laravel.
  - `routes/` : Contient les définitions de routes de l'application Laravel.
  - `database/` : Contient les migrations et modèles de la base de données.
  - `python_scripts/` : Contient les scripts Python utilisés dans le projet.

- **config/** :

  - Contient les fichiers de configuration pour Hadoop et Spark nécessaires à la gestion des tâches distribuées (pas encore implémenté).

- **spark/** :
  - `init_hdfs.sh` : Script pour télécharger les scripts Python dans Hadoop.
  - `master_dockerfile` et `worker_dockerfile` : Dockerfiles pour configurer les nœuds maître et travailleurs de Spark.

### Fonctionnement des Contrôleurs

Les contrôleurs de l'application appellent Hadoop et Spark ainsi que les fonctions Python pour traiter les données. Ces contrôleurs gèrent les requêtes utilisateur, exécutent les tâches de traitement distribuées via Spark, et récupèrent les résultats. Les scripts Python situés dans `python_scripts/` sont utilisés pour le traitement des données et sont intégrés dans les workflows Spark.

### Implémentation de Leaflet pour le Front-end

Leaflet est utilisé pour la visualisation de cartes dans l'application front-end. Actuellement, l'implémentation utilise des données simulées pour afficher les cartes. Leaflet est intégré avec des composants JavaScript dans le répertoire `resources/` pour rendre les cartes interactives et afficher les données géospatiales.

### Configuration NGINX

L'application utilise un fichier de configuration NGINX (`nginx.conf`) pour le reverse proxy et la gestion des requêtes HTTP. Ce fichier est crucial pour le bon fonctionnement de l'application en production.

#### Notes Importantes

- **Liens de téléchargement des données** :
  Consultez le fichier `Liens de téléchargement des données.md` pour obtenir les datasets nécessaires au fonctionnement de l'application.

- **Scripts de configuration** :
  Utilisez les scripts fournis pour configurer Hadoop et Spark si vous prévoyez de les utiliser.

#### État d'Avancement du Projet

- [x] **DevOps** : Fonctionnel et en production, manque CI/CD et organisation GitHub.
- [x] **Front-end** : Terminé, en attente du back-end pour supprimer les données simulées.
- [x] **Scripts pour télécharger les CSV et les stocker dans Hadoop** : Fonctionnels sans Spark, échec d'implémentation avec Spark (dossier `python_scripts` dans `app`).
- [x] **Migrations dans le back-end, base de données structurée** : Voir la section ci-dessous pour plus de détails sur la base de données.
- [ ] **TODO** : Corriger Spark et son interaction avec l'application et Hadoop.
- [ ] **TODO** : Traiter les données et les insérer dans notre base de données (les données de crime vont dans MongoDB, il y a un contrôleur Mongo qui s'en charge).
- [ ] **TODO** : Implémenter les fichiers de configuration pour Hadoop et Spark dans `config/` car le `.env` n'est pas toujours pris en compte.

#### Point de Blocage -- où je me suis arrêté

L'API Spark n'accepte pas le mode de déploiement en cluster, donc nous sommes obligés de passer par notre propre API ou d'unifier les conteneurs `app` et `spark-master` pour pouvoir appeler `docker exec` sans passer par l'API. J'ai pas réussi à stocker les logs Spark de manière propre non plus.

#### Schéma et Migrations de la Base de Données

La base de données est structurée avec des migrations Laravel. Les migrations définissent le schéma de la base de données et permettent de gérer les modifications de manière versionnée. Le schéma actuel inclut des tables pour les utilisateurs, les propriétés, les transactions, etc. Les données de crime sont stockées dans une base de données MongoDB, gérée par un contrôleur dédié.

### Résumé

La majorité du travail DevOps est terminée, et l'application fullstack est presque achevée. Les deux principaux défis restants sont l'intégration de Spark, qui pose divers problèmes, et le traitement correct des données. En suivant ces instructions, vous devriez être en mesure de lancer et d'utiliser l'application Homepedia.
