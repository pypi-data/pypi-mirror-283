import time

from kucoin.client import Margin, Trade, Lending, Earn


def test_Trade():
    client = Trade(key='', secret='', passphrase='')
    #res=client.get_interest_rates("BTC")
    res =client.create_market_order(symbol='FRM-USDT',side='buy',clientOid=f'clientid-{time.time()*1000}',size=5)
    print(res)

def test_Lending():
    client2 = Lending(key='', secret='', passphrase='')
    res= client2.get_currency_information(currency='BTC')
    print(res)


def test_Earn():
    earn = Earn(key='668aac1303b7f800017a7c33', secret='bcb25e2a-77db-4e39-85a2-4369f78edc9c', passphrase='abc,123*')
    # res= earn.get_earn_eth_staking_products()
    # print(res)
    # res= earn.get_earn_savings_products()
    # print(res)
    # res= earn.get_earn_fixed_income_current_holdings(currency='USDT')
    # print(res)
    # res= earn.get_earn_kcs_staking_products(currency='KCS')
    # print(res)

    # res= earn.get_earn_limited_time_promotion_products(currency='ADA')
    # print(res)
    res= earn.get_earn_staking_products()
    print(res)

    # res= earn.subscribe_to_earn_fixed_income_products(productId='994',amount='10',accountType='MAIN')
    # print(res)



