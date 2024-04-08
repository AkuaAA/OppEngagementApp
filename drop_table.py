import sqlite3

# Connect to your database
conn = sqlite3.connect('db.sqlite')

# Create a cursor object
c = conn.cursor()

# Execute the DROP TABLE command
c.execute("DROP TABLE IF EXISTS _alembic_tmp_employees")

# Query for all table names
c.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Print all table names
print(c.fetchall())

# Commit the transaction
conn.commit()

# Close the connection
conn.close()