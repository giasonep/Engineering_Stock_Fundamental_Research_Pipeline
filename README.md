# Stock Fundamental Research Pipeline
Metis Data Engineering Module 3 Project

## ABSTRACT

I built a pipeline to pull data from QuickFS.net’s API, which is a service that provides its users financial data from publicly traded companies’ quarterly filings with the SEC. I cleaned the pulled data with Pandas’ software and saved the results using SQLite to SQL databases. I then used the databases along with Streamlit to build a web application that performs fundamental analysis on over two thousand stocks with over five million data entry points. This analysis provides users with a proprietary score, in addition to other visual metrics, to identify securities displaying powerful fundamental characteristics. I then pushed the databases along with the web app to Heroku, a cloud application hosting service, where my site is publicly available across the world wide web: 

[Click here: POWERFUL Stock Fundamentals Research Tool](https://frozen-escarpment-19997.herokuapp.com/)

### Install
 The following libraries are required for this project:
 
  - NumPy
  - Pandas
  - Plotly
  - Requests
  - Yahoo Finance
  - SQLite
  - SQLAlchemy
  
---> **Hosting**
  - Streamlit
  - Heroku

### Data
  - [QuickFS.net](https://quickfs.net/)
