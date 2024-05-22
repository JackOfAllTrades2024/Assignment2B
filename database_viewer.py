import sqlite3

# Connect to the database
conn = sqlite3.connect('reliability_ratings.db')
cursor = conn.cursor()

# Execute a query to retrieve data from a table
cursor.execute("SELECT * FROM ratings")

# Fetch all the rows from the query result
rows = cursor.fetchall()

# Display the data
for row in rows:
    print(row)

# Close the database connection
conn.close()