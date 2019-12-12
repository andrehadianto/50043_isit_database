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
* The reviews are stored in a relational databases (SQL is recommended). 
* The metadata (book descriptions) is in a document store (MongoDB is recommended). 
* The web server logs are recorded in a document store. Each log record must have at least the following
information:
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
|Endpoint               |REST|Description|
|-----------------------|----|-----------|
|/book/:asin|GET | // Returns book details (all available fields), erroneous asin in array will be ignored
* Parameter: asin
* Body: json(id, asin, title, categories, imUrl, related?, price?, description?)|
|/books?page={}&count={}|GET | //Returns books information (lightweight) with pagination
* Body: Array of json(asin, title, imUrl?)
* Use Case: Home Page, viewing of ALL books|
|/books/previews/       |POST| // Returns books information (lightweight)
* Request Body: (asinArray) Array of string
* Response Body: Array of json(asin, title, imUrl)
* Use case: view also bought/also viewed/bought together|
|/books/category        |POST| // Returns books that have categories containing categories in categoryArray
* Request Body: (categoryArray) Array of string
* Response Body: Array of json(asin, title, imUrl)
* Use case: filtering of categories |
|/book/update/:asin     |PUT | // Updates book details
* Parameters: asin
* Body: json(title, categories, imUrl, related?, price?, description)|
|/category/all          |GET | // Returns all available book category
* Use Case: Add new book, selecting category
* Body: Array of json(category)|





### Analytics Backend
