import mysql.connector

# Connect to the RDS instance
conn = mysql.connector.connect(
    host='your-rds-endpoint.rds.amazonaws.com',
    user='your_username',
    password='your_password',
    database='your_database_name'
)

# Create a cursor object
cursor = conn.cursor()

# Execute a query
cursor.execute("SELECT * FROM your_table")

# Fetch and print results
for row in cursor.fetchall():
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()