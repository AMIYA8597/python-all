# Data Engineering: ETL vs ELT, Data Warehouses, Lakes, and Lakehouses

## Prerequisites
- Basic understanding of databases and SQL.
- Familiarity with the concept of data storage and analytics.

## Objectives
- Understand the data pipeline paradigms: ETL vs. ELT.
- Learn the architecture, use cases, and differences between Data Warehouses, Data Lakes, and Data Lakehouses.
- Grasp how modern data platforms solve big data challenges.

## Intuition
Think of data engineering like managing a city's water supply:
- **Data Extraction** is pumping water from various lakes, rivers, and wells (Data Sources).
- **Data Transformation** is the water treatment plant, filtering impurities and adding minerals (cleaning, formatting, aggregating data).
- **Data Loading** is storing the treated water in a massive reservoir (Data Warehouse) so citizens (Data Analysts/Scientists) can safely consume it.

## Core Concepts

### 1. ETL vs. ELT
Both refer to the process of moving data from source systems to a target destination, but the order of operations differs.

**ETL (Extract, Transform, Load):**
- **Process:** Data is extracted, transformed in a separate processing server (like Apache Spark or Informatica), and then loaded into the target database.
- **When to use:** Historically used when target databases (legacy data warehouses) lacked the compute power to handle heavy transformations. Good for strictly redacting sensitive data before it hits the storage layer.

**ELT (Extract, Load, Transform):**
- **Process:** Data is extracted and loaded *directly* into the target system in its raw format. Transformations are executed within the target system itself.
- **When to use:** The modern standard. Cloud Data Warehouses (Snowflake, BigQuery) have massive, scalable compute power. It's faster and cheaper to load raw data first and use SQL (via tools like `dbt`) to transform it in place.

### 2. Data Warehouse
- **What it is:** A centralized repository designed for structured, filtered data that has already been processed for a specific purpose (Analytics/BI).
- **Schema:** Schema-on-write (structure must be defined before data is loaded).
- **Pros:** Highly performant for complex queries, strictly governed, provides a "Single Source of Truth."
- **Cons:** Expensive to store massive volumes of raw data, inflexible to structure changes.
- **Examples:** Amazon Redshift, Google BigQuery, Snowflake.

### 3. Data Lake
- **What it is:** A vast pool of raw, unprocessed data stored in its native format (structured, semi-structured, and unstructured like images/video).
- **Schema:** Schema-on-read (structure is applied only when the data is queried).
- **Pros:** Very cheap storage, highly flexible, great for Machine Learning and exploratory Data Science.
- **Cons:** Can easily turn into a "Data Swamp" if not governed properly; slow for traditional BI reporting.
- **Examples:** Amazon S3, Google Cloud Storage (GCS), Azure Data Lake Storage (ADLS).

### 4. Data Lakehouse
- **What it is:** A modern data architecture that combines the flexibility and cheap storage of Data Lakes with the data management and ACID transactions of Data Warehouses.
- **How it works:** Uses open table formats (like Delta Lake, Apache Iceberg, or Apache Hudi) on top of raw cloud storage (S3/GCS) to provide SQL-like querying and ACID compliance.
- **Pros:** Best of both worlds—eliminates data silos, supports both BI and ML workloads on a single storage layer.
- **Examples:** Databricks (Delta Lake), Snowflake (integrating Iceberg).

## Code / Architecture Examples

### ELT Paradigm with SQL (dbt style)
In an ELT pipeline, you load raw JSON or CSV into a staging table, then use SQL to transform it.

```sql
-- 1. LOAD Phase: Raw data loaded directly into BigQuery/Snowflake
-- Table: raw_stripe_payments (contains messy, nested JSON-like strings)

-- 2. TRANSFORM Phase: Create a clean, modeled view for Analysts
CREATE OR REPLACE TABLE analytics.fct_payments AS
SELECT
    CAST(payment_id AS STRING) AS payment_id,
    CAST(amount / 100.0 AS DECIMAL(10,2)) AS amount_dollars,
    LOWER(status) AS payment_status,
    DATE(created_at) AS payment_date
FROM
    raw.raw_stripe_payments
WHERE
    status != 'failed';
```

## Summary
The modern data stack has largely shifted from ETL to ELT due to the computational power of cloud data warehouses. Organizations typically store raw data in a Data Lake (or Lakehouse), and process structured data in a Data Warehouse for business intelligence.

## Interview Questions
1. **What is the difference between ETL and ELT?**
   *Answer:* ETL transforms data outside the target database before loading. ELT loads raw data into the target database first, then uses the database's compute engine to transform it.
2. **Compare a Data Warehouse and a Data Lake.**
   *Answer:* Warehouses store structured, processed data with schema-on-write, optimized for BI. Lakes store raw, unstructured data with schema-on-read, optimized for ML and low-cost storage.
3. **What problem does a Data Lakehouse solve?**
   *Answer:* It solves the two-tier architecture problem (moving data from Lake to Warehouse) by bringing Warehouse capabilities (ACID, fast SQL) directly to the cheap Data Lake storage layer using formats like Apache Iceberg or Delta Lake.
