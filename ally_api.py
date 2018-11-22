import requests, json
import xml.etree.ElementTree as xml
from requests_oauthlib import OAuth1
from my_auth import my_key, my_secret, oauth_token, oauth_secret



def get_response(url, oauth1, format):
    
    def parse_pairs(pairs):
        seen_keys = dict()
        response = dict()

        for key, value in pairs:
            if key not in seen_keys:
                seen_keys[key] = 1
                response[key] = value
            else:
                seen_keys[key] += 1
                response[f'{key}_{seen_keys[key]}'] = value

        return response

    content = requests.get(url, auth=oauth1).content
    if format == 'json':
        return json.loads(content, object_pairs_hook=parse_pairs)['response']
    elif format == 'xml':
        return list(xml.fromstring(content))


def get_(what_to_get, format, oauth1):
    url = f'https://api.tradeking.com/v1{what_to_get}.{format}'
    return get_response(url, oauth1, format)


def get_profile(oauth1, format='json'):
    return get_('/member/profile', format, oauth1)


def get_watchlists(oauth1, format='json'):
    watchlists = get_('/watchlists', format, oauth1)
    if format == 'json':
        return watchlists['watchlists']
    elif format == 'xml':
        return list(watchlists[1])


def get_watchlist(id, oauth1, format='json'):
    return get_(f'/watchlists/{id}', format, oauth1)


def get_accounts(oauth1, format='json'):
    accounts = get_('/accounts', format, oauth1)
    if format == 'json':
        return accounts['accounts']
    elif format == 'xml':
        return list(list(accounts[1])[0])


def get_balances(oauth1, format='json'):
    return get_('/accounts/balances', format, oauth1)


def get_total_balance(oauth1, format='json'):
    balances = get_balances(oauth1, format)
    if format == 'json':
        return balances['totalbalance']['accountvalue']
    elif format == 'xml':
        return balances


def get_account_info(id, oauth1, format='json'):
    return get_(f'/accounts/{id}', format, oauth1)


def get_by_id(what_to_get, id, oauth1, format='json'):
    return get_(f'/accounts/{id}/{what_to_get}', format, oauth1)


def get_account_balance(id, oauth1, format='json'):
    balance = get_account_info(id, oauth1)
    if format == 'json':
        return balance['accountbalance']
    elif format == 'xml':
        return balance


def get_account_holdings(id, oauth1, format='json'):
    holdings = get_by_id('holdings', id, oauth1, format)
    if format == 'json':
        return holdings['accountholdings']
    elif format == 'xml':
        return holdings


def get_account_history(id, oauth1, format='json'):
    history = get_by_id('history', id, oauth1, format)
    if format == 'json':
        return history['transactions']['transaction']
    elif format == 'xml':
        return history


def get_account_orders(id, oauth1, format='json'):
    orders = get_by_id('orders', id, oauth1, format)
    if format == 'json':
        return orders['orderstatus']['order']
    elif format == 'xml':
        return orders


def get_stock_quotes(oauth1, symbols, format='json'):
    url = '/market/ext/quotes.json?symbols='
    if isinstance(symbols, str):
        url += symbols
    elif isinstance(symbols, list):
        symbols = [str().join([s,',']) for s in symbols]
        symbols[len(symbols) - 1] = symbols[len(symbols) - 1].strip(',')
        url = [url]
        url.extend(symbols)
        url = str().join(url)
    else:
        raise ValueError('get_quotes accepts a single symbol as a string, or a list of symbol strings')
    quotes = get_(url, format, oauth1)
    if format == 'json':
        return quotes['quotes']
    elif format == 'xml':
        return quotes


def utility(util, oauth1, format='json'):
    return get_(f'/utility/{util}', format, oauth1)


def get_api_status(oauth1, format='json'):
    return utility('status', oauth1, format)


def get_api_version(oauth1, format='json'):
    return utility('version', oauth1, format)


# gets the first account
def get_acct(oauth1):
    return get_profile(oauth1)['userdata']['account']['account']


if __name__ == '__main__':
    auth = OAuth1(my_key, my_secret, oauth_token, oauth_secret)
    acct = get_acct(auth)
    formats = ['xml', 'json']
    # testing
    def call_all(acct, formats):
        for fmt in formats:
            print(f'\n\n***************************************\ncalling: get_profie with format {fmt}')
            print(get_profile(auth, fmt))
            print(f'\n\n***************************************\ncalling: get_watchlists with format {fmt}')
            print(get_watchlists(auth, fmt))
            print(f'\n\n***************************************\ncalling: get_watchlist with format {fmt}')
            print(get_watchlist('DEFAULT', auth, fmt))
            print(f'\n\n***************************************\ncalling: get_accounts with format {fmt}')
            print(get_accounts(auth, fmt))
            print(f'\n\n***************************************\ncalling: get_balances with format {fmt}')
            print(get_balances(auth, fmt))
            print(f'\n\n***************************************\ncalling: get_total_balance with format {fmt}')
            print(get_total_balance(auth, fmt))
            print(f'\n\n***************************************\ncalling: get_account_balance with format {fmt}')
            print(get_account_balance(acct, auth, fmt))
            print(f'\n\n***************************************\ncalling: get_account_holdings with format {fmt}')
            print(get_account_holdings(acct, auth, fmt))
            print(f'\n\n***************************************\ncalling: get_account_history with format {fmt}')
            print(get_account_history(acct, auth, fmt))
            print(f'\n\n***************************************\ncalling: get_account_orders with format {fmt}')
            print(get_account_orders(acct, auth, fmt))
            print(f'\n\n***************************************\ncalling: get_stock_quotes with format {fmt}')
            if fmt == 'json':
                # TODO: fix xml issue with these
                print(get_stock_quotes(auth, 'GSPE', fmt))
                print(f'\n\n***************************************\ncalling: get_stock_quotes with format {fmt}')
                print(get_stock_quotes(auth, ['GSPE', 'AAPL'], fmt))
                print(f'\n\n***************************************\ncalling: get_api_status with format {fmt}')
            print(get_api_status(auth, fmt))
            print(f'\n\n***************************************\ncalling: get_api_version with format {fmt}')
            print(get_api_version(auth, fmt))

    call_all(acct, formats)
            