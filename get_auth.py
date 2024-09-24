import schwabdev
from datetime import datetime, timedelta
from dotenv import load_dotenv
from time import sleep
import os


def main():
    # place your app key and app secret in the .env file
    load_dotenv()  # load environment variables from .env file

    # create client
    client = schwabdev.Client(os.getenv('app_key'), os.getenv('app_secret'), os.getenv('callback_url'), tokens_file="./tmp/tokens.json"verbose=True)

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

    print("\n\nAccounts and Trading - Transactions.")

    # get all transactions for an account
    print(
        "|\n|client.transactions(account_hash, datetime.utcnow() - timedelta(days=30), datetime.utcnow(), \"TRADE\").json()",
        end="\n|")
    print(client.transactions(account_hash, datetime.utcnow() - timedelta(days=30), datetime.utcnow(),"TRADE").json())
    sleep(3)

if __name__ == '__main__':
    print("Welcome to the unofficial Schwab interface!\nGithub: https://github.com/tylerebowers/Schwab-API-Python")
    main()  # call the user code above