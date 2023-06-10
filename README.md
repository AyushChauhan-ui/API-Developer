**Trade Data API Solution Document**

# Solution Overview
The Trade Data API is designed to provide endpoints for retrieving, searching, and filtering trade data. It is built using the Python Flask framework and utilizes a mocked database for storing and retrieving trade information.

# Endpoints and Functionality
1. GET /trades - Fetches a list of trades. Supports filtering, pagination, and sorting.

Query Parameters:

page (optional): Specifies the page number for pagination (default is 1).
per_page (optional): Specifies the number of trades per page (default is 10).
assetClass (optional): Filters trades based on the asset class.
start (optional): Filters trades based on the minimum trade date.
end (optional): Filters trades based on the maximum trade date.
minPrice (optional): Filters trades based on the minimum trade price.
maxPrice (optional): Filters trades based on the maximum trade price.
tradeType (optional): Filters trades based on the trade type (BUY or SELL).
search (optional): Searches for trades based on a text query across multiple fields.

2. GET /trades/{trade_id} - Fetches a single trade by its ID.
Path Parameter:
trade_id: The unique ID of the trade to retrieve.

# Reasoning Behind the Approach

## Mocked Database
Since the requirement specified that we need to mock a database interaction layer, a simple approach was taken to use an in-memory Python list (trades_db) to store the trade data. This list serves as a representation of the database and provides a source of data for the API endpoints.

## Flask Framework
The Flask framework was chosen for building the API due to its simplicity, flexibility, and wide adoption in the Python community. Flask provides a lightweight and efficient way to create RESTful APIs, making it well-suited for this task.

## Pydantic Model
The Pydantic library was utilized to define the data model for trades (Trade and TradeDetails). Pydantic allows us to define the structure and validation rules for the trade data, ensuring that it conforms to a specified schema. This helps in maintaining data integrity and provides serialization/deserialization capabilities.

## Filtering and Searching
To support filtering and searching of trades, the API utilizes query parameters. The /trades endpoint accepts various query parameters (assetClass, start, end, minPrice, maxPrice, tradeType, search) to filter and search trades based on the specified criteria. These query parameters are processed in the filter_trades() function, which applies the corresponding filters to the list of trades. The search functionality is implemented by performing a case-insensitive search across multiple fields using the provided text query.

## Pagination and Sorting
The API supports pagination and sorting of trades. Pagination is achieved using the page and per_page query parameters, allowing the client to specify the desired page number and the number of trades per page. The API calculates the appropriate start and end indices to return the requested page of trades. Sorting functionality is not explicitly implemented in the provided solution, but it can be easily added by extending the filter_trades() function to sort the trades based on a specified field.
