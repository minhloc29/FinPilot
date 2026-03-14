# import asyncio
# from app.services.market_data_service import MarketDataService

# async def main():

#     service = MarketDataService()

#     print("\n=== Market Data Service Test ===")

#     print("\n1. Get latest quote")
#     symbol = input("Enter symbol (e.g. FPT): ")

#     quote = await service.get_quote(symbol)
#     print("\nQuote result:")
#     print(quote)

#     print("\n============================")

#     print("\n2. Get historical data")
#     start = input("Start date (YYYY-MM-DD): ")
#     end = input("End date (YYYY-MM-DD): ")

#     history = await service.get_price_history(
#         symbol,
#         start,
#         end
#     )

#     print("\nHistory result:")
#     print(history)

#     print("\n============================")

#     print("\n3. Get market indices")

#     indices = await service.get_market_indices()

#     print("\nMarket indices:")
#     print(indices)

#     print("\n============================")

#     print("\n4. Get all symbols")

#     symbols = await service.get_all_symbols()

#     print("\nFirst 20 symbols:")
#     print(symbols[:20])


# if __name__ == "__main__":
#     asyncio.run(main())

import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=1USFD83E3WZMXTQU'
r = requests.get(url)
data = r.json()

print(data)