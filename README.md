# Intégration Stripe Checkout avec FastAPI et Docker

Ce projet montre comment intégrer Stripe Checkout dans une application FastAPI, le tout déployé via Docker et Docker Compose. L'objectif est de fournir une solution de paiement pour une borne de recharge de véhicule électrique.

## Pré-requis

Assurez-vous d'avoir les éléments suivants installés sur votre machine :
- Docker
- Docker Compose
- Python 3.6 ou version ultérieure (si vous souhaitez exécuter le projet sans Docker)

## Structure du Projet

```
Stripe_IRVE/
├── app/
│   ├── main.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── success.html
│   │   └── cancel.html
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
```

## Configuration

### 1. Fichier `.env`

Créez un fichier `.env` à la racine du projet avec le contenu suivant :

```
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
BASE_URL=http://localhost:8000
```

Remplacez `your_stripe_public_key` et `your_stripe_secret_key` par vos clés API Stripe.

### 2. Fichier `requirements.txt`

Le fichier `requirements.txt` contient les dépendances nécessaires pour exécuter l'application FastAPI avec Stripe :

```
fastapi
uvicorn
stripe
python-dotenv
jinja2
```

### 3. Fichier `Dockerfile`

Le `Dockerfile` contient les instructions pour créer l'image Docker de l'application FastAPI :

```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app
COPY .env /app/.env

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

### 4. Fichier `docker-compose.yml`

Le fichier `docker-compose.yml` définit les services et les configurations pour exécuter l'application dans des conteneurs Docker :

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:80"
    env_file:
      - .env
    volumes:
      - ./app:/app
```

## Explications du Code

### Fichier `app/main.py`

Ce fichier contient le code principal de l'application FastAPI.

1. **Importation des modules** :
    - `fastapi`, `Request`, `HTMLResponse`, `RedirectResponse` : Modules nécessaires pour créer des routes et gérer les réponses HTTP.
    - `Jinja2Templates` : Utilisé pour rendre les templates HTML.
    - `stripe` : Bibliothèque Stripe pour gérer les paiements.
    - `os`, `load_dotenv` : Modules pour gérer les variables d'environnement.

2. **Initialisation de l'application** :
    - `app = FastAPI()` : Crée l'application FastAPI.
    - `templates = Jinja2Templates(directory="templates")` : Définit le répertoire des templates HTML.

3. **Configuration de Stripe** :
    - `stripe.api_key = os.getenv("STRIPE_SECRET_KEY")` : Initialise la clé secrète Stripe.
    - `public_key = os.getenv("STRIPE_PUBLIC_KEY")` : Récupère la clé publique Stripe.
    - `base_url = os.getenv("BASE_URL")` : Récupère l'URL de base de l'application.

4. **Routes de l'application** :
    - `@app.get("/")` : Route pour la page d'accueil, rend le template `index.html`.
    - `@app.post("/create-checkout-session")` : Route pour créer une session de paiement Stripe et rediriger l'utilisateur vers la page de paiement Stripe.
    - `@app.get("/success")` : Route pour la page de succès après un paiement réussi, rend le template `success.html`.
    - `@app.get("/cancel")` : Route pour la page d'annulation après un paiement annulé, rend le template `cancel.html`.

### Templates HTML

1. **`index.html`** : Page d'accueil avec un formulaire pour initier un paiement.

2. **`success.html`** : Page affichée après un paiement réussi.

3. **`cancel.html`** : Page affichée après un paiement annulé.

## Démarrage de l'Application

1. **Construire l'image Docker** :
   ```bash
   docker-compose build
   ```

2. **Démarrer les services** :
   ```bash
   docker-compose up -d
   ```

Accédez à `http://localhost:8000` pour voir la page de paiement Stripe en action.

## Tester l'Application

Pour tester l'application, suivez ces étapes :

1. **Ouvrir le navigateur** : Accédez à `http://localhost:8000`.
2. **Démarrer une session de paiement** : Cliquez sur le bouton "Checkout" pour initier une session de paiement.
3. **Compléter le paiement** : Utilisez les informations de test Stripe pour compléter le paiement.
4. **Vérifier la redirection** : Après le paiement, vous devriez être redirigé vers la page de succès. En cas d'annulation, vous serez redirigé vers la page d'annulation.

## Conclusion

Ce projet montre comment intégrer Stripe Checkout avec FastAPI et Docker pour gérer les paiements en ligne de manière sécurisée et efficace. En suivant les instructions ci-dessus, vous pouvez facilement déployer cette solution et l'adapter à vos besoins spécifiques.

### Explications des Composants et des Étapes

#### 1. Création du Fichier `.env`

Ce fichier contient les informations sensibles comme les clés API Stripe et l'URL de base de votre application. Il est essentiel de ne pas inclure ce fichier dans votre contrôle de version pour des raisons de sécurité.

#### 2. Configuration du Fichier `requirements.txt`

Ce fichier liste toutes les bibliothèques Python nécessaires à l'exécution de l'application, permettant à Docker d'installer automatiquement ces dépendances lors de la construction de l'image.

#### 3. Création du `Dockerfile`

Le `Dockerfile` contient les instructions nécessaires pour construire une image Docker de votre application. Il inclut les étapes pour copier les fichiers de l'application, installer les dépendances, et définir la commande de démarrage de l'application.

#### 4. Configuration de `docker-compose.yml`

Ce fichier permet de définir et de gérer plusieurs conteneurs Docker en une seule commande. Ici, il configure le service web, mappe les ports, et définit le fichier `.env` à utiliser.

#### 5. Explication du Code dans `main.py`

- **Initialisation** : Importation des modules nécessaires et initialisation de l'application et des templates.
- **Configuration de Stripe** : Chargement des clés API Stripe à partir des variables d'environnement.
- **Définition des Routes** : Création des routes pour gérer l'affichage de la page d'accueil, la création de sessions de paiement, et les pages de succès et d'annulation.

#### 6. Utilisation des Templates HTML

- **`index.html`** : Contient le formulaire pour initier un paiement.
- **`success.html` et `cancel.html`** : Pages de redirection après le paiement, pour informer l'utilisateur du succès ou de l'annulation du paiement.

### Instructions pour Tester l'Application

1. **Construire l'image Docker** : La commande `docker-compose build` construit l'image Docker en utilisant le `Dockerfile`.
2. **Démarrer les services** : La commande `docker-compose up -d` démarre les services définis dans `docker-compose.yml`.
3. **Accéder à l'application** : En visitant `http://localhost:8000`, vous pouvez tester l'interface de paiement.
