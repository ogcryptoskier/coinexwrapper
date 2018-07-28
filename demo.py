from coinex import coinex

# add your CoinEx Access ID and Secret Key here
coinex = coinex('your-access-ID-here','your-secret-key-here')

if __name__ == "__main__":

    pair = 'CETBTC'
    merge = '0.00000001'
    limit = '5'
    transaction_id = '435013239'
    period = "1min"
    coin_type = "BCH" 
    to_address = "someaddress" 
    amount = "0.01"
    order_type = "sell"
    price = "20000"
    source_id = "this demo"
    page_num = "1"
    amt_per_page = "100"
    order_id = "1124285199"

    # print coinex.marketList()
    # print coinex.marketStats(pair)
    # print coinex.marketDepth(pair, merge, limit)
    # print coinex.marketTransactionsSince(pair, transaction_id)
    # print coinex.marketKLine(pair, type, limit)
    # print coinex.accountBalances()
    # print coinex.accountWithdrawals()
    # print coinex.withdraw(coin_type, to_address, amount)
    # print coinex.cancelWithdrawal(withdrawal_id)
    # print coinex.limitOrder(pair, order_type, amount, price, source_id)
    # print coinex.marketOrder(pair, order_type, amount)
    # print coinex.IOCOrder(pair, order_type, amount, price, source_id)
    # print coinex.pendingOrders(pair)
    # print coinex.completedOrders(pair)
    # print coinex.orderStatus(pair, order_id)
    # print coinex.orderDetails(order_id)
    # print coinex.orderDetailsByPair(pair)
    # print coinex.miningDifficulty()



