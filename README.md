
docker exec -it 11f6e6ffa6bf /bin/bash
docker rm -f $(docker ps -aq)
Note:

# 1. Log in mysql:
docker exec -it <my_sql_container_id> /bin/bash
mysql -u root -p

# 2. Generate data 
```
pip install -U git+https://github.com/canhtran/dgscli
```
#### Generation
Generate the dummy car selling company data. Rules of thumbs:

- Number of inventory = Number of product
- Number of User = Number of User Details
- Number of Order = Number of Order Details.

##### Usage: dgscli generate [OPTIONS]

* Options:
  ```
  --data TEXT             Choose the dummy data: order, product, user
  --num INTEGER           Number of records
  --no_userid INTEGER     Number of user_id for orders
  --no_productid INTEGER  Number of product_id for orders
  --help                  Show this message and exit.
  ```

* Example commands
### Generate 100 products

``dgscli generate --data product --num 10`` 

### Generate 10 customers
$ dgscli generate --data users --num 10

### Generate 10 orders of 5 customers and 7 products
```dgscli generate --data order --num 10 --no_userid 5 --no_productid 7```

### Import data

1. Execute container mysql
```
docker exec -it <mysql-container-id> mysql -u root -p <password>
```
2. Check secure file prv
```
SHOW VARIABLES LIKE 'secure_file_priv';
```
This will show you the directory that is currently allowed.


3. Copy file into secure file to import
```
docker cp <path_from> <container_id>:/<path_target>
```
4. Execute sql file in mysql
```
source <path_file>
```
if you want to load csv file to table
```commandline
LOAD DATA INFILE '<file_path>'
INTO TABLE orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

This command starts a MySQL container named "mysql-container", sets the root password to "my-secret-pw", and maps the container's port 3306 to the host's port 3306.

Copy the CSV file to the container using a command like this:

Copy
docker cp /path/to/file.csv mysql-container:/tmp/file.csv
This command copies the CSV file located at "/path/to/file.csv" on the host to the "/tmp" directory in the "mysql-container" container.

Connect to the MySQL container using the mysql command-line client:

docker exec -it mysql-container mysql -uroot -pmy-secret-pw
This command runs the mysql client inside the "mysql-container" container and connects to the MySQL server as the root user with the password "my-secret-pw".

In the MySQL client, create a database and a table that matches the structure of the CSV file:

CREATE DATABASE my_database;
USE my_database;
CREATE TABLE my_table (col1 INT, col2 VARCHAR(255), col3 DATE);
Replace "my_database" and "my_table" with appropriate names for your database and table, and adjust the column names and data types to match your CSV file.

Load the data from the CSV file into the table using the LOAD DATA INFILE command:

LOAD DATA INFILE '/tmp/file.csv'
INTO TABLE my_table
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
Replace "/tmp/file.csv" with the path to your CSV file, and adjust the table name and column names to match your database and table.

Note that the LOAD DATA INFILE command assumes that the CSV file is formatted with commas as field separators, double quotes as field enclosures, and newlines as row separators. If your CSV file uses different delimiters or enclosures, you'll need to adjust the command accordingly.

That's it! Your CSV file should now be imported into the MySQL container's database and table. You can verify this by running queries in the MySQL client.




### Recreate only service when update docker-compose.yml file 
docker-compose up -d --no-deps <service-name>