import schwabdev
from datetime import datetime, timedelta
from dotenv import load_dotenv
from time import sleep
import os


def main():
    # place your app key and app secret in the .env file
    load_dotenv()  # load environment variables from .env file

    # create client
    client = schwabdev.Client(os.getenv('app_key'), os.getenv('app_secret'), os.getenv('callback_url'), verbose=True)

    print("\n\nAccounts and Trading - Accounts.")

    # get account number and hashes for linked accounts
    print("|\n|client.account_linked().json()", end="\n|")
    linked_accounts = client.account_linked().json()
    print(linked_accounts)
    # this will get the first linked account
    account_hash = linked_accounts[0].get('hashValue')
    sleep(3)

    # get positions for linked accounts
    print("|\n|client.account_details_all().json()", end="\n|")
    print(client.account_details_all().json())
    sleep(3)

    # get specific account positions (uses default account, can be changed)
    print("|\n|client.account_details(account_hash, fields='positions').json()", end="\n|")
    print(client.account_details(account_hash, fields="positions").json())
    sleep(3)

    print("\n\nAccounts and Trading - Orders.")

    # get orders for a linked account
    print("|\n|client.account_orders(account_hash, datetime.utcnow() - timedelta(days=30), datetime.utcnow()).json()",end="\n|")
    print(client.account_orders(account_hash, datetime.utcnow() - timedelta(days=30), datetime.utcnow()).json())
    sleep(3)

    # place an order, get the details, then cancel it (uncomment to test)
    """
    order = {"orderType": "LIMIT", "session": "NORMAL", "duration": "DAY", "orderStrategyType": "SINGLE", "price": '10.00',
         "orderLegCollection": [
             {"instruction": "BUY", "quantity": 1, "instrument": {"symbol": "INTC", "assetType": "EQUITY"}}]}
    resp = client.order_place(account_hash, order)
    print("|\n|client.order_place(account_hash, order).json()", end="\n|")
    print(f"Response code: {resp}") 
    # get the order ID - if order is immediately filled then the id might not be returned
    order_id = resp.headers.get('location', '/').split('/')[-1] 
    print(f"Order id: {order_id}")
    sleep(3)

    # get specific order details
    print("|\n|client.order_details(account_hash, order_id).json()", end="\n|")
    print(client.order_details(account_hash, order_id).json())
    sleep(3)

    # cancel specific order
    print("|\n|client.order_cancel(account_hash, order_id).json()", end="\n|")
    print(client.order_cancel(account_hash, order_id))
    sleep(3)
    """

    # replace specific order (no demo implemented)
    # print("|\n|client.order_replace(account_hash, order_id, order)")
    # client.order_replace(account_hash, order_id, order)

    # get up to 3000 orders for all accounts for the past 30 days
    print(
        "|\n|client.account_orders_all(datetime.utcnow() - timedelta(days=30), datetime.utcnow()).json()",
        end="\n|")
    print(client.account_orders_all(datetime.utcnow() - timedelta(days=30), datetime.utcnow()).json())
    sleep(3)

    # preview order (not implemented by Schwab yet)
    # print("|\n|client.order_preview(account_hash, orderObject)")
    # client.order_preview(account_hash, orderObject)

    print("\n\nAccounts and Trading - Transactions.")

    # get all transactions for an account
    print(
        "|\n|client.transactions(account_hash, datetime.utcnow() - timedelta(days=30), datetime.utcnow(), \"TRADE\").json()",
        end="\n|")
    print(client.transactions(account_hash, datetime.utcnow() - timedelta(days=30), datetime.utcnow(),"TRADE").json())
    sleep(3)

    # get details for a specific transaction (no demo implemented)
    # print("|\n|client.transaction_details(account_hash, transactionId).json()", end="\n|")
    # print(client.transaction_details(account_hash, transactionId).json())

    print("\n\nAccounts and Trading - UserPreference.")

    # get user preferences for an account
    print("|\n|client.preferences().json()", end="\n|")
    print(client.preferences().json())
    sleep(3)

    print("\n\nMarket Data - Quotes.")

    # get a list of quotes
    print("|\n|client.quotes([\"AAPL\",\"AMD\"]).json()", end="\n|")
    print(client.quotes(["AAPL", "AMD"]).json())
    sleep(3)

    # get a single quote
    print("|\n|client.quote(\"INTC\").json()", end="\n|")
    print(client.quote("INTC").json())
    sleep(3)

    print("\n\nMarket Data - Options Chains.")
    print("|\n|There is a lot to print so this is not shown, the demo code is commented out")
    # get an option chain
    # print("|\n|client.option_chains(\"AAPL\").json()", end="\n|")
    # print(client.option_chains("AAPL").json())
    sleep(3)

    print("\n\nMarket Data - Options Expiration Chain.")

    # get an option expiration chain
    print("|\n|client.option_expiration_chain(\"AAPL\").json()", end="\n|")
    print(client.option_expiration_chain("AAPL").json())
    sleep(3)

    print("\n\nMarket Data - PriceHistory.")
    # get price history for a symbol
    print("|\n|client.price_history(\"AAPL\", \"year\").json()", end="\n|")
    print(client.price_history("AAPL", "year").json())
    sleep(3)

    print("\n\nMarket Data - Movers.")

    # get movers for an index
    print("|\n|client.movers(\"$DJI\").json()", end="\n|")
    print(client.movers("$DJI").json())
    sleep(3)

    print("\n\nMarket Data - MarketHours.")

    # get marketHours for a symbol
    print("|\n|client.market_hours([\"equity\",\"option\"]).json()", end="\n|")
    print(client.market_hours(["equity", "option"]).json())
    # print(client.market_hours("equity,option").json()) # also works
    sleep(3)

    # get marketHours for a market
    print("|\n|client.market_hour(\"equity\").json()", end="\n|")
    print(client.market_hour("equity").json())
    sleep(3)

    print("\n\nMarket Data - Instruments.")

    # get instruments for a symbol
    print("|\n|client.instruments(\"AAPL\", \"fundamental\").json()", end="\n|")
    print(client.instruments("AAPL", "fundamental").json())
    sleep(3)

    # get instruments for a cusip
    print("|\n|client.instrument_cusip(\"037833100\").json()", end="\n|")
    print(client.instrument_cusip("037833100").json())  # 037833100 = AAPL
    sleep(3)



if __name__ == '__main__':
    print("Welcome to the unofficial Schwab interface!\nGithub: https://github.com/tylerebowers/Schwab-API-Python")
    main()  # call the user code above