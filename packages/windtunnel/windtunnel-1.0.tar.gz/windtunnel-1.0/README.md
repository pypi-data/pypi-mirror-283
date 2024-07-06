# WindTunnel

Ce package permet de faire le shift de la journée

## Table des matières

- [Description](#description)
  - [Résumé du process métier via tunn3l](#résumé-du-process-métier-via-tunn3l)
  - [Résumé du process métier via les csv](#résumé-du-process-métier-via-les-csv)
- [Exécution en main()](#exécution-en-main)
  - [Prise en main rapide](#prise-en-main-rapide)
  - [Configuration](#configuration)
    - [Configuration avec les fichiers csv](#configuration-avec-les-fichiers-csv)
      - [Fichier staff](#fichier-staff)
      - [Fichier timeslots](#fichier-timeslots)
    - [Configuration avec le backoffice tunn3l csv](#configuration-avec-le-backoffice-tunn3l)
  - [Exécution en main()](#exécution-en-main)
- [Exécution en package](#exécution-en-package)
  - [Package utilisé avec tunn3l](#package-utilisé-avec-tunn3l)
  - [Package utilisé avec les csv](#package-utilisé-avec-les-csv)
- [Règles métier](#règles-métier)
- [Limitations](#limitations)

## Description

Ce package permet de faire le shift depuis deux sources de données au choix:
- soit depuis des fichiers csv que vous devrez fournir pour indiquer le staff et les timeslots
- soit en se connectant à votre backoffice tunn3l avec vos données d'authentification

Le package a 2 environnements possibles de lancement:
- Soit il est exécuté en soi en lançant son __init__.py
- Soit il est utilisé comme package avec son bagage de fonctions pour réaliser toutes les étapes nécessaires à la réalisation du shift

### Résumé du process métier via tunn3l

- On demande à l'utilisateur les données d'authentification tunn3l
- On récupère la liste des employés dans  tunn3l et on l'affiche au user
- On demande au user qui parmi les employés on doit utiliser pour le staff
- On récupère la liste des timeslots dans tunn3l
- On fait le shift et on l'affiche à l'utilisateur avec le compteur de staff

### Résumé du process métier via les csv

- On demande à l'utilisateur les fichiers csv
- On récupère la liste de staffs depuis son fichier csv
- On récupère la liste de timeslots depuis son fichier csv
- On fait le shift et on l'affiche à l'utilisateur avec le compteur de staff

## Exécution en main()

### Prise en main rapide

- Faire un fichier .env sur le modèle du .env.example,
- y éditer vos données tunn3l ou l'emplacement des fichiers csv
- pour une utilisation via les fichiers csv, créer vos fichiers csv staffs et timeslots sur la même structure que les 2 fichiers en exemples
- dans le dossier du package lancer le __init__.py et se laisser guider

```sh
cd windtunnel
py __init__.py
```


### Configuration

- Copier le fichier ".env.example" à la racine du projet, le renommer ".env ".
- Editer le .env selon votre choix de source de données, csv ou tunn3l

#### Configuration avec les fichiers csv

Si vous utilisez les fichiers csv, il faudra un fichier pour le staff et un autre fichier pour les timeslots.

##### Fichier staff

- séparateur ","
- 1 ligne = 1 instructeur
- Structure:
  - name: nom de l'instructeur à afficher sur le shift, conseillé au format "Prénom N".
  - working_ranges: liste des créneaux horaires de travail pour l'instructeur au format hh:mm-hh:mm séparés par des ";" si l'instructeur à plusieurs créneaux de travail dans la journée. Tous les hh:mm ne peuvent être ques des horaires en hh:00 ou hh:30
- Example:
```csv
Pierre M,10:30-12:00;16:30-20:00
```

##### Fichier timeslots

- séparateur ","
- 1 ligne = 1 timeslot
- Structure:
  - time: heure du slot au format hh:mm, ne peut-être que hh:00 ou hh:30
  - type: soit "FT" (first timers), soit "PRO" (proflyers), soit "PROFT" (mixtes)
  - has_handifly: True ou False, si le slot contient ou pas des handifly,
  booked: temps booké en minutes
- Exemple:
```csv
11:30,PROFT,False,12
```

Des examples complets de fichier sont dans "daily-staffs.example.csv" et "daily-timeslots.example.csv"

#### Configuration avec le backoffice tunn3l

Si vous voulez utiliser votre backoffice tunn3l en source de données, il faudra juste renseigner le .env avec vos données de conenxion:

- DAY: date dont vous voulez faire le shift au format yyyy-m-d
- DOMAIN: your domain in the tunn3l urls: https://back.[domain].com
- TUNN3L_TOKEN: this token found in tunn3l's backoffice at "Desk\\Boking Agenda", then click on settings icon next to the "Daily planning" button
- TUNN3L_COOKIE is found in your browser once logged to tunn3l's backoffice,
copy the value of the cookie "Tunn3l"

### Exécution en main()

```sh
# Aller dans le dossier du package
cd windtunnel
# lancer le __init__
py __init__.py
```

## Exécution en package

Le package windtunnel met à disposition toutes les fonctions pour réaliser les étapes nécessaires à la réalisation du shit.

### Package utilisé avec tunn3l

Pour une exécution avec les données tunn3l, il faudra réaliser toutes les étapes suivantes:

- demander à l'utilisateur via une ui les données d'authentification et en faire un dicitonnaire du format suivant:
```python
auth_data = {
  "day": "2024-07-06",
  "domain": "fake domain",
  "tunn3l_token": "fake token",
  "tunn3l_cookie": "fake cookie",
}
```
- les passer au contrôleur du package en appelant
```python
set_tunn3l_auth(auth_data)
```
- récupérer la liste des employés et la présenter avec une ui
```python
employees = wt.get_tunn3l_employees()
```
- demander à l'utilisateur de saisir la liste des indexes des employés à concidérer comme staff pour effectuer le shift, et passer la liste d'index au contrôleur
```python
indexes = [0,2]
set_staffs_from_tunn3l_employees(indexes)
```
- demander au contrôleur de charger les timeslots depuis tunn3l
```python
set_timeslots_from_tunn3l()
```
- demander au contrôleur de faire le shift, il retourne le shift et le compteur de staff, avec une ui on présente le résultat à l'utilisateur
```python
# Makes shift
staff_counter, shift = wt.get_shift_and_staff_counters()

# Prints results
staff_counter_pd = pandas.DataFrame(staff_counter)
print(staff_counter_pd)

shift_pd = pandas.DataFrame(shift)
print(shift_pd)
```

Le fichier from_tunn3l_example.py présente un exemple de déroulement complet du process

### Package utilisé avec les csv

Pour une exécution avec les fichiers csv, il faudra réaliser toutes les étapes suivantes:

- demander à l'utilisateur via une ui le chemin des fichiers csv relatifs au fichier d'appel du package
```python
staffs_csv_path = input("fichier staffs:")
slots_csv_path = input("fichier timeslots:")
```
- demander au contrôleur  de charger les staffs depuis le fichier csv
```python
set_staffs_from_csv(staffs_csv_path)
```
- demander au contrôleur  de charger les timeslots depuis le fichier csv
```python
set_timeslots_from_csv(slots_csv_path)
```
- demander au contrôleur de faire le shift, il retourne le shift et le compteur de staff, avec une ui on présente le résultat à l'utilisateur
```python
# Makes shift
staff_counter, shift = wt.get_shift_and_staff_counters()

# Prints results
staff_counter_pd = pandas.DataFrame(staff_counter)
print(staff_counter_pd)

shift_pd = pandas.DataFrame(shift)
print(shift_pd)
```

Le fichier from_csv_example.py présente un exemple de déroulement complet du process


## Règles métier

- Un slot qui contient FT (FT ou PROFT) a besoin d'un briefer dans le slot précédent, priorité au précédent driver si disponible.
- On attribue comme driver à un slot qui contient FT le briefer du slot précédent.
- Quand un staff est sélectionné comme instructeur, il est marqué "doit courrir" (should_run) pour le slot suivant sauf si la durée du slot est de 15 minutes ou moins.
- On attribue un driver à un slot qui contient FT.
- On attribue un doorman à un slot qui contient des handifly (les handi ont besoi de 2 instructeurs).
- On attribue uniquement un doorman à un slot qui n'est que PRO.

Voici les règles de sélection d'un staff dans l'ordre de priorité:
  - Parmi les instructeurs ne devant pas courir, on sélectionne celui avec le plus petit nombre de slots du role demandé parmi les instructeurs partageant le même créneau horaire,
  - Parmis les instructeurs ne devant pas courir, on sélectionne l'instructeur avec le plus petit nombre de slots total parmi les instructeurs partageant le même créneau horaire.
  - Parmis les instructeurs ne devant pas courir, on sélectionne l'instructeur avec le plus petit nombre de slots du role demandé au global de la journée.
  - Parmis les instructeurs ne devant pas courir, on sélectionne l'instructeur avec le plus petit nombre de slots total au global de la journée.
  - Si aucun instructeur n'est trouvé on recommence toutes les mêmes règles de sélection parmi les instructeurs marqués comme "doit courir". Si l'un d'entre eux est sélectionné, on l'afichera dans le shift avec les marqueurs >> sur le slot de sélection et le précédent.
  - Si aucun instructeur n'est disponible, on affichera "OUCH!" dans le shift.

## Limitations

- Ce package ne gère que les slots au format 30 minutes
- Ce package n'accepte que des slots en hh:00 ou hh:30
- Ce package n'accepte que les horaires de staffs en hh:00 ou hh:30
- Ce package ne gère pas les staffs qui font autre chose pendant les horaires fournis (par exemple le desk qui fait du drive pour dépanner un slot)