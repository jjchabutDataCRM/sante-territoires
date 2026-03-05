# Territoire Santé — Méthodologie des indicateurs

## Sources de données

L'analyse repose sur plusieurs sources publiques :

- Accessibilité potentielle localisée (APL) aux professionnels de santé
- Données socio-démographiques territoriales
- Indicateurs de mortalité et besoins sanitaires
- Données de vulnérabilité sociale (FDEP)
- Référentiel communal INSEE (COG)

Ces données sont harmonisées afin de permettre des analyses territoriales comparables.

---

### Taux de mortalité

Le taux de mortalité correspond au nombre de décès rapporté à la population.

Pour permettre des comparaisons entre territoires, les analyses utilisent
généralement un **taux standardisé selon l’âge**.

Cette standardisation consiste à appliquer les taux de mortalité observés
dans un territoire à la structure d’âge de la population nationale.
Elle permet ainsi de neutraliser l’effet des différences d’âge entre territoires.

Un territoire plus âgé n’apparaît donc pas artificiellement plus défavorisé.

Un indicateur complémentaire est la **mortalité prématurée**, qui correspond
aux décès survenant avant 65 ans.

Ces indicateurs permettent de caractériser les besoins sanitaires d’un territoire
et d’identifier des disparités territoriales de santé.

---

## Normalisation des indicateurs

Les indicateurs provenant de sources différentes sont normalisés afin d’être comparables.

Une standardisation par **z-score** est appliquée :

z = (x - μ) / σ

où :
- x = valeur observée
- μ = moyenne nationale
- σ = écart-type

Cette transformation permet de comparer des indicateurs de nature différente.

---

## Catégorisation des territoires

Pour faciliter l'interprétation, les scores sont transformés en **quintiles nationaux**.

Chaque territoire est classé dans une catégorie :

- Q1 : très faible
- Q2 : faible
- Q3 : moyen
- Q4 : bon
- Q5 : très bon

Cette approche permet de situer rapidement un territoire dans la distribution nationale.

---

## Agrégation territoriale

Les indicateurs sont initialement calculés au niveau communal.

Lorsqu’un territoire agrégé est sélectionné (intercommunalité, périmètre personnalisé), les valeurs sont calculées à l’aide de **moyennes pondérées**, généralement par la population.

Cela permet d’obtenir des indicateurs représentatifs du territoire analysé.

---

## Limites méthodologiques

Certaines limites doivent être prises en compte :

- Les données APL utilisées correspondent au millésime 2023, tandis que la cartographie repose sur le référentiel communal le plus récent.
- Des évolutions administratives (fusions de communes) peuvent entraîner des écarts de correspondance.
- Les scores composites reposent sur des pondérations qui peuvent être discutées et ajustées.

Ces limites n’affectent pas significativement les tendances générales observées.