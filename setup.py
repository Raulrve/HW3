import sqlite3

conn = sqlite3.connect('reviewData.db')
print("Opened database successfully")

conn.execute('CREATE TABLE Reviews (Username VARCHAR(40), Restaurant VARCHAR(50), ReviewTime TEXT, Rating FLOAT, Review VARCHAR(500))')
print("Table created successfully")
conn.execute('CREATE TABLE Ratings (Restaurant VARCHAR(50), Food FLOAT, Service FLOAT, Ambience FLOAT, Price FLOAT, Overall FLOAT)')
print("Table created successfully")
conn.close()