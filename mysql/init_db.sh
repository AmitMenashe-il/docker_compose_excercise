echo "******** Creating DB, Tables and user"

mysql -u root -p$MYSQL_ROOT_PASSWORD --execute \
"
SET TIME_ZONE='israel';
CREATE DATABASE IF NOT EXISTS $DB_NAME;
CREATE TABLE $DB_NAME.$COUNT_TABLE (
        id int not null auto_increment primary key,
        counter int
    );
INSERT INTO $DB_NAME.$COUNT_TABLE (counter) VALUES (0);
CREATE TABLE $DB_NAME.$LOG_TABLE (
        id int not null auto_increment primary key,
        client_ip varChar(15),
        internal_ip varChar(15),
        timestamp TIMESTAMP
    );
CREATE USER '$USER_NAME'@'%' IDENTIFIED BY '$USER_PASSWORD';
GRANT SELECT, INSERT, UPDATE ON $DB_NAME.$COUNT_TABLE TO '$USER_NAME'@'%';
GRANT SELECT, INSERT, UPDATE ON $DB_NAME.$LOG_TABLE TO '$USER_NAME'@'%';
FLUSH PRIVILEGES;
"

echo "******** Finished creating DB, Table and user"