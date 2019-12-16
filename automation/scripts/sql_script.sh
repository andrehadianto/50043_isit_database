#!/bin/bash

yum update -y
yum install mysql57-server -y

service mysqld start

mysql -u root <<'EOF'
UPDATE mysql.user SET authentication_string=PASSWORD('password') WHERE User='root';
DELETE FROM mysql.user WHERE User='';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';
FLUSH PRIVILEGES;
EOF

mysql -u root -ppassword -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'password'"
mysql -u root -ppassword -e "FLUSH PRIVILEGES"

service mysqld restart
chkconfig mysqld on

# Download dataset
wget -c wget -c https://istd50043.s3-ap-southeast-1.amazonaws.com/kindle-reviews.zip -O kindle-reviews.zip -O kindle-reviews.zip
unzip kindle-reviews.zip
rm -rf kindle_reviews.json

# Load csv into database
mysql -u root -ppassword <<'EOF'
CREATE SCHEMA isit_database;
CREATE TABLE isit_database.kindle_reviews(
`id` INT(11) NOT NULL AUTO_INCREMENT,
`asin` VARCHAR(255) NOT NULL,
`helpful` VARCHAR(255) NOT NULL,
`overall` INT(11) NOT NULL,
`reviewText` TEXT NOT NULL,
`reviewTime` VARCHAR(255) NOT NULL,
`reviewerID` VARCHAR(255) NOT NULL,
`reviewerName` VARCHAR(255) NOT NULL,
`summary` VARCHAR(255) NOT NULL,
`unixReviewTime` INT(11) NOT NULL,PRIMARY KEY (`id`));
SET sql_mode='NO_AUTO_VALUE_ON_ZERO';
LOAD DATA LOCAL INFILE 'kindle_reviews.csv' INTO TABLE isit_database.kindle_reviews FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
EOF

touch /home/ec2-user/script-finished.txt