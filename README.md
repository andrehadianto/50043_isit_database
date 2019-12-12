# 50.043 Project

## Description
In this project, we built a web application for Kindle book reviews, similar to [Goodreads](https://goodreads.com).

### Dataset
We were provided with 2 public datasets from Amazon.
+ Amazon Kindle's reviews, available from [Kaggle website](https://www.kaggle.com/bharadwaj6/kindle-reviews). 
This dataset has 982,619 entries (about 700MB).
+ Amazon Kindle metadata, available from [UCSD website](http://jmcauley.ucsd.edu/data/amazon/)
This dataset has 434,702 products (about 450MB)


## Production Backend
### Requirements
* The web server receives requests and computes the responses by interacting with the databases. 
* The reviews are stored in a relational databases, we used MySQL.
* The metadata (book descriptions) is in a document store, we used MongoDB.
* The web server logs are recorded in a document store. Each log record must have at least the following information:
  + Timestamp
  + What type of request is being served
  + What is the response

### Production Backend Design
#### 1. Books Metadata
##### Schema (MongoDB)
* id: ObjectId, primary key
* asin: String
* title: String
* categories: String[]
* imUrl?: String
* related?: json
  + also_bought: string[]
  + also_viewed: string[]
  + bought_together: string[] 
* price?: Double
* description?: String
##### Endpoints
| Endpoint                    | REST | Description                                                  |
|-----------------------------|------|--------------------------------------------------------------|
| /book/:asin                 | GET  | Returns book details (all available fields), erroneous asin in array will be ignored<br/><ul><li>Parameter: asin</li><li>Body: json(id, asin, title, categories, imUrl, related?, price?, description?)</li></ul> |
| /books?page={}&count={}     | GET  | Returns books information (lightweight) with pagination<br/><ul><li>Body: Array of json(asin, title, imUrl?)</li><li>Use Case: Home Page, viewing of ALL books</li></ul> |
| /books/previews/            | POST | Returns books information (lightweight)<br/><ul><li>Request Body: (asinArray) Array of string</li><li>Response Body: Array of json(asin, title, imUrl)</li><li>Use case: view also bought/also viewed/bought together</li></ul> |
| /books/category             | POST | Returns books that have categories containing categories in categoryArray<br/><ul><li>Request Body: (categoryArray) Array of string</li><li>Response Body: Array of json(asin, title, imUrl)</li><li>Use case: filtering of categories</li></ul>|
| /book/new                   | POST | Adds a book to database<br/><ul><li>Body: json(title, categories?, imUrl, related?, price?, description)</li><li>Backend: perform check on imUrl (If empty: add in hard-coded url)</li></ul> |
| /book/update/:asin          | PUT  | Updates book details<br/><ul><li>Parameters: asin</li><li>Body: json(title, categories, imUrl, related?, price?, description)</li></ul> |
| /category/all               | GET  | Returns all available book category<br/><ul><li>Use Case: Add new book, selecting category</li><li>Body: Array of json(category)</li></ul> |
| /user/logs?page={}&count={} | GET  | Returns a list of logs<br/><ul><li>Body: count, logs(status code, method, path, body)</li></ul> |
| /user/logs/:id              | GET  | Returns a specific log in details<br/><ul><li>Parameters: ObjectId</li><li>Body: status code, time, method, path, body</li></ul> |
| /user/login                 | POST | Log in to an account into the website |
| /user/signup                | POST | Sign up a new account into the database |

#### 2. Kindle Reviews
##### Schema (MySQL)
* id: Integer, primary key
* asin: String
* helpful: String
* overall: Integer
* reviewText: Text
* reviewTime: String
* reviewerID: String
* reviewerName: String
* summary: String
* unixReviewTime: Integer
##### Endpoints    
| Endpoint                        | REST   | Description                                                  |
|---------------------------------|--------|--------------------------------------------------------------|
| /reviews/:asin?page={}&count={} | GET    | Returns reviews details (all fields) for a book with pagination<br/><ul><li>Body: Array of json(id, asin, helpful, overall, reviewText, reviewTime, reviewerID, reviewerName, summary, unixReviewTime)</li></ul> |
| /reviews/:asin                  | POST   | Adds a review to database<br/><ul><li>Body: json(asin, overall, reviewText, reviewerID, reviewerName, summary)</li></ul> |
| /reviews/user/:userid           | GET    | Returns all reviews by user<br/><ul><li>Body: Array of json(id, asin, helpful, overall, reviewText, reviewTime, reviewerID, reviewerName, summary, unixReviewTime</li></ul> |
| /review/:id                     | DELETE | Delete review |
| /review/:id                     | PUT    | Edit review by user<br/><ul><li>Body: json(overall, reviewText, summary)</li></ul> |



### Analytics Backend
