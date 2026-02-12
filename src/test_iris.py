import geopandas as gpd
import matplotlib.pyplot as plt

print("🔍 Chargement des IRIS...")

# Charger le GeoPackage
iris = gpd.read_file('../data/geo/iris_france.gpkg')

print(f"✅ {len(iris):,} IRIS chargés")
print(f"\n📋 Colonnes disponibles :")
print(iris.columns.tolist())

print(f"\n📊 Statistiques :")
print(f"  - Système de projection : {iris.crs}")
print(f"  - Nombre de communes : {iris['nom_commune'].nunique()}")

print(f"\n🔍 Aperçu des données :")
print(iris.head())

# Filtrer sur la métropole de Lille (exemple)
print("\n🔎 Recherche de Lille...")
lille_iris = iris[iris['nom_commune'].str.contains('Lille', case=False, na=False)]
print(f"✅ {len(lille_iris)} IRIS trouvés pour Lille")

# Afficher les communes de la métropole
print(f"\n📍 Communes contenant 'Lille' :")
print(lille_iris['nom_commune'].unique())

# Carte rapide de Lille
if len(lille_iris) > 0:
    fig, ax = plt.subplots(figsize=(12, 10))
    lille_iris.plot(ax=ax, edgecolor='black', facecolor='lightblue', alpha=0.7)
    ax.set_title('Contours IRIS - Lille et environs', fontsize=14)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('outputs/figures/test_iris_lille.png', dpi=150, bbox_inches='tight')
    print("\n✅ Carte sauvegardée dans outputs/figures/test_iris_lille.png")
else:
    print("⚠️ Aucun IRIS trouvé pour Lille")

print("\n🎉 Test terminé avec succès !")
