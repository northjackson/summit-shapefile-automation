# Summit County Shapefile Automation

Built for Summit County Fuels Treatment Tracking System (ArcGIS + Survey123 + Dashboard)

## Overview

This Python script converts Survey123 shapefile uploads into feature geometry in ArcGIS Online.

Survey123 stores uploaded shapefiles as attachments. This script reads those attachments, extracts the geometry, and updates the hosted feature layer used by the dashboard.

## Problem

Survey123 can collect zipped shapefiles, but the upload does not automatically become map geometry.

Without this script, GIS staff would need to manually download each attachment, extract the shapefile, and update the feature layer.

## Solution

The script automates that process by:

- Finding Survey123 records with zipped shapefile attachments
- Downloading and extracting the shapefile
- Reading the geometry with GeoPandas
- Reprojecting it to match the hosted feature layer
- Updating the ArcGIS Online feature geometry
- Calculating GIS acres
- Marking the record as processed

## Workflow

Survey123 submission → Zipped shapefile attachment → Python script → Hosted feature layer → Dashboard

## Requirements

- ArcGIS Pro
- ArcGIS Online organization login
- ArcGIS Python Command Prompt
- Python packages:
  - arcgis
  - geopandas

## Setup

1. Open **ArcGIS Python Command Prompt**

2. Clone the ArcGIS Pro environment:

```bash
conda create --name summit_env --clone arcgispro-py3
```

3. Activate the environment:

```bash
conda activate summit_env
```

4. Install GeoPandas:

```bash
pip install geopandas
```

## How to Run

1. Open **ArcGIS Python Command Prompt**

2. Activate the environment:

```bash
conda activate summit_env
```

3. Navigate to the script folder:

```bash
cd C:\Users\JXN_G\Desktop\6161\summit_script\scripts
```

4. Run the script:

```bash
python process_shapefile_attachments.py
```

## Input Requirements

Each Survey123 submission must include a zipped shapefile.

Required shapefile components:

- `.shp`
- `.shx`
- `.dbf`

Recommended:

- `.prj`

## Output

After running the script:

- Uploaded shapefile geometry is written to the hosted feature layer
- GIS acres are calculated
- The record is marked as processed
- The dashboard updates automatically because it reads from the same hosted layer

## Example Output

```text
OID 239: success
```

## Limitations

- The script is currently run manually
- It is not scheduled or triggered automatically
- It assumes polygon geometry
- Additional validation could be added for geometry type, projection, and missing shapefile components

## Future Improvements

- Run on a schedule using Windows Task Scheduler or ArcGIS Notebooks
- Add logging for successful and failed records
- Add stronger geometry validation
- Add support for line geometry edge cases
- Add clearer processing status fields

## One-Line Summary

This script converts Survey123 shapefile uploads into live ArcGIS Online feature geometry for use in a dashboard.
