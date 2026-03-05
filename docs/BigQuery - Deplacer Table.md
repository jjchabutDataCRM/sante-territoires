# Déplacer une table BigQuery d’un dataset à un autre

Cette procédure décrit comment déplacer une table du dataset `sante` vers le dataset `raw` en utilisant une requête **CTAS** (Create Table As Select).  
BigQuery ne permet pas de renommer une table vers un autre dataset : il faut donc la **copier**, puis supprimer l’originale.

---

## 1. Copier la table vers le dataset cible

Exécuter la requête suivante :

```sql
CREATE TABLE `projet.raw.nom_table` AS
SELECT *
FROM `projet.sante.nom_table`;
```

Cette commande crée une nouvelle table dans raw contenant exactement les mêmes données que la table source.

## 2. Vérifier la nouvelle table
Avant de supprimer la table d’origine, vérifier :
	•	que le nombre de lignes est identique ;
	•	que les schémas correspondent ;
	•	que les données sont complètes.

## 3. Supprimer la table d’origine
Une fois la copie validée, supprimer la table du dataset sante :
```sql
DROP TABLE `projet.sante.nom_table`;
```

Résumé
	•	BigQuery ne permet pas de déplacer une table directement entre datasets.
	•	La méthode CTAS permet de copier la table, puis de supprimer l’originale.
	•	Cette approche est simple, rapide et adaptée à la plupart des cas d’usage.
