# berlin_rental_prices

### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Results](#results)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>

1) To webscrape new listings install Scrapy:  `$ pip install scrapy`
2) To follow my analysis in the Jupyter Notebbok install the following packages:
    - Tabula to extract information fom PDFs: `$ pip pip install tabula-py`
    - FuzzyWuzzy to match strings: `$ pip install fuzzywuzzy`
    - Plotly for visualizations in the Jupyter Notebook: `$ pip install plotly`
    - Chart studio if you want to export your Plotly Visualisations: `$ pip install chart_studio`


## Project Motivation<a name="motivation"></a>

To stop the ever increasing costs of housing, the Berlin state government passed a controversial law that caps the rent. On February 23, the new law will come into effect.

As my next data science side project, I decided to analyse current online listings on ImmobilienScout24, to see whether current landlords already respect the new rent cap. 

1. How many listings had a higher price than the allowed rent cap?
2. How much more per month would all tenants pay than they had to under the new rent cap?
3. How much would the average cold rent decrease under the new law?
4. What is the distribution of the excess rent under the new law?
5. How would the average cold rent price change per district?
6. Which big real estate firms are charging the most excess rent?

## File Descriptions and Getting Started <a name="files"></a>

To run the spider/web crawler:
1) Go to the base folder **berlin_rental_prices** and change to the subfolder **berlin_rental_prices** (`$ cd berlin_rental_prices`)
2) Run the spider in your terminal with `scrapy crawl immo_scraper -o your_file_name.csv`

To run the jupyter noteebook:
1) Navigate to the following folder:  **berlin_rental_prices** ->  **berlin_rental_prices** -> **berlin_rental_prices**
2) Open the **data_analysis.ipynb** Jupyter Notebook

## Results<a name="results"></a>

The main findings of the code can be found at the post available [here](https://medium.com/@felix.vemmer/1-week-until-the-berlin-rent-freeze-how-many-illegal-overpriced-offers-can-i-find-online-6e5511d49e5a).

## Licensing, Authors, Acknowledgements<a name="licensing"></a>

Must give credit to the author for the data. Otherwise, feel free to use the code here as you would like! 
