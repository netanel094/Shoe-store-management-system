from dotenv import load_dotenv
import os
import mysql.connector as cn

# Load environment variables from .env file
load_dotenv()

try:
    # Connect to the MySQL server without specifying a database
    mydb = cn.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD")
    )

    if mydb.is_connected():
        print("Connected to MySQL!")

    # Create the database if it doesn't exist
    create_database_query = f"CREATE DATABASE IF NOT EXISTS {os.getenv('DATABASE')}"
    mycursor = mydb.cursor()
    mycursor.execute(create_database_query)
    print("Database created or already exists")

    # Connect to the specific database
    mydb = cn.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE")
    )
    if mydb.is_connected():
        print(f"Connected to {os.getenv('DATABASE')}")

except cn.Error as e:
    print(f'Error connecting to MySQL: {e}')


# Define table creation queries
table_queries = [
    '''
    CREATE TABLE IF NOT EXISTS Customers (
        phone VARCHAR(20) PRIMARY KEY,
        name VARCHAR(255),
        order_id INT
    )
    ''',
    '''
  CREATE TABLE IF NOT EXISTS Shoes (
    numModel INT,
    color VARCHAR(50),
    size INT,
    quantity INT,
    floor INT,
    season VARCHAR(50),
    PRIMARY KEY (numModel, color, size, season)
)
    ''',
    '''
    CREATE TABLE IF NOT EXISTS Orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        phone VARCHAR(20),
        numModel INT,
        order_date DATE,
        quantity INT,
        price DECIMAL(10, 2),
        FOREIGN KEY (phone) REFERENCES Customers(phone),
        FOREIGN KEY (numModel) REFERENCES Shoes(numModel)
    )
    '''
]

try:
    # Get the cursor before executing the queries
    mycursor = mydb.cursor()

    for query in table_queries:
        mycursor.execute(query)
    print("Tables created successfully")

except cn.Error as e:
    print(f'Error creating tables: {e}')
