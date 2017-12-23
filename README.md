# Amazon-Nike Compare

## General Overview
* The purpose of this web application is to collect data for Nike products from amazon.com and nike.com, analyze the data, and then present the data for the user to compare the prices on the two websites.
* The user can then search the results using specific details such as product descriptions, prices or ratings.
* The average prices of a particular product on amazon.com and nike.com are calculated and then visualized as a bar chart.

## Technical Overview
* AngularJS 1.x
*	Python Flask, requests, beautifulSoup
*	Bootstrap
*	D3.js
*	Angular Material

## Getting Started
This app uses python’s flask to implement the server so install flask if necessary.
To get started, clone the repository, and run python app.py:
```
git clone <this repo>
cd <this project folder>
python app.py
```
This will start a web server on port 5000.

## Development
### Backend
Python modules were used to build the server, scrape the data, and perform the data analysis. The server was implemented with flask and bs4 was used to scrape data from amazon.com and nike.com. Given a keyword, the bs4 makes search requests to amazon.com and nike.com by passing the keyword as a query string in the URL. It then downloads the returned HTML files and selects from the HTML tree the required HTML elements with certain classes and/or attributes. The selected relevant data is then saved into a JSON file to be used as the model in Angular’s MVC.

### Frontend
The application itself was built with AngularJS and the user interface was designed with twitter’s bootstrap. Angular Material was conveniently used to build most of the UI features. D3.js is used to draw the bar chart using the average prices from Nike.com every time a product is searched

## Challenges
### Cache
After searching for a product for the first time, the browser caches the JSON files and so the same results will appear for a different product unless the developer tools in chrome is opened while searching. For further improvements, the program should version the JSON files.

### Scraping Amazon
Developing a strategy to scrape nike.com was much less time consuming than developing a way to scrape amazon.com. The HTML class names for the prices on Amazon are not consistent and so given some keywords the program will return an error as it will not be able to scrape any data. For further improvements, the scraping method should be revised so that it can detect different HTML class names and scrape the data accordingly.
