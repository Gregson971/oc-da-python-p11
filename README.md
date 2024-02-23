[![oc-project-shield][oc-project-shield]][oc-project-url]

[oc-project-shield]: https://img.shields.io/badge/OPENCLASSROOMS-PROJECT-blueviolet?style=for-the-badge
[oc-project-url]: https://openclassrooms.com/fr/paths/518-developpeur-dapplication-python

# Openclassrooms - Développeur d'application Python - Projet 11

Améliorez une application Web Python par des tests et du débogage

![GÜDLFT](https://user.oc-static.com/upload/2020/09/22/16007798203635_P9.png)

## Compétences évaluées

- :bulb: Implémentez une suite de tests Python
- :bulb: Debugger le code d'une application Python
- :bulb: Gérer les erreurs et les exceptions en Python

## Installation et exécution du projet

### Pré-requis

- Avoir `Python`, `pip` et `pipenv` installé sur sa machine.

1. Cloner le repo

```sh
git clone https://github.com/Gregson971/oc-da-python-p11.git
```

2. Se placer dans le dossier oc-da-python-p11

```sh
cd /oc-da-python-p11/
```

3. Créer l'environnement virtuel

```sh
python -m venv env
```

4. Activer l'environnement virtuel \
   Si vous utilisez Mac ou Linux

```sh
source env/bin/activate
```

Si vous utilisez Windows

```sh
env\Scripts\activate.bat
```

5. Installer les packages requis

```sh
pip install -r requirements.txt
```

6. Lancer le serveur Flask

```sh
export FLASK_APP=server.py
flask run
```

Pour accéder au site, se rendre sur l'adresse par défaut : http://127.0.0.1:5000/

## Tests

### Tests unitaires / tests d'intégration

Les tests unitaires et d'intégration sont exécutés grâce à Pytest (version 8.0.1).

Pour effectuer l'ensemble des tests unitaires et d'intégration, entrer la commande :

```sh
pytest -v
```

### Tests de performance

Les tests de performance sont exécutés grâce à Locust (version 2.23.1).

Pour effectuer les tests de performance, entrer la commande :

```sh
locust -f tests/performance_tests/locustfile.py
```

Puis se rendre sur l'adresse par défaut : http://0.0.0.0:8089 pour configurer les tests.

### Couverture de code

Pour obtenir un rapport de couverture de code, entrer la commande :

```sh
pytest --cov=. --cov-report html
```

## Rapports

- [Rapport de tests](https://github.com/Gregson971/oc-da-python-p11/blob/QA/reports/tests_report.png)
- [Rapport de couverture de code](https://github.com/Gregson971/oc-da-python-p11/blob/QA/reports/coverage_report.png)
- [Rapport de performance](https://github.com/Gregson971/oc-da-python-p11/blob/QA/reports/performance_report.png)
