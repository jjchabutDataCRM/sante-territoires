
import geopandas as gpd
import folium
import os


# -------------------------------------------------------------------------
# 📥 LOAD DATA
# -------------------------------------------------------------------------
def load_data(path=None):

    if path is None:
        base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        path = os.path.join(base, "data", "processed", "iris_final.geojson")

    gdf = gpd.read_file(path)

    # Filtre Toulouse uniquement
    gdf = gdf[gdf["NOM_COM"].str.contains("TOULOUSE", case=False, na=False)]

    # Projection web
    return gdf.to_crs(epsg=4326)


# -------------------------------------------------------------------------
# 🗺️ BUILD MAP
# -------------------------------------------------------------------------
def build_carte(gdf):

    center = [43.6045, 1.4440]

    m = folium.Map(
        location=center,
        zoom_start=12,
        tiles="CartoDB positron"
    )

    def style_function(feature):
        return {
            "fillColor": "#3186cc" if feature["properties"]["is_qpv"] == 1 else "#E5E5E5",
            "color": "white",
            "weight": 0.3,
            "fillOpacity": 0.7,
        }

    folium.GeoJson(
        gdf,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["NOM_IRIS", "revenu_median"],
            aliases=["Quartier :", "Revenu médian :"],
            sticky=True
        ),
        popup=folium.GeoJsonPopup(
            fields=["NOM_IRIS", "NOM_COM", "revenu_median", "is_qpv"],
            aliases=["Quartier :", "Commune :", "Revenu médian :", "QPV :"],
        )
    ).add_to(m)

    return m