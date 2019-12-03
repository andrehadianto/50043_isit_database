#!/bin/bash

# Download pip3 and virtualenv
sudo apt-get update
sudo apt-get install -y python3-pip
curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt install -y nodejs
nodejs -v
npm -v

# Download code
wget -c https://www.dropbox.com/s/x6pcb278trb2hrn/50043_isit_database-master.zip?dl=0 -O 50043_isit_database.zip
sudo apt install unzip
unzip 50043_isit_database.zip

# Create virtualenv and install dependencies
cd 50043_isit_database-master/server && python3 -m venv .pyenv
# source .pyenv/bin/activate
# python -m pip install -r requirements.txt
touch log.txt
python3 -m pip install -r requirements.txt
chmod +x app.py
chmod a+rwx log.txt

# Install node modules
cd ../static
npm install
LOCAL_PUBLIC_IP=$(curl ifconfig.co)
export LOCAL_PUBLIC_IP
echo $LOCAL_PUBLIC_IP
npx webpack --env.API_URL=http://$LOCAL_PUBLIC_IP:5000 --progress -p --mode=production --config webpack.config.js 

# # Create .env 
# # cd ../server

# cat >> .env << EOF
# SQL_DB=isit_database
# SQL_USER=root
# SQL_PW=password
# SQL_HOST=$1
# MONGO_DB=isit_database_mongo
# LOG_DB=log_mongo
# MONGO_HOST=$2
# EOF

# touch /home/ubuntu/script-finished.txt

# # Run flask app
# python app.py