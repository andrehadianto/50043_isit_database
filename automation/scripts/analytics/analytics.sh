#!/usr/bin/env bash

# $1 key path, $2 namenode dns, $3 mongo ip, $4 mysql ip
echo "Getting kindle_metadata from mongo..."
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "mongoexport --uri=mongodb://admin:password@$3:27017/isit_database_mongo?authSource=admin --collection=kindle_metadata --out=/home/ubuntu/meta.json"

echo "Getting kindle_reviews from sql..."
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "mysql -u root -ppassword -h 54.255.139.159 --batch --raw -e 'select id, asin, reviewText FROM isit_database.kindle_reviews' > /home/ubuntu/kindle_reviews.tsv"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "tr '\t' ',' < /home/ubuntu/kindle_reviews.tsv > /home/ubuntu/kindle.csv"

scp -o StrictHostKeyChecking=no -i $1 "scripts/analytics/ACTIVATE.sh"  ubuntu@$2:/home/ubuntu/ACTIVATE.sh
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "chmod +x /home/ubuntu/ACTIVATE.sh"
ssh -o StrictHostKeyChecking=no -i $1 ubuntu@$2 "/bin/bash /home/ubuntu/ACTIVATE.sh"
