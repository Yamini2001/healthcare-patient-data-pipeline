# Healthcare Patient Medical Records Analytics & NoSQL Serving Engine

A Big Data pipeline built on **Hadoop (HDFS)**, **PySpark**, and **Apache HBase** to ingest, process, and serve patient visit records for batch analysis and fast NoSQL point-lookups.

---

## Architecture Overview

1. **Ingestion Layer:** Raw patient visit logs (`healthcare_visits.csv`) ingested into **HDFS** (`/healthcare/input/`).
2. **Batch Analytics Layer:**
   - **PySpark:** Computes patient-level aggregations (total visit counts and overall billing amounts).
   - **Python MapReduce:** Calculates department-wise visit distributions using Hadoop Streaming.
3. **Serving Layer:** Processed PySpark output and visit logs are automatically loaded into **Apache HBase** via a Python client (**HappyBase**) over Thrift protocol.
4. **Data Retrieval:** Optimized compound row keys (`Patient_ID#Visit_ID`) enable sub-second record retrieval using HBase `GET` and `SCAN` operations.

---

## Tech Stack

- **Storage:** Apache Hadoop HDFS
- **Processing:** PySpark, Python MapReduce
- **NoSQL Database:** Apache HBase (Thrift Server)
- **Programming & Tools:** Python 3, HappyBase API, Linux/Bash

---

## Data Schema & Design

### HBase Tables
1. **`patient_visits`**
   - **Row Key:** `Patient_ID#Visit_ID` (e.g., `P101#V001`)
   - **Column Families:** `patient`, `visit`, `medical`, `billing`
2. **`patient_analytics`**
   - **Row Key:** `Patient_ID` (e.g., `P101`)
   - **Column Family:** `analytics` (`visit_count`, `total_amount`)

---

## How to Run

### 1. Start Services
Ensure HDFS, YARN, HBase, and HBase Thrift Server are active:
```bash
start-all.sh
start-hbase.sh
nohup hbase thrift start -p 9090 > /tmp/hbase-thrift.log 2>&1 &
