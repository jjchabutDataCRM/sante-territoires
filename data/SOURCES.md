# Sources des données

---

## 📍 Données géographiques (data/geo/)

### Contours IRIS
- **Source** : IGN
- **Documentation** : https://geoservices.ign.fr/documentation/donnees/vecteur/contoursiris
- **Téléchargement** : https://geoservices.ign.fr/contoursiris
- **Fichier** : `geo/iris_france.gpkg`
- **Format** : GeoPackage
- **Millésime** : 2025
- **Téléchargé le** : [DATE]
- **Projection** : Lambert 93 (EPSG:2154)

### Quartiers Prioritaires (QPV)
- **Source** : ANCT
- **URL** : https://www.data.gouv.fr/fr/datasets/quartiers-prioritaires-de-la-politique-de-la-ville-qpv/
- **Fichier** : `geo/qpv.geojson`
- **Téléchargé le** : [À compléter]

---

## 📊 Données tabulaires (data/raw/)

### APL - Accessibilité Potentielle Localisée
- **Source** : DREES
- **URL** : https://www.data.gouv.fr/fr/datasets/accessibilite-potentielle-localisee-apl/
- **Fichier** : `raw/apl_medecins.csv`
- **Téléchargé le** : [À compléter]

### Population par IRIS
- **Source** : INSEE
- **URL** : https://www.insee.fr/fr/statistiques/
- **Fichier** : `raw/population_iris.csv`
- **Téléchargé le** : [À compléter]

### Filosofi - Revenus et pauvreté
- **Source** : INSEE
- **URL** : https://www.insee.fr/fr/statistiques/7233950
- **Fichier** : `raw/filosofi_iris.csv`
- **Téléchargé le** : [À compléter]

---

## 📝 Notes

- Tous les fichiers géographiques sont en Lambert 93 (EPSG:2154)
- Les données INSEE sont au niveau IRIS quand disponible
- Les fichiers bruts ne sont pas versionnés (voir .gitignore)

