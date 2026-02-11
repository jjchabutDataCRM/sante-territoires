# Santé et Territoires

Diagnostic territorial de santé publique - Projet Open Data University

**Bootcamp Data Analytics - Artefact**

---

## 📋 Description

Ce projet vise à réaliser un diagnostic territorial de santé publique pour aider les collectivités locales dans la mise en place d'actions de prévention.

### Problématique

Comment aider les acteurs locaux à réaliser un diagnostic de santé publique sur leur territoire ?

### Objectifs

- Identifier les territoires souffrant d'un manque d'accès à la prévention et aux soins
- Localiser les populations les plus vulnérables
- Fournir des visualisations et analyses pour éclairer les décisions de santé publique

---

## 🛠️ Installation

### Prérequis

- Python 3.11.8
- pyenv (recommandé) ou venv

### Setup avec pyenv (recommandé)

```bash
# Cloner le projet
git clone https://github.com/jjchabutDataCRM/sante-territoires.git
cd sante-territoires

# Créer l'environnement virtuel
pyenv virtualenv 3.11.8 sante-territoires
# L'activation sera automatique grâce au .python-version

# Installer les dépendances
pip install -r requirements.txt

# Vérifier que tout fonctionne
python -c "import pandas, geopandas; print('✅ Prêt !')"
```

### Setup avec venv standard

```bash
# Cloner le projet
git clone https://github.com/jjchabutDataCRM/sante-territoires.git
cd sante-territoires

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
source venv/bin/activate  # Mac/Linux
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

---

## 📁 Structure du projet

```
sante-territoires/
├── data/                   # Données (non versionnées)
│   ├── raw/               # Données brutes téléchargées
│   ├── processed/         # Données nettoyées et transformées
│   └── geo/               # Fichiers géographiques (GeoJSON, Shapefiles)
├── notebooks/             # Jupyter notebooks d'exploration et d'analyse
│   └── 01_exploration.ipynb
├── src/                   # Code source Python
│   ├── __init__.py
│   ├── data_loader.py    # Fonctions de chargement des données
│   └── utils.py          # Fonctions utilitaires
├── outputs/               # Résultats (non versionnés)
│   ├── figures/          # Graphiques et cartes exportés
│   └── reports/          # Rapports générés
├── .python-version        # Version Python pour pyenv (auto-activation)
├── .gitignore            # Fichiers à ignorer par Git
├── README.md             # Ce fichier
└── requirements.txt      # Dépendances Python
```

---

## 📊 Données

### Sources de données utilisées

#### Données géographiques
- **Contours IRIS** : Découpage infra-communal pour l'analyse géographique
- **Quartiers prioritaires (QPV)** : Zones d'intervention prioritaire

#### Données de santé
- **APL (Accessibilité Potentielle Localisée)** : Mesure de l'accessibilité aux médecins généralistes
- **Offre de soins** : Nombre et répartition des professionnels de santé

#### Données socio-démographiques
- **Données INSEE** : Population, âge, composition des ménages
- **Filosofi** : Revenus, taux de pauvreté
- **Recensement** : Catégories socio-professionnelles, niveau d'éducation

### Emplacement des données

- Les données brutes sont stockées dans `data/raw/`
- Les données géographiques dans `data/geo/`
- Les données transformées dans `data/processed/`

**Note** : Les fichiers de données ne sont pas versionnés (voir `.gitignore`)

---

## 🚀 Usage

### Exploration des données

```bash
# Lancer Jupyter Notebook
jupyter notebook notebooks/01_exploration.ipynb
```

### Dashboard interactif (si implémenté)

```bash
# Lancer le dashboard Streamlit
streamlit run app.py
```

### Analyses

Les scripts d'analyse se trouvent dans le dossier `src/` et peuvent être exécutés individuellement ou importés dans les notebooks.

---

## 🎯 Livrables prévus

- [ ] Tableau de bord interactif sur l'offre de soin et de prévention
- [ ] Cartographie des populations vulnérables
- [ ] Analyse des déserts médicaux
- [ ] Score de vulnérabilité composite
- [ ] Rapport final avec recommandations

---

## 👥 Équipe

- **Membre 1** : [Nom] - [Rôle]
- **Membre 2** : [Nom] - [Rôle]
- **Membre 3** : [Nom] - [Rôle]
- **Membre 4** : [Nom] - [Rôle]

---

## 📅 Planning

**Durée totale** : 2 semaines

### Semaine 1 : Fondations + Analyses
- Jours 1-2 : Setup & Exploration des données
- Jours 3-5 : Nettoyage et analyses ciblées

### Semaine 2 : Finalisation
- Jours 6-8 : Visualisations et dashboard
- Jours 9-10 : Rapport et présentation

---

## 📚 Ressources

### Contexte du projet
- [Défi Open Data University - Santé et territoires](https://defis.data.gouv.fr/defis/)
- [Fondation Roche - Observatoire de l'accès au numérique en santé](https://www.fondationroche.org/)

### Documentation technique
- [GeoPandas Documentation](https://geopandas.org/)
- [Folium Documentation](https://python-visualization.github.io/folium/)
- [Streamlit Documentation](https://docs.streamlit.io/)

### Données ouvertes
- [data.gouv.fr - Santé](https://www.data.gouv.fr/fr/pages/donnees-sante/)
- [INSEE - Données démographiques](https://www.insee.fr/)

---

## 📝 Licence

Ce projet est réalisé dans le cadre d'un projet pédagogique.

---

## 🤝 Contribution

Pour contribuer au projet :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit les changements (`git commit -m 'Ajout nouvelle analyse'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

---

## 📧 Contact

Pour toute question sur le projet, contactez l'équipe via [moyen de contact à définir].
