#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import hashlib
import json
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)
http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=1, read=2))

class coinex(object):
    __headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }

    def __init__(self, access_id, secret_key, headers={}):
        self.access_id = access_id
        self.secret_key = secret_key
        self.baseUrl = 'https://api.coinex.com'
        self.version = '/v1'
        self.headers = self.__headers
        self.headers.update(headers)

    @staticmethod
    def createToken(params, secret_key):
        sort_params = sorted(params)
        data = []
        for item in sort_params:
            data.append(item + '=' + str(params[item]))
        str_params = "{0}&secret_key={1}".format('&'.join(data), secret_key)
        token = hashlib.md5(str_params).hexdigest().upper()
        return token

    def authorize(self, params):
        params['access_id'] = self.access_id
        params['tonce'] = int(time.time()*1000)
        self.headers['AUTHORIZATION'] = self.createToken(params, self.secret_key)

    def request(self, req_auth, method, endpoint, params={}, data='', json_object={}):
        method = method.upper()
        url = self.baseUrl + self.version + endpoint
        if method in ['GET', 'DELETE']:
            if req_auth == True:
                self.authorize(params)
            response = http.request(method, url, fields=params, headers=self.headers)
        else:
            if data:
                json_object.update(json.loads(data))
            if req_auth == True:
                self.authorize(json_object)
            encoded_data = json.dumps(json_object).encode('utf-8')
            response = http.request(method, url, body=encoded_data, headers=self.headers)
        return response

    # Return a list of all available trading pairs.
    def marketList(self):
        endpoint = '/market/list'   
        response = self.request(False, 'GET', endpoint).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)    

    # Return real-time market statistics for a single trading pair (e.g. "BTCBCH").
    def marketStats(self, pair):
        endpoint = '/market/ticker'
        params = {'market':pair}        
        response = self.request(False, 'GET', endpoint, params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)

    # Return the current order depth for a single trading pair. 
    # Limit is an optional range of 5, 10, or 20.
    def marketDepth(self, pair, merge, limit=""):
        endpoint = '/market/depth'
        params =    {'market':pair,
                    'merge':merge,
                    'limit':limit}
        response = self.request(False, 'GET', endpoint, params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)

    # Return transaction history of up to 1000 transactions since a particular transaction_id.
    # Will only return transaction history for the latest 1000 transaction ids.
    def marketTransactionsSince(self, pair, transaction_id=""):
        endpoint = '/market/deals'
        params =    {'market':pair,
                    'last_id':transaction_id}
        response = self.request(False, 'GET', endpoint, params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)

    # Return up to 1000 K-Line data points of a given type for a particular trading pair.
    def marketKLine(self, pair, period, limit=""):
        endpoint = '/market/kline'
        params =    {'market':pair,
                    'limit':limit,
                    'type':period}
        response = self.request(False, 'GET', endpoint, params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)

    # Return all of the currency balances for the account.
    def accountBalances(self):
        endpoint = '/balance'
        response = self.request(True, 'GET', endpoint).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)   
    
    # Return withdrawal information for a specific coin type or withdrawal ID.
    def accountWithdrawals(self, coin_type="", withdrawal_id="", page_num="", amt_per_page=""):
        endpoint = '/balance/coin/withdraw'
        params =    {'coin_type':coin_type,
                    'coin_withdraw_id':withdrawal_id,
                    'page':page_num,
                    'Limit':amt_per_page}
        response = self.request(True, 'GET', endpoint, params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)   

    # Submit a withdrawal order
    def withdraw(self, coin_type, to_address, amount):
        endpoint = '/balance/coin/withdraw'
        params =    {'coin_type':coin_type,
                    'coin_address':to_address,
                    'actual_amount':amount}
        response = self.request(True, 'POST', endpoint, json_object=params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)   

    # Cancel a withdrawal order
    def cancelWithdrawal(self, withdrawal_id):
        endpoint = '/balance/coin/withdraw'
        params = {'coin_withdraw_id':withdrawal_id}
        response = self.request(True, 'DELETE', endpoint, params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)   
    
    # Place a limit order 
    def limitOrder(self, pair, order_type, amount, price, source_id=""):
        endpoint = '/order/limit'
        params =    {'market':pair,
                    'type':order_type,
                    'amount':amount,
                    'price':price,
                    'source_id':source_id}
        response = self.request(True, 'POST', endpoint, json_object=params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)  
    
    # Place a market order
    def marketOrder(self, pair, order_type, amount):
        endpoint = '/order/market'
        params =    {'market':pair,
                    'type':order_type,
                    'amount':amount}
        response = self.request(True, 'POST', endpoint, json_object=params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)  

    # Place an immediate-or-cancel order
    def IOCOrder(self, pair, order_type, amount, price, source_id=""):
        endpoint = '/order/ioc'
        params =    {'market':pair,
                    'type':order_type,
                    'amount':amount,
                    'price':price,
                    'source_id':source_id}
        response = self.request(True, 'POST', endpoint, json_object=params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)  
    
    # Get a list of pending orders
    def pendingOrders(self, pair, page_num="1", amt_per_page="50"):
        endpoint = '/order/pending'
        params =    {'market':pair,
                    'page':page_num,
                    'limit':amt_per_page}
        response = self.request(True, 'GET', endpoint, params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)   

    # Get a list of completed orders
    def completedOrders(self, pair, page_num="1", amt_per_page="100"):
        endpoint = '/order/finished'
        params =    {'market':pair,
                    'page':page_num,
                    'limit':amt_per_page}
        response = self.request(True, 'GET', endpoint, params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)   

    # Get the status of an order
    def orderStatus(self, pair, order_id):
        endpoint = '/order/status'
        params =    {'market':pair,
                    'id':order_id}
        response = self.request(True, 'GET', endpoint, params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)   
    
    # Get the details of an executed order
    def orderDetails(self, order_id, page_num="1", amt_per_page="100"):
        endpoint = '/order/deals'
        params =    {'id':order_id,
                    'page':page_num,
                    'limit':amt_per_page}
        response = self.request(True, 'GET', endpoint, params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)   

    # Get all order details for a given traiding pair
    def orderDetailsByPair(self, pair, page_num="1", amt_per_page="100"):
        endpoint = '/order/user/deals'
        params =    {'market':pair,
                    'page':page_num,
                    'limit':amt_per_page}
        response = self.request(True, 'GET', endpoint, params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)   

    # Cancel an order
    def cancelOrder(self, order_id, pair):
        endpoint = '/order/pending'
        params =    {'id':order_id,
                    'market':pair}
        response = self.request(True, 'DELETE', endpoint, params).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)   
    
    # Get the current mining difficulty
    def miningDifficulty(self):
        endpoint = '/order/mining/difficulty'
        response = self.request(True, 'GET', endpoint).data
        parsed = json.loads(response)
        return json.dumps(parsed, indent=4, sort_keys=True)   