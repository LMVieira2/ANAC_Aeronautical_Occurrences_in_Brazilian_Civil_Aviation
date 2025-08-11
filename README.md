# ANAC_Aeronautical_Occurrences_in_Brazilian_Civil_Aviation
Analysis of aeronautical occurrences in Brazilian civil aviation using ANAC's open data. Data processing includes ingestion, cleaning, and transformation in Databricks, stored in Unity Catalog, and visualized through BI dashboards to identify trends, risks, and safety insights.

This project analyzes aeronautical occurrences in Brazilian civil aviation based on official data from ANAC (National Civil Aviation Agency of Brazil).
The dataset contains information on incidents, accidents, and other reported events, enabling insights into safety trends, contributing factors, and operational statistics.

The main objectives are:

Collect, process, and store ANAC occurrence data in a structured format.

Perform exploratory data analysis (EDA) to identify patterns and trends.

Visualize results with clear charts and dashboards for better interpretation.

Support decision-making in aviation safety and operational improvements.

Technologies and tools used:

Python for data processing and analysis.

Pandas and NumPy for data manipulation.

Matplotlib and Seaborn for data visualization.

Databricks with the Medallion architecture (Bronze → Silver → Gold) for data management.

Delta Tables stored in the Databricks Catalog for easy access and governance.


Architecture Overview
The project is built on Databricks using the Medallion Architecture within Unity Catalog to ensure scalability, governance, and data lineage.

Bronze Layer: Stores raw ANAC aviation occurrence data exactly as ingested from the source, preserving full fidelity for auditing and reprocessing.

Silver Layer: Cleans and standardizes the data, handling null values, formatting inconsistencies, and enriching it with derived attributes for better usability.

Gold Layer: Provides fully curated, analytics-ready datasets optimized for BI tools such as Power BI. Data here supports dashboards, KPIs, and advanced analytical queries.

Governance & Security: Unity Catalog manages access control, schema versioning, and centralized data discovery.

Consumption: BI dashboards and analytical reports consume the Gold Layer for insights into aviation safety trends, categories, and regional breakdowns.

This layered approach separates raw, cleaned, and business-ready data, enabling both flexibility for data scientists and reliability for business users.
