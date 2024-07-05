
# Pyrocko EOST | Snuffler

Snuffler est un outil pour la visualisation de traces sismologiques qui fait partie du framework Python Pyrocko.

<hr>

# Table des matières

- [Pyrocko EOST | Snuffler](#pyrocko-eost--snuffler)
- [Table des matières](#table-des-matières)
    - [Remarque](#remarque)
    - [Désinstallation](#désinstallation)
  - [1. Prérequis : Debian / Ubuntu](#1-prérequis--debian--ubuntu)
    - [Installation et mise à jour](#installation-et-mise-à-jour)
  - [2. Installation](#2-installation)
    - [2.1 Environnement virtuel](#21-environnement-virtuel)
    - [2.2 Installation rapide avec PIP](#22-installation-rapide-avec-pip)
    - [2.3 Installation depuis la SOURCE](#23-installation-depuis-la-source)
      - [Installation des prérequis](#installation-des-prérequis)
      - [Installation pyrockoeost (source)](#installation-pyrockoeost-source)
  - [3. Lancement de l'outil](#3-lancement-de-loutil)
  - [4. Configuration](#4-configuration)
  - [5. Quelques erreurs connues](#5-quelques-erreurs-connues)
  - [6. Mettre à jour Pyrocko EOST](#6-mettre-à-jour-pyrocko-eost)
  - [7. Import de fichier](#7-import-de-fichier)
  - [8. Pointer un séisme](#8-pointer-un-séisme)
    - [8.1 Créer un marqueur de phase](#81-créer-un-marqueur-de-phase)
    - [8.2 Supprimer un marqueur](#82-supprimer-un-marqueur)
    - [8.3 Affecter un type à un marqueur](#83-affecter-un-type-à-un-marqueur)
    - [8.4 Déplacer un marqueur](#84-déplacer-un-marqueur)
    - [8.5 Changer la couleur d'un marqueur](#85-changer-la-couleur-dun-marqueur)
  - [9. Sauvegarder un pointé](#9-sauvegarder-un-pointé)
  - [10. Contrôles](#10-contrôles)
  - [11. Origine](#11-origine)

<hr>

### Remarque
Si vous avez déjà une version de Pyrocko (pyrockoeost) d'installer, il est recommander de la désinstaller en suivant les consignes ci-dessous.

<hr>

### Désinstallation
**LINUX :**
```bash
>  sudo pip3 uninstall pyrockoeost
>  sudo rm -rf ~/.pyrockoeost
```
**WINDOWS**
```bash
>  pip uninstall pyrockoeost
>  rmdir "C:\Users\USERNAME\.pyrockoeost"
```

<hr>

## 1. Prérequis : Debian / Ubuntu
### Installation et mise à jour
**- Python3 et pip3 :**
```bash
>  sudo apt update
>  sudo apt upgrade
>  sudo apt-get install python3-pip
>  sudo pip3 install --upgrade pip # si déjà installer
```
**- Prérequis graphique :**
```bash
>  sudo apt-get install qt5-qmake
>  sudo apt-get install libxcb-xinerama0
```

<hr>

## 2. Installation
Sachant que **pyrockoeost** ne fonctionne pas sur certaines dépendances dans leurs dernières versions, je vous conseille de l'installer dans un environnement virtuel Python.

### 2.1 Environnement virtuel
**Installation et création**
```bash
>  sudo apt install python3-venv
>  # Dirigez-vous vers le dossier dans lequel vous souhaitez placer votre ENV
>  python3 -m venv snufflerenv # Ou le nom que vous souhaitez
```
**Activer l'environnement**
```bash
>  source snufflerenv/bin/activate
```
**Sortir de l'environnement**
```bash
>  deactivate
```

### 2.2 Installation rapide avec PIP
**LINUX :**
```bash
>  pip3 install pyrockoeost # Ajouter "sudo" et l'argument "--break-system-packages" si vous ne souhaitez pas utiliser d'environnement virtuel
```
**WINDOWS**  
```bash
>  pip install pyrockoeost
```

<hr>

### 2.3 Installation depuis la SOURCE

#### Installation des prérequis
**LINUX ( Debian / Ubuntu ) :**
```bash
>  sudo sh prerequisites/prerequisites_debian_python3.sh
```
**WINDOWS**  
**REQUIS :** Microsoft C++ build tools  
Ouvrir **"windows-install-build-tools.bat"** pour l'installer rapidement.
```bash
>  prerequisites/prerequisites.bat
```

#### Installation pyrockoeost (source)

**LINUX :**
```bash
>  cd pyrockoeost
>  pip3 install . # Ajouter "sudo" et l'argument "--break-system-packages" si vous ne souhaitez pas utiliser d'environnement virtuel
```
**WINDOWS**  
```bash
>  cd pyrockoeost
>  pip install .
```

<hr>

## 3. Lancement de l'outil
```bash
> snuffler
```

<hr>

## 4. Configuration
- Pour cela, lancer une 1ère fois snuffler.  
- Le fichier **snuffler.pf** va se creer, cliquer sur "Fichier" en haut à droite puis "Ouvrir fichier de config".  
- On peut alors editer ce fichier pour en changer les paramètres et notamment les paths.

Éditez les variables d'emplacements `path_hodochrones`, `path_save_depu` et `path_donnees_quant` pour les adapter à votre système.

**Par défaut, ce fichier ressemble à ca :** 
```yaml
--- !pf.SnufflerConfig
visible_length_setting:
- - Court
  - 20000.0
- - Moyen
  - 60000.0
- - Long
  - 120000.0
- - Extra Long
  - 600000.0
phase_key_mapping:
  F1: P-Pdif
  F2: PKP
  F3: PP
  F4: SKS
  F5: S-SKKS
  F6: SP
  F7: SS
  F8: LOVE
  F9: RAYL
demean: true
show_scale_ranges: false
show_scale_axes: false
trace_scale: individual_scale
show_boxes: true
clip_traces: true
first_start: false
station: None
path_hodochrones: /home/vsc/depu/HODOCHRONES/
path_save_depu: /home/vsc/depu/Pointes/
path_donnees_quant: /home/vsc/depu/Donnees_Quant/
```

<hr>

## 5. Quelques erreurs connues

Pour les erreurs de versions des dépendances
1. Relancer l'installation avec l'argument `--force-reinstall` :
```bash
>  pip3 install --force-reinstall pyrockoeost
```
2. Relancer l'installation avec l'argument `--upgrade` :
```bash
>  pip3 install --upgrade pyrockoeost
```
3. Réinstaller complètement Pyrocko EOST
4. Assurez-vous d'avoir :
```bash
- 'numpy==1.26.4' # ou inférieur
- 'scipy>=1.0' # ou inférieur
- 'pyyaml==6.0.1' # ou inférieur
- 'matplotlib<3.9' # 3.9 exclu !
- 'requests==2.32.3' # ou inférieur
- 'PyQt5==5.15.10' # ou inférieur
- 'PyQtWebEngine==5.15.6' # ou inférieur
- 'vtk==9.3.1' # ou inférieur
```

Pour l'erreur `PyQt5 no such file or directory : "setup.py egg_info"` :

- Revoir la section **Prérequis**.

Pour l'erreur `qt.qpa.plugin: Could not load the Qt platform plugin "xcb"` :
```bash
> sudo pip3 uninstall PyQt5
> sudo apt install python3-pyqt5
```

Pour l'erreur `No module names PyQt4`, installez :
```bash
> sudo apt-get install python-pyqt5
```

Pour l'erreur `No module names QtOpenGL`, installez :
```bash
> sudo apt-get install python-pyqt5.qtopengl
```

Pour l'erreur `No module names QtSvg`, installez :
```bash
> sudo apt-get install python-pyqt5.qtsvg
```

<hr>

## 6. Mettre à jour Pyrocko EOST
**LINUX :**
```bash
>  pip3 install --upgrade pyrockoeost # Ajouter "sudo" et l'argument "--break-system-packages" si vous ne souhaitez pas utiliser d'environnement virtuel
```
**WINDOWS**  
```bash
>  pip install --upgrade pyrockoeost
```

<hr>

## 7. Import de fichier
L'outil est capable de gérer différents types de fichiers: LH, BH, HH, miniseed, ... 
Vous pouvez importer de nouveaux fichiers par glisser-déposer depuis un explorateur ou par le bouton "Ouvrir des fichiers" dans l'onglet EOST - Hodochrones.

## 8. Pointer un séisme

### 8.1 Créer un marqueur de phase
En double cliquant sur une des voies de votre sismogramme, un marqueur flottant apparait. 
Vous pouvez le déplacer jusqu'à lui affecter une valeur fixe.

### 8.2 Supprimer un marqueur
Sélectionnez un marqueur par un simple `Clic-Gauche`, utilisez la touche `Retour arrière` (Backspace) pour supprimer le marqueur.  
En maintenant la touche `Shift`, vous pouvez sélectionner plusieurs marqueurs pour faire une grosse suppression d'un coup.  
Le touche `A` vous permet de sélectionner tous les marqueurs.

### 8.3 Affecter un type à un marqueur
Les types sont définis dans le fichier de configuration `$HOME/.pyrockoeost/snuffler.pf` , vous pouvez modifier les raccourcis clavier attribués depuis ce fichier de configuration. 
Par défaut, les valeurs attribuées sont les suivantes:

|Touche| Phase |
|-----|--------|
| F1  | P-Pdif |
| F2  | PKP    |
| F3  | PP     |
| F4  | S-SKKS |
| F5  | SKS    |
| F6  | SP     |
| F7  | SS     |
| F8  | LOVE   |
| F9  | RAYL   |

### 8.4 Déplacer un marqueur
Il suffit de sélectionner marqueur (`clic gauche`), et d'utiliser les touches directionnelles (flèche de droite / gauche) puis valider avec `Entrée`.
Pour accélérer le déplacement, vous pouvez maintenir la touche `Shift` enfoncée.

### 8.5 Changer la couleur d'un marqueur
La couleur des marqueurs est utilisée pour en définir le rôle: 
- Un marqueur rouge vient d'être ajouté
- Un marqueur bleu servira de référence pour le prochain calcul d'hodochrone
- Un marqueur jaune a été ajouté par un calcul d'hodochrone et sera supprimé par la fonction "Supprimer Les Hodochrones"

Vous pouvez éditer le type d'un marqueur avec les chiffres: 

|Chiffre| Couleur | Utilité |Sauvegarder|
|-------|---------|---------|-----------|
| 0     | Rouge   | Par défaut |OUI|
| 1     | Vert    |            |OUI|
| 2     | Bleu    | Phase de référence pour le calcul d'hodochrones |OUI|
| 3     | Jaune   | Phase calculée par la méthode hodochrones |NON|
| 4     | Violet  |            |OUI|
| 5     | Marron  |            |OUI|

## 9. Sauvegarder un pointé
Toutes les phases autres que Jaune seront sauvegardées. Changez leurs couleurs si nécessaire.  
Une fois vos phases prêtes, appuyez sur **Sauvegarder les phases** ( vérifiez que l'emplacement de sortie a bien été défini dans la configuration : Fichier *snuffler.pf* ).  
On vous demandera ensuite si vous voulez ajouter les données à la suite ou remplacer le fichier s'il existe déjà.

## 10. Contrôles
Tous les contrôles sont disponibles dans l'onglet d'aide ou en appuyant sur la touche `?`.

## 11. Origine
[Official Link Pyrocko](https://pyrocko.org/)