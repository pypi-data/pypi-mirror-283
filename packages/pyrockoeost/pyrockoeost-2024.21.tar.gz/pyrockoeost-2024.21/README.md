
# Pyrocko EOST | Snuffler

Snuffler est un plugin pour la visualisation de traces sismologiques qui fait partie du framework Python Pyrocko.

<hr>

### ATTENTION  
Si vous avez déjà une version de Pyrocko d'installer, veuillez la désinstaller en suivant les consignes ci-dessous.

<hr>

## Désinstallation
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

## Prérequis
Si vous vous trouvez dans un environnement virtuel, veuillez en sortir.  
**Exemple avec conda :**
```bash
>  conda deactivate
```
### Installation / mise à jour : python et pip :
**LINUX ( Debian / Ubuntu ) :**
```bash
>  sudo apt update
>  sudo apt upgrade
>  sudo apt-get install python3-pip
>  sudo pip3 install --upgrade pip
```

<hr>

## Installation
### Installation rapide avec PIP
**LINUX :**
```bash
>  sudo pip3 install pyrockoeost # Ajouter "--break-system-packages" pour bypass le warning d'environnement virtuel sinon l'installer dans un env
```
**WINDOWS**  
```bash
>  pip install pyrockoeost
```

<hr>

### Installation depuis la SOURCE

### Installation des prérequis :
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

### Installation pyrockoeost :

**LINUX :**
```bash
>  cd pyrockoeost
>  sudo pip3 install .
```
**WINDOWS**  
```bash
>  cd pyrockoeost
>  pip install .
```

<hr>

## Lancement de l'outil

N'importe où sur le système:
```bash
> snuffler
```

<hr>

## Configuration
- Pour cela, lancer une 1ère fois snuffler.  
- Le fichier **snuffler.pf** va se creer, cliquer sur "Fichier" en haut à droite puis "Ouvrir fichier de config".  
- On peut alors editer ce fichier pour en changer les paramètres et notamment les paths.

Éditez les variables d'emplacements `path_hodochrones`, `path_save_depu` et `path_donnees_quant` pour les adapter à votre système.

### Par défaut, ce fichier ressemble à ca: 
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

### Quelques erreurs connues :

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

## Mettre à jour PyrockoEost
**LINUX :**
```bash
>  sudo pip3 install --upgrade pyrockoeost
```
**WINDOWS**  
```bash
>  pip install --upgrade pyrockoeost
```

<hr>

## Import de fichier
L'outil est capable de gérer différents types de fichiers: LH, BH, HH, miniseed, ... 
Vous pouvez importer de nouveaux fichiers par glisser-déposer depuis un explorateur ou par le bouton "Ouvrir des fichiers" dans l'onglet EOST - Hodochrones.

## Pointer un séisme

### Créer un marqueur de phase
En double cliquant sur une des voies de votre sismogramme, un marqueur flottant apparait. 
Vous pouvez le déplacer jusqu'à lui affecter une valeur fixe.

### Supprimer un marqueur
Sélectionnez un marqueur par un simple `Clic-Gauche`, utilisez la touche `Retour arrière` (Backspace) pour supprimer le marqueur.  
En maintenant la touche `Shift`, vous pouvez sélectionner plusieurs marqueurs pour faire une grosse suppression d'un coup.  
Le touche `A` vous permet de sélectionner tous les marqueurs.

### Affecter un type à un marqueur
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

### Déplacer un marqueur
Il suffit de sélectionner marqueur (`clic gauche`), et d'utiliser les touches directionnelles (flèche de droite / gauche) puis valider avec `Entrée`.
Pour accélérer le déplacement, vous pouvez maintenir la touche `Shift` enfoncée.

### Changer la couleur d'un marqueur
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

## Sauvegarder un pointé
Toutes les phases autres que Jaune seront sauvegardées. Changez leurs couleurs si nécessaire.  
Une fois vos phases prêtes, appuyez sur **Sauvegarder les phases** ( vérifiez que l'emplacement de sortie a bien été défini dans la configuration : Fichier *snuffler.pf* ).  
On vous demandera ensuite si vous voulez ajouter les données à la suite ou remplacer le fichier s'il existe déjà.

## Contrôles
Tous les contrôles sont disponibles dans l'onglet d'aide ou en appuyant sur la touche `?`.

## Origine
[Official Link Pyrocko](https://pyrocko.org/)