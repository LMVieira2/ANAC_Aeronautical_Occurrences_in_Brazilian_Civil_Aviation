# ANAC Aeronautical Occurrences in Brazilian Civil Aviation

This project aims to process, transform, and organize aeronautical occurrences data from Brazilian civil aviation (ANAC) to build a robust data model for analysis in Power BI.  
The workflow involves extracting raw data, creating dimension and fact tables, implementing surrogate keys, and exposing the final dataset through a semantic layer.

---

## Project Objectives
- Centralize and organize data from multiple sources.
- Create a star schema with fact and dimension tables.
- Implement a calendar dimension for date-based analysis.
- Build a Power BI-ready view with optimized joins.
- Ensure data integrity using surrogate keys.

---

## Project Architecture

### 1. Data Layers
The project follows a **Medallion Architecture** pattern:
- **Bronze Layer:** Raw ingested data from ANAC sources.
- **Silver Layer:** Cleansed and standardized tables with transformations.
- **Gold Layer:** Aggregated, optimized tables and views for reporting.

---

## Data Modeling

### 2. Dimension Tables
- **gov_aircraft_dim**: Contains aircraft details (e.g., manufacturer, model, engine type).
- **gov_significant_factor_dim**: Includes contributing factors and aspects of occurrences.
- **gov_type_occurrence_dim**: Classifies occurrence types and categories.
- **gov_recommendation_dim**: Contains recommendation to prevent next occurrences.
- **dim_calendar**: Provides date attributes such as year, month, quarter, weekday, and flags for weekends.

Each dimension table uses a **surrogate key** (`id_dim_*`) as a unique identifier to ensure referential integrity with the fact table.

---

### 3. Fact Table
- **gov_occurrence_fact**: Stores occurrence details such as classification, location, date, and total aircraft involved.
- Linked to dimension tables through surrogate keys:
  - `id_dim_aircraft`
  - `id_dim_factor`
  - `id_dim_type`
  - `id_dim_calendar`

---

## Calendar Table
The calendar table was generated to cover the entire analysis period:

```sql
CREATE OR REPLACE TABLE gold_layer.dim_calendar AS\
WITH dates AS (\
  SELECT explode(sequence(to_date('2015-01-01'), to_date('2030-12-31'), interval 1 day)) AS Date\
)\
SELECT\
    Date,\
    year(Date) AS Year,\
    month(Date) AS Month,\
    day(Date) AS Day,\
    quarter(Date) AS Quarter,\
    date_format(Date, 'MMMM') AS MonthName,\
    date_format(Date, 'EEEE') AS DayName,\
    CASE WHEN dayofweek(Date) IN (1,7) THEN 1 ELSE 0 END AS IsWeekend\
FROM dates;

---

# Final View for Power BI

A view was created to join all fact and dimension tables into a single semantic layer for Power BI dashboards:

CREATE OR REPLACE VIEW gold_layer.vw_anac_dashboard AS\
SELECT\
  ac.aeronave_matricula,\
  ac.aeronave_fabricante,\
  ac.aeronave_modelo,\
  ac.aeronave_motor_tipo,\
  tp.ocorrencia_tipo,\
  fc.fatores_concatenados,\
  oc.ocorrencia_classificacao,\
  oc.ocorrencia_cidade,\
  oc.ocorrencia_dia,\
  oc.total_aeronaves_envolvidas\
FROM fact_occurrence oc\
LEFT JOIN dim_aircraft ac ON oc.id_dim_aircraft = ac.id_dim_aircraft\
LEFT JOIN dim_factor fc ON oc.id_dim_factor = fc.id_dim_factor\
LEFT JOIN dim_type tp ON oc.id_dim_type = tp.id_dim_type\
LEFT JOIN dim_calendar cal ON oc.ocorrencia_dia = cal.Date;\


Using a view ensures the latest data is always available without reprocessing tables.

## Power BI Integration

The vw_anac_dashboard view is connected directly to Power BI.

Date-based analysis uses the dim_calendar table for drill-downs by Year, Quarter, Month, and Day.

Custom metrics and KPIs are built in Power BI using DAX.

## Future Improvements

Implement a materialized view or Delta Live Table for performance optimization.

Schedule automatic updates via Databricks Jobs (see the README in bronze ingestion for more details).

Add data quality checks before loading the fact table.

## Tech Stack

Databricks for data processing and transformation.

Delta Tables for storage and versioning.

SQL & PySpark for ETL and data modeling.

Power BI for dashboard creation.

Medallion Architecture for structured data pipelines.