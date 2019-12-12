## Initialization
### Package installation
-----
- make sure that you have the latest `node>=10.0.0` and `npm>=6.0.0` installed in your local machine
- go to `/static`
- run `npm install`

### Development
-----
#### Generating bundle.js for Development
React runs on javascript and it is not readable as pages on our browser. Webpack library helps us by compiling React codes into `bundle.js` which is then loaded using `babel-loader` into html file in `index.html`. Whenever changes is made, the `bundle.js` needs to be updated and recompiled. Development will set all host to be set to `http://localhost:5000` by default when retrieving data from the databases.
tl;dr: run the command below before developing locally to automatically recompile whenever changes are made
- run `npm run watch` to build the page  
- enter `localhost:5000/init` on the search bar to access the homepage  

#### Generating bundle.js for Production
Production `bundle.js` will ignore any dependencies listed in `DevDependencies` and most of the library modules files to further reduce the file size. This is to ensure that the file can be loaded quickly. To create production-ready bundle, run the code below. Production will set the host to be `http://52.7.180.215:5000`.
- run `npm run prod`  


## Project Structure
-----
#### File Structure
static  
| src  
| - | components  
| - | - | AllBooks.jsx  
| - | - | AlsoBought.jsx  
| - | - | BookPreviewList.jsx  
| - | - | BookSearch.jsx  
| - | - | CategoryFilter.jsx  
| - | - | LoginMenu.jsx  
| - | - | NavBar.jsx  
| - | - | SignUpMenu.jsx  
| - | pages  
| - | - | AddNewBook.jsx  
| - | - | BookDetails.jsx  
| - | - | home.jsx  
| - | - | LogPreview.jsx  
| - | - | NotFound404.jsx  
| - | - | SeeLogList.jsx  
| - | router  
| - | - | AppRouter.jsx  
| - | styles  
| - | - | base  
| - | - | - | _base.scss  
| - | - | styles.scss
| - | index.jsx  
| public  
| - | bundle.js  
| .babelrc  
| favicon.ico  
| index.html  
| package-lock.json  
| package.json  
| webpack.config.js    
| README.md  
| .gitignore  

## Features
-----
![Homepage](/static/images/01.png)  
Homepage of our webiste shows a list of all books available in our database. User may sign up and login to our website.  

![Filter](/static/images/02.png)  
Filter the books by multiple categories. Type inside the input form for category suggestions.  

![Filtered Book](/static/images/07.png)  
Filtered books will show the filtered categories in the labels by upper-left corner.  

![Search](/static/images/03.png)  
Search a book by its asin code.  

![Login](/static/images/04.png)  
User may login to gain access to user-only features.  

![Signup](/static/images/06.png)  
User may sign up a new account. Username is unique.  

![User-only Features](/static/images/05.png)  
User-only features consist of Adding new books, Seeing logs, and logging out.  

![Book details](/static/images/09.png)  
Selecting a book will show the book details. You can see the title if available, the genre, author, description, and its price. Below shows all the available reviews by other users and the overall ratings.  

![Share a review](/static/images/10.png)  
Anonymous user may post a review using a nickname of their own choice.  

![Share a review logged in](/static/images/08.png)  
Logged in user does not have to choose a nickname and their review will be based on their entered display name.  

![Add new book](/static/images/11.png)  
Logged in user can add a new book. The preview of the book can be seen before submitting the book.  

![Successfully add new book](/static/images/14.png)  
User can check the details of successful new book submission immediately.  

![List of logs](/static/images/12.png)  
Logged in user may see the list of logs.  

![Log details](/static/images/13.png)  
Details of a log.  

