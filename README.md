# C2 Python Server & Client

Ce projet permet de gérer un serveur C2 en Python qui communique avec plusieurs clients. Il offre la possibilité d'envoyer des commandes à un client spécifique ou à tous les clients connectés.

## Fonctionnalités
- Gestion d'une base de données pour enregistrer les clients avec un identifiant unique.
- Sélection d'un client spécifique pour envoyer des commandes.
- Changement de client actif.
- Envoi d'une commande d'attaque à tous les clients avec un paramètre d'URL et un temps défini.
- Récupération de l'identifiant d'un client qui se déconnecte.

## Installation
1. **Cloner le dépôt**
   ```sh
   git clone https://github.com/votre-utilisateur/votre-repo.git
   cd votre-repo
   ```
2. **Installer les dépendances**
   ```sh
   pip install -r requirements.txt
   ```
3. **Lancer le serveur**
   ```sh
   python server.py
   ```
4. **Lancer un client**
   ```sh
   python client.py
   ```

## Commandes du Serveur

Le serveur accepte plusieurs commandes pour interagir avec les clients :

| Commande | Description |
|----------|-------------|
| `list` | Affiche la liste des clients connectés avec leur ID. |
| `select <ID>` | Sélectionne un client spécifique pour lui envoyer des commandes. |
| `send <commande>` | Envoie une commande au client sélectionné. |
| `switch <ID>` | Change de client actif. |
| `attack <URL> <temps>` | Envoie une commande à tous les clients pour attaquer une URL pendant un temps donné. |
| `exit` | Ferme le serveur. |

## Exemple d'utilisation

1. **Lister les clients connectés**
   ```sh
   > list
   [1] Client A - 192.168.1.10
   [2] Client B - 192.168.1.15
   ```
2. **Sélectionner un client**
   ```sh
   > select 1
   Client 1 sélectionné.
   ```
3. **Envoyer une commande**
   ```sh
   > send whoami
   Réponse: root
   ```
4. **Envoyer une attaque à tous les clients**
   ```sh
   > attack http://site-cible.com 30
   Tous les clients envoient des requêtes vers http://site-cible.com pendant 30 secondes.
   ```

## Remarque
- Ce projet est à des fins éducatives uniquement.
- Vérifiez la légalité de vos actions avant d'exécuter certaines commandes.

## Auteur
Xatomm 

