### Initialization

#### 1. Package installation
- make sure that you have the latest `node` installed in your local machine
- go to `/static`
- run `npm install`

#### 2. Development
React runs on javascript and it is not readable as pages on our browser. Webpack library helps us by compiling React codes into `bundle.js` which is then loaded using `babel-loader` into html file in `index.html`. Whenever changes is made, the `bundle.js` needs to be updated and recompiled.
tl;dr: run the command below before developing to automatically recompile whenever changes are made
- run `npm run watch` to build the page

#### 3. Production
Production `bundle.js` will ignore any dependencies listed in `DevDependencies` and most of the library modules files to further reduce the file size. This is to ensure that the file can be loaded quickly. To create production-ready bundle, run the code below.
- run `npm run prod` 

Project Structure  
static  
| src  
|-| components  
|-|-| AddReview.jsx  
|-|-| AllBooks.jsx  
|-|-| AlsoBought.jsx  
|-|-| BookPreviewList.jsx  
|-|-| LoginMenu.jsx  
|-|-| NavBar.jsx  
|-|-| SignUpMenu.jsx  
|-| pages  
|-|-| AddNewBook.jsx  
|-|-| BookDetails.jsx  
|-|-| home.jsx  
|-|-| LogPreview.jsx  
|-|-| NotFound404.jsx  
|-|-| SeeLogList.jsx  
|-|-| UserAction.jsx  
|-| router  
|-|-| AppRouter.jsx  
|-| styles  
|-|-| base  
|-|-| components  
|-|-| styles.scss
|-| index.jsx  
| public  
|-| bundle.js  
| .babelrc  
| favicon.ico  
| index.html  
| package-lock.json  
| package.json  
| webpack.config.js    
| README.md  
| .gitignore  