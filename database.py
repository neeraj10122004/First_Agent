import sqlite3
import os

# File path
database_file_path = './sql_lite_database.db'

# Check if database file exists and delete if it does
if os.path.exists(database_file_path):
    os.remove(database_file_path)
    message = "File 'sql_lite_database.db' found and deleted."
else:
    message = "File 'sql_lite_database.db' does not exist."

# Step 1: Connect to the database or create it if it doesn't exist
conn = sqlite3.connect(database_file_path)

# Step 2: Create a cursor
cursor = conn.cursor()

# Step 3: Create tables
create_table_query1 = """
                        CREATE TABLE IF NOT EXISTS   "SUPPLIER"
                        (
                            "SUPPLIER_ID" CHAR(6) NOT NULL PRIMARY KEY,
                            "SUPPLIER_NAME" CHAR(40),
                            "SUPPLIER_ADDRESS" CHAR(35),
                            "SUPPLIER_CONTACT" CHAR(15)
                            );
                        """

create_table_query2 = """
                        CREATE TABLE IF NOT EXISTS   "PRODUCT"
                        (	"PRODUCT_ID" VARCHAR2(6) NOT NULL PRIMARY KEY,
                            "PRODUCT_NAME" VARCHAR2(40) NOT NULL,
                            "PRODUCT_DESCRIPTION" CHAR(35),
                            "PRODUCT_PRICE" FLOAT,
                            "SUPPLIER_ID" CHAR(6) NOT NULL REFERENCES SUPPLIER
                        );
                        """

create_table_query3 = """
                        CREATE TABLE IF NOT EXISTS "INVENTORY"
                        (
                            "INVENTORY_ID" NUMBER(6,0) NOT NULL PRIMARY KEY,
                            "PRODUCT_ID" VARCHAR2(6) NOT NULL REFERENCES PRODUCT,
                            "QUANTITY" NUMBER(6,0) NOT NULL,
                            "MIN_STOCK" NUMBER(6,0) NOT NULL
                        );
                        """

queries = [create_table_query1, create_table_query2, create_table_query3]
# queries = [create_table_query1, create_table_query2]

for query in queries:
    # execute queries
    cursor.execute(query)

# Step 4: Insert data into tables Agents, Orders and Customers
insert_query = """
INSERT INTO SUPPLIER VALUES ('A001','Samsung Electronics', 'Seoul, South Korea', '800-726-7864');
INSERT INTO SUPPLIER VALUES ('A002','Apple Inc.', 'Cupertino, California, USA', '800–692–7753');
INSERT INTO SUPPLIER VALUES ('A003','OnePlus Technology', 'Shenzhen, Guangdong, China', '400-888-1111');
INSERT INTO SUPPLIER VALUES ('A004','Google LLC', 'Mountain View, California, USA', '855-836-3987');
INSERT INTO SUPPLIER VALUES ('A005','Xiaomi Corporation', 'Beijing, China', '1800-103-6286');
INSERT INTO PRODUCT VALUES ('P001','Samsung Galaxy S21', 'Samsung flagship smartphone',799.99,'A001');
INSERT INTO PRODUCT VALUES ('P002','Samsung Galaxy Note 20', 'Samsung premium smartphone with stylus',999.99,'A001');
INSERT INTO PRODUCT VALUES ('P003','iPhone 13 Pro', 'Apple flagship smartphone',999.99,'A002');
INSERT INTO PRODUCT VALUES ('P004','iPhone SE', 'Apple budget smartphone',399.99,'A002');
INSERT INTO PRODUCT VALUES ('P005','OnePlus 9', 'High performance smartphone',729.00,'A003');
INSERT INTO PRODUCT VALUES ('P006','OnePlus Nord', 'Mid-range smartphone',499.00,'A003');
INSERT INTO PRODUCT VALUES ('P007','Google Pixel 6', 'Googles latest smartphone',599.00,'A004');
INSERT INTO PRODUCT VALUES ('P008','Google Pixel 5a', 'Affordable Google smartphone',449.00,'A004');
INSERT INTO PRODUCT VALUES ('P009','Xiaomi Mi 11', 'Xiaomi high-end smartphone',749.99,'A005');
INSERT INTO PRODUCT VALUES ('P0010','Xiaomi Redmi Note 10', 'Xiaomi budget smartphone',199.99,'A005');
INSERT INTO INVENTORY VALUES(1, 'P001',150,30);
INSERT INTO INVENTORY VALUES(2, 'P002',100,20);
INSERT INTO INVENTORY VALUES(3, 'P003',120,30);
INSERT INTO INVENTORY VALUES(4, 'P004',80,15);
INSERT INTO INVENTORY VALUES(5, 'P005',200,40);
INSERT INTO INVENTORY VALUES(6, 'P006',150,25);
INSERT INTO INVENTORY VALUES(7, 'P007',100,20);
INSERT INTO INVENTORY VALUES(8, 'P008',90,18);
INSERT INTO INVENTORY VALUES(9, 'P009',170,35);
INSERT INTO INVENTORY VALUES(10, 'P0010',220,45);
"""

for row in insert_query.splitlines():
    try:
        cursor.execute(row)
    except:
        print(f"An error occurred")
        print(row)

# Step 5: Fetch data from tables
list_of_queries = []
list_of_queries.append("SELECT * FROM SUPPLIER")
list_of_queries.append("SELECT * FROM PRODUCT")
list_of_queries.append("SELECT * FROM INVENTORY")

# execute queries
for query in list_of_queries:
    cursor.execute(query)
    data = cursor.fetchall()

    print(f"--- Data from tables ({query}) ---")
    for row in data:
        print(row)

# Step 7: Close the cursor and connection
cursor.close()
conn.commit()
conn.close()