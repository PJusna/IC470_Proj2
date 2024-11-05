import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Fetch all submissions
cursor.execute('SELECT * FROM submissions')
submissions = cursor.fetchall()

# Print the results
for submission in submissions:
    print(submission)

# Close the connection
conn.close()
