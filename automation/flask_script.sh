#!/bin/bash

# Download pip3 and virtualenv
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv

# Download code
wget -c https://www.dropbox.com/s/km4f6rwzyjq1gl1/50043_isit_database.zip?dl=0 -O 50043_isit_database.zip
sudo apt install unzip
unzip 50043_isit_database.zip

# Create virtualenv and install dependencies
cd 50043_isit_database/server && python3 -m venv .pyenv
source .pyenv/bin/activate
python -m pip install -r requirements.txt

# Install node modules
cd ../static
sudo apt install -y npm
npm install

# Create .env 
cd ../server

cat >> .env << EOF
SQL_DB=isit_database
SQL_USER=root
SQL_PW=password
SQL_HOST=$1
MONGO_DB=isit_database_mongo
LOG_DB=log_mongo
MONGO_HOST=$2
EOF

touch /home/ubuntu/script-finished

# Run flask app
python app.py