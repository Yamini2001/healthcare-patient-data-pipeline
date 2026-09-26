# Healthcare Patient Data Pipeline

A Big Data processing pipeline built with Hadoop (HDFS, MapReduce), PySpark, and Apache HBase to ingest, analyze, and serve patient medical visit records.

---

Directory Structure

```text
healthcare-hbase-project/
├── data/
│   └── healthcare_visits.csv
├── mapreduce/
│   ├── mapper.py
│   └── reducer.py
├── pyspark/
│   └── patient_analytics.py
└── loader/
    ├── hbase_test.py
    └── load_to_hbase.py
```

## Prerequisites & Service Startup
Start Hadoop services, HBase, and the HBase Thrift server.

## 1. Start Hadoop (HDFS & YARN)
start-dfs.sh
start-yarn.sh

## Verify Hadoop processes (NameNode, DataNode, ResourceManager, etc.)
jps

## 2. Start HBase
start-hbase.sh

## Verify HBase processes (HMaster, HRegionServer)
jps

## 3. Start HBase Thrift Server (Required for Python HappyBase)
nohup hbase thrift start -p 9090 > /tmp/hbase-thrift.log 2>&1 &

## Step 1: Upload Raw Data to HDFS
Create project directories in HDFS and upload the raw dataset.

## Create HDFS directories
hdfs dfs -mkdir -p /healthcare/input
hdfs dfs -mkdir -p /healthcare/mapreduce
hdfs dfs -mkdir -p /healthcare/analytics

## Upload dataset to HDFS
hdfs dfs -put -f data/healthcare_visits.csv /healthcare/input/

## Verify uploaded file
hdfs dfs -ls /healthcare/input
hdfs dfs -cat /healthcare/input/healthcare_visits.csv

## Step 2: Run Hadoop MapReduce Streaming
Process department-wise visit distributions using Python MapReduce streaming.

## Test Mapper locally
cat data/healthcare_visits.csv | python3 mapreduce/mapper.py

## Test MapReduce locally
cat data/healthcare_visits.csv | python3 mapreduce/mapper.py | sort | python3 mapreduce/reducer.py

## Remove previous output directory if it exists
hdfs dfs -rm -r -f /healthcare/mapreduce/department_output

## Run MapReduce job on Hadoop cluster
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -files mapreduce/mapper.py,mapreduce/reducer.py \
  -input /healthcare/input/healthcare_visits.csv \
  -output /healthcare/mapreduce/department_output \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py"

## Check MapReduce output in HDFS
hdfs dfs -cat /healthcare/mapreduce/department_output/part-*

## Step 3: Run PySpark Patient Analytics
Execute PySpark analytics to aggregate total visits and billing amounts per patient.

## Run PySpark job
spark-submit pyspark/patient_analytics.py

## Check PySpark output in HDFS
hdfs dfs -ls /healthcare/analytics/patient_analytics
hdfs dfs -cat /healthcare/analytics/patient_analytics/part-*

## Merge PySpark results to local file system for HBase loading
hdfs dfs -getmerge /healthcare/analytics/patient_analytics /tmp/patient_analytics.csv

## Step 4: Create HBase Tables
Create required NoSQL tables and column families using the HBase shell.

## Open HBase shell
hbase shell

Inside HBase shell, run:

## Create patient visits table with column families
create 'patient_visits', 'patient', 'visit', 'medical', 'billing'

## Create patient analytics table
create 'patient_analytics', 'analytics'

## List tables to confirm
list

## Exit HBase shell
exit

## Step 5: Automated Ingestion into HBase
Run Python scripts to test Thrift connection and load processed datasets into HBase tables.

## 1. Test HBase Thrift Connection
python3 loader/hbase_test.py

## 2. Automatically load data into HBase tables
python3 loader/load_to_hbase.py

## Step 6: Query and Verify HBase Data
Verify data storage and sub-second retrieval using row-key queries in the HBase shell.

## Open HBase shell
hbase shell

Inside HBase shell, run:

## Scan all patient visit records
scan 'patient_visits'

## Retrieve specific visit using compound row key (Patient_ID#Visit_ID)
get 'patient_visits', 'P101#V001'

## Scan aggregated patient analytics
scan 'patient_analytics'

## Retrieve single patient analytics summary
get 'patient_analytics', 'P103'

## Exit HBase shell
exit
