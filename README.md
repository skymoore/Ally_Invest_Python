# Ally Invest API Python Interface

# IMPORTANT:
## By using this software you release me from all responsibility resulting from it's use. I am not a financial advisor and am not offering any financial advice. I am not suggesting or implying that you buy, sell, or hold any security or investment by making this software available.

requires: requests, requests_oauthlib

`pip install requests, requests_oauthlib`

## Ally Invest API Documentation

[API Documentation](https://www.ally.com/api/invest/documentation/getting-started "Ally Invest API Documentation")

## Use this interface

1. Go [here](https://www.ally.com/api/invest/documentation/) and login, create an application and get your credentials
2. Edit my_auth.py with your credentials

`# create an oauth object`

`auth = Oauth1(my_key, my_secret, oauth_token, oauth_secret)`

`# get your data`

`acct = get_acct(auth)`