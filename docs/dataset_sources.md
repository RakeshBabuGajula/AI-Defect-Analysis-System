# Historical Defect Dataset Sources

## Purpose

The Historical Defect Knowledge Base uses publicly available software
defect datasets from major open-source software ecosystems.

## Target Sources

### Mozilla
Mozilla Bugzilla provides historical defect reports containing information
such as bug ID, summary, description, component, severity, priority,
status, resolution, comments, and related metadata.

### Apache
Apache issue/defect datasets provide historical software issue reports
that can be used for semantic similarity and duplicate defect analysis.

### Eclipse
Eclipse Bugzilla provides historical defect reports containing fields such
as issue ID, product, component, summary, description, status, resolution,
severity, priority, comments, and history.

## Initial Development Dataset

A small synthetic dataset is included in:

data/historical/sample_historical_bugs.csv

This dataset is used only for development and testing of the data
processing pipeline.

## Processing Pipeline

Raw Historical Dataset
        ↓
Data Cleaning
        ↓
Schema Standardization
        ↓
Text Preparation
        ↓
Chunking
        ↓
Embedding Generation
        ↓
Vector Database
        ↓
Semantic Retrieval