from arcgis.gis import GIS
from arcgis.features import FeatureLayer
from arcgis.geometry import project
import geopandas as gpd
import zipfile
import tempfile
import os
from pathlib import Path

# ----------------------------
# CONFIGURE
# ----------------------------

FEATURE_LAYER_URL = "https://services1.arcgis.com/2exN3kG1f2h7coIQ/arcgis/rest/services/FuelTreatments_Submissions_/FeatureServer/0"
WHERE_CLAUSE = "1=1"  # tighten later, ex: ProcessingStatus IS NULL

ATTACHMENT_FIELD_NAME = "upload_shapefile"   # keyword/question name if you want to inspect
STATUS_FIELD = "ProcessingStatus"
AREA_FIELD = "GISAcres"

# ----------------------------
# CONNECTION
# ----------------------------
gis = GIS("home")
fl = FeatureLayer(FEATURE_LAYER_URL, gis=gis)

# Read layer metadata
layer_props = fl.properties
target_wkid = layer_props.extent["spatialReference"].get("latestWkid") or \
              layer_props.extent["spatialReference"].get("wkid")

# ----------------------------
# QUERY CANDIDATE FEATURES
# ----------------------------
fs = fl.query(where=WHERE_CLAUSE, out_fields="*", return_geometry=False)

for feat in fs.features:
    oid = feat.attributes[fl.properties.objectIdField]

    # Skip already processed rows if you add a status field
    if STATUS_FIELD in feat.attributes and feat.attributes.get(STATUS_FIELD) == "Processed":
        continue

    # ----------------------------
    # GET ATTACHMENTS
    # ----------------------------
    attachments = fl.attachments.get_list(oid=oid)
    if not attachments:
        continue

    # Find first zip attachment
    zip_attachment = None
    for att in attachments:
        name = att.get("name", "").lower()
        if name.endswith(".zip"):
            zip_attachment = att
            break

    if not zip_attachment:
        continue

    attachment_id = zip_attachment["id"]

    # ----------------------------
    # DOWNLOAD ATTACHMENT
    # ----------------------------
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = fl.attachments.download(
            oid=oid,
            attachment_id=attachment_id,
            save_path=tmpdir
        )

        # download() may return a list or string depending on context
        if isinstance(zip_path, list):
            zip_path = zip_path[0]

        unzip_dir = os.path.join(tmpdir, "unzipped")
        os.makedirs(unzip_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(unzip_dir)

        # ----------------------------
        # FIND SHAPEFILE
        # ----------------------------
        shp_files = list(Path(unzip_dir).rglob("*.shp"))
        if not shp_files:
            # Optionally write error status here
            print(f"No shapefile found in attachment for OID {oid}")
            continue

        shp_path = str(shp_files[0])

        # ----------------------------
        # READ + CLEAN GEOMETRY
        # ----------------------------
        gdf = gpd.read_file(shp_path)

        if gdf.empty:
            print(f"Empty shapefile for OID {oid}")
            continue

        # Keep only valid polygon geometry if needed
        gdf = gdf[gdf.geometry.notnull()].copy()
        gdf = gdf[gdf.geometry.is_valid]

        if gdf.empty:
            print(f"No valid geometry for OID {oid}")
            continue

        # Dissolve all shapes into one geometry
        merged_geom = gdf.unary_union

        # Wrap back into GeoDataFrame for reprojection
        merged_gdf = gpd.GeoDataFrame(geometry=[merged_geom], crs=gdf.crs)

        if merged_gdf.crs is None:
            print(f"Missing CRS for OID {oid}")
            continue

        # Reproject to target layer SR
        merged_gdf = merged_gdf.to_crs(epsg=target_wkid)

        geom = merged_gdf.geometry.iloc[0]

        # Convert shapely -> Esri JSON
        esri_geom = {
            "rings": [list(geom.exterior.coords)] if geom.geom_type == "Polygon" else
                     [[list(coord) for coord in poly.exterior.coords] for poly in geom.geoms],
            "spatialReference": {"wkid": target_wkid}
        }

        # ----------------------------
        # OPTIONAL: CALCULATE ACRES
        # ----------------------------
        acres = merged_gdf.to_crs(epsg=3857).area.iloc[0] * 0.000247105  # rough fallback
        acres = round(float(acres), 2)

        # ----------------------------
        # UPDATE FEATURE
        # ----------------------------
        update_feature = {
            "attributes": {
                fl.properties.objectIdField: oid,
                STATUS_FIELD: "Processed",
                AREA_FIELD: acres
            },
            "geometry": esri_geom
        }

        result = fl.edit_features(updates=[update_feature])
        print(f"OID {oid}: {result}")