### Initialization

#### 1. Package installation
- make sure that you have `node` installed in your local machine
- go to `/static`
- run `npm install`

#### 2. Development
React runs on javascript and it is not readable as pages on our browser. Webpack library helps us by compiling React codes into `bundle.js` which is then loaded using `babel-loader` into html file in `index.html`. Whenever changes is made, the `bundle.js` needs to be updated and recompiled.
tl;dr: run the command below before developing to automatically recompile whenever changes are made
- run `npm run watch` to build the page

Project Structure  
static  
| src  
|-| components  
|-| pages  
|-| router  
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