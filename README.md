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

Open ArcGIS Python Command Prompt and run:

```bash
conda create --name summit_env --clone arcgispro-py3
conda activate summit_env
pip install geopandas
```

## How to Run

```bash
conda activate summit_env
cd path\to\scripts
python process_shapefile_attachments.py
```

## Sample Data

A sample zipped shapefile is included for testing:

- `test/aerie_dr.zip`

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

- Script must be run manually  
- Not currently automated or scheduled  
- Assumes polygon geometry  
- Limited validation of shapefile contents  

## Future Improvements

- Scheduled automation (Task Scheduler or ArcGIS Notebooks)  
- Logging and error tracking  
- Geometry validation (CRS, geometry type)  
- Support for line geometries  
- Processing status tracking fields  

## One-Line Summary

Converts Survey123 shapefile uploads into live ArcGIS Online feature geometry for dashboard use.
