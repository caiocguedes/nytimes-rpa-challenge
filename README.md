NEW YORK TIMES RPA CHALLENGE

This project consists in an RPA automation using Python and RPA Framework (rpaframework.org), executing the following steps:

- Extract data from https://nytimes.com, using 3 configured variables, that can be found in config.ini (in this project we will use only 2 - the website data filter wasn't working properly):
  - search phrase
  - news category
  - number of months for which you need to receive news (excluded from the project due to the website data filter issue)

The main steps:

- Open the site
- Enter a phrase in the search field
- On the result page, apply the following filters:
    - select a news category (specified in the config.ini file)
    - choose the latest (newest) news
- Get the values: title, date and description
- Store in an Excel file:
    - title
    - date
    - description (if available, there are some news without description)
    - True or False, depending on whether the title or description contains any amount of money (Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD)
- Download the news picture and specify the file name in the Excel File (pictures stored in Pictures folder)
  

