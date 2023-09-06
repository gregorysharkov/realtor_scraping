# Australian real estate deals scraping

# Problem statement
What do you think of scraping the first 50 pages of this: https://www.realtor.com/realestateandhomes-search/Philadelphia_PA/show-recently-sold/pg-50
I need address of each listing sold, price it sold for, and date sold

# Solution
In this case we need to make a request to get list of individual deals and this page contains all information we need, so additional requests are not needed. The whole solution consists of 2 classes:
* DealList
* Deal

`DealList` class is responsible for sending request and parsing the results
`Deal` is responsible for all operations with retrieved deal information (store and represent in a form of a list)

The web site has a request counter, so if a multiple requests are sent from the same IP address, the results are no longer sent. Therefore the scrape script has multiple waiting windows.
