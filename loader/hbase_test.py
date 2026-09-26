import happybase

def test_hbase_connection():
    host = "localhost"
    port = 9090
    
    print(f"Connecting to HBase Thrift Server at {host}:{port}...")
    
    try:
        connection = happybase.Connection(host=host, port=port)
        connection.open()
        
        print("Successfully connected to HBase!")
        
        tables = connection.tables()
        print("Existing HBase tables:")
        if tables:
            for table in tables:
                print(f" - {table.decode('utf-8')}")
        else:
            print(" No tables found in HBase.")
            
        connection.close()
        
    except Exception as e:
        print(f"Failed to connect to HBase. Error: {e}")
        print("Ensure HBase and Thrift server are running (hbase thrift start -p 9090).")

if __name__ == "__main__":
    test_hbase_connection()