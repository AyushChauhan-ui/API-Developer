from datetime import datetime
from typing import List
from flask import Flask, jsonify, request
from pydantic import BaseModel, Field

app = Flask(__name__)

trades_db = [
    {
        "trade_id": "1",
        "asset_class": "Equity",
        "counterparty": "Counterparty 1",
        "instrument_id": "TSLA",
        "instrument_name": "Tesla",
        "trade_date_time": datetime(2022, 1, 1),
        "trade_details": {
            "buySellIndicator": "BUY",
            "price": 100.0,
            "quantity": 10
        },
        "trader": "John Doe"
    },
    {
        "trade_id": "2",
        "asset_class": "FX",
        "counterparty": "Counterparty 2",
        "instrument_id": "USD",
        "instrument_name": "US Dollar",
        "trade_date_time": datetime(2022, 2, 1),
        "trade_details": {
            "buySellIndicator": "SELL",
            "price": 1.5,
            "quantity": 1000
        },
        "trader": "Jane Smith"
    },
]


class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    asset_class: str = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: str = Field(default=None, description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")
    trade_date_time: datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")


@app.route("/trades", methods=["GET"])
def get_trades():
    filtered_trades = filter_trades(request.args)
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    start = (page - 1) * per_page
    end = start + per_page
    
    paginated_trades = filtered_trades[start:end]
    
    return jsonify(paginated_trades)


@app.route("/trades/<trade_id>", methods=["GET"])
def get_trade(trade_id):
    trade = next((trade for trade in trades_db if trade["trade_id"] == trade_id), None)
    if trade:
        return jsonify(trade)
    else:
        return jsonify({"error": "Trade not found"}), 404


def filter_trades(query_params) -> List[Trade]:
    filtered_trades = trades_db

    asset_class = query_params.get("assetClass")
    if asset_class:
        filtered_trades = [trade for trade in filtered_trades if trade["asset_class"] == asset_class]
    
    start_date = query_params.get("start")
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        filtered_trades = [trade for trade in filtered_trades if trade["trade_date_time"] >= start_date]
    
    end_date = query_params.get("end")
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        filtered_trades = [trade for trade in filtered_trades if trade["trade_date_time"] <= end_date]
    
    min_price = query_params.get("minPrice")
    if min_price:
        min_price = float(min_price)
        filtered_trades = [trade for trade in filtered_trades if trade["trade_details"]["price"] >= min_price]
    
    max_price = query_params.get("maxPrice")
    if max_price:
        max_price = float(max_price)
        filtered_trades = [trade for trade in filtered_trades if trade["trade_details"]["price"] <= max_price]
    
    trade_type = query_params.get("tradeType")
    if trade_type:
        filtered_trades = [trade for trade in filtered_trades if trade["trade_details"]["buySellIndicator"] == trade_type]
    
    search_query = query_params.get("search")
    if search_query:
        search_query = search_query.lower()
        filtered_trades = [
            trade
            for trade in filtered_trades
            if (
                search_query in trade["counterparty"].lower()
                or search_query in trade["instrument_id"].lower()
                or search_query in trade["instrument_name"].lower()
                or search_query in trade["trader"].lower()
            )
        ]

    return filtered_trades


if __name__ == "__main__":
    app.run()
