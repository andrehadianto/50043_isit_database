# MongoDB
## Books Metadata
### kindle_metadata
- id: String, primary key
- asin: String
- categories: String[]
- imUrl?: String
- related?: String[]
- price?: Double
- description?: String
## Logs

# MySQL
## Kindle Reviews
### kindle_reviews
- id: Integer, primary key
- asin: String
- helpful: String
- overall: Integer
- reviewText: Text
- reviewTime: String
- reviewerID: String
- reviewerName: String
- summary: String
- unixReviewTime: Integer