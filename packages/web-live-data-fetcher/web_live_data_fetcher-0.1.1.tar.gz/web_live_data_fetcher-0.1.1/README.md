# Web Live Data Fetcher

A Python package for retrieving and summarizing live data from web searches by performing Google searches and extracting content from the top search results.

## Installation

You can install the package via pip:

 ```sh
 pip install web_live_data_fetcher
 ```

# Usage

The web_live_data_fetcher package allows you to search for a query on Google, fetch the content of the top results, and extract the text content from the body of the webpages.

 ```python
 from web_live_data_fetcher import live_data
 
 query = "What is the weather like in Bangalore right now?"
 data = live_data(query)
 print(data)
 ```

# License

This project is licensed under the Apachi License. See the LICENSE file for more details.

# Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.