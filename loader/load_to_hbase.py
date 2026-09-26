import csv
import os
import happybase

HBASE_HOST = "localhost"
HBASE_PORT = 9090

def load_data():
    print("Connecting to HBase...")
    connection = happybase.Connection(host=HBASE_HOST, port=HBASE_PORT)
    connection.open()
    print("Connected to HBase.")

    visit_table = connection.table("patient_visits")
    analytics_table = connection.table("patient_analytics")

    # 1. Load Raw Patient Visit Records
    visit_file = "data/healthcare_visits.csv"
    if os.path.exists(visit_file):
        print(f"\nLoading patient visit records from {visit_file}...")
        with open(visit_file, "r") as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                # Compound Row Key: Patient_ID#Visit_ID
                row_key = f"{row['Patient_ID']}#{row['Visit_ID']}"
                
                data = {
                    b"patient:id": row["Patient_ID"].encode(),
                    b"visit:id": row["Visit_ID"].encode(),
                    b"visit:doctor": row["Doctor"].encode(),
                    b"visit:department": row["Department"].encode(),
                    b"visit:date": row["Visit_Date"].encode(),
                    b"medical:diagnosis": row["Diagnosis"].encode(),
                    b"medical:medicine": row["Medicine"].encode(),
                    b"billing:amount": row["Amount"].encode()
                }
                
                visit_table.put(row_key.encode(), data)
                count += 1
        print(f"Patient visit records loaded: {count}")
    else:
        print(f"Error: {visit_file} not found.")

    # 2. Load Processed PySpark Patient Analytics
    analytics_file = "/tmp/patient_analytics.csv"
    if os.path.exists(analytics_file):
        print(f"\nLoading patient analytics from {analytics_file}...")
        with open(analytics_file, "r") as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                # Row Key: Patient_ID
                row_key = row["Patient_ID"]
                
                data = {
                    b"analytics:visit_count": row["Visit_Count"].encode(),
                    b"analytics:total_amount": row["Total_Amount"].encode()
                }
                
                analytics_table.put(row_key.encode(), data)
                count += 1
        print(f"Patient analytics records loaded: {count}")
    else:
        print(f"Warning: {analytics_file} not found. Run 'hdfs dfs -getmerge' first.")

    connection.close()
    print("\nHBase loading process completed.")

if __name__ == "__main__":
    load_data()