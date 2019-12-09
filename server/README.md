# Checkpoint 1
Implementation of production backend on local machine. That is, the web server and databases run on the same machine.

## Initialization

### 1. Python Virtual Environment
For Windows User
- run command prompt
- type `pip install virtualenv`

Creating a virtualenv
- go to server folder
- type `virtualenv .pyenv`

To activate the isolated virtualenv  
If you are using powershell or powershell-based VSCode terminal
- go to server folder
- run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once
- run `.\\.pyenv\Scripts\activate`

If you are using command prompt
- go to server folder
- run `.\\.pyenv\Scripts\activate`

Installing Python Dependencies
- go to server folder
- run `python -m pip install -r requirements.txt`

### 2. Use .env
- Create .env file in server folder
- Add in the following:
```
# Change values according to your local machine

SQL_DB=isit_database
SQL_HOST=localhost
SQL_USER=root
SQL_PW=

MONGO_HOST=localhost
MONGO_DB=isit_database_mongo
LOG_DB=log_mongo
```
### 3. Set up mongo database
(you can refer to `../automation/scripts/mongo_script.sh` from master branch)
- Install mongodb
- Create a new database called `isit_database_mongo`
- Download the `meta_kindle_store` data and the `categories.json` data:
  ```
  wget -c https://www.dropbox.com/s/7r3ajphm9vytn2b/categories.json?dl=0 -O categories.json
  ```
- run `mongod` in any shell (or using `sudo service mongod start`)
- Import the dataset into mongodb:
  ```
  mongoimport -d isit_database_mongo -c kindle_metadata --file meta_Kindle_Store.json  --legacy
  mongoimport -d isit_database_mongo -c categories --drop --file categories.json
  ``` 

### 4. Set up MYSQL database
- Install MYSQL version 5.7
- Run the following:
```
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
```

### 5. Set up front-end
(you can refer to `../automation/scripts/flash_script.sh` from master branch)
- Install nodejs, npm
- After installation, run:
```
# Install node modules
cd ../static
npm install
```
- run `npm run watch`

### 6. Running the Server
Running:
```
python app.py
```
Go to `http://localhost:5000/isit` 