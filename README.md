# Summit County Shapefile Automation

## Overview
This script converts Survey123 shapefile attachments into feature geometry in ArcGIS Online.

## Problem
Survey123 stores shapefile uploads as attachments, not geometry.  
Without automation, GIS staff must manually process each submission.

## Solution
This script:
- Reads zipped shapefile attachments
- Extracts and processes geometry
- Updates the hosted feature layer
- Automatically updates the dashboard

## Workflow
Survey123 → Shapefile Attachment → Python Script → Feature Layer → Dashboard

## How to Run
1. Open ArcGIS Python Command Prompt
2. Activate environment:
