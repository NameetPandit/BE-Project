import mysql.connector

# Function to connect to MySQL
def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Change this
        password="root",  # Change this
        database="vehicle_access"
    )
    return conn

# Function to insert data into the database
def save_to_db(plate_number, owner_name):
    conn = connect_db()
    cursor = conn.cursor()
    
    sql = "INSERT INTO license_plates (plate_number, owner_name) VALUES (%s, %s)"
    values = (plate_number, owner_name)
    cursor.execute(sql, values)
    conn.commit()

    print(f"✅ Saved to DB: {plate_number} - {owner_name}")

    cursor.close()
    conn.close()