# Gestionnaire de tâches FastAPI

Cette application fournit une API REST pour gérer des tâches avec FastAPI et SQLite.

## Installation locale

1. Créez et activez un environnement virtuel Python.
2. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

3. Lancez l'application avec Uvicorn :

   ```bash
   uvicorn app.main:app --reload
   ```

L'API est accessible sur `http://127.0.0.1:8000`. La documentation interactive Swagger est disponible sur `http://127.0.0.1:8000/docs`.

## Lancement avec Docker

1. Construisez l'image :

   ```bash
   docker build -t gestionnaire-taches .
   ```

2. Démarrez le conteneur :

   ```bash
   docker run -p 8000:8000 gestionnaire-taches
   ```

L'API sera accessible sur `http://127.0.0.1:8000`.

## Exemples d'appels API

### Créer une tâche

```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Écrire la documentation",
    "description": "Compléter le README",
    "status": "à faire",
    "date_limite": "2024-12-31"
  }'
```

### Lister les tâches

```bash
curl http://127.0.0.1:8000/tasks
```

### Récupérer une tâche

```bash
curl http://127.0.0.1:8000/tasks/1
```

### Mettre à jour une tâche

```bash
curl -X PUT "http://127.0.0.1:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "en cours"
  }'
```

### Supprimer une tâche

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

## Tests

Lancez les tests avec :

```bash
pytest
```
