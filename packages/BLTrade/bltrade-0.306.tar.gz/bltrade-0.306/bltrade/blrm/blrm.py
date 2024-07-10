from tqsdk import TqAccount, TqApi, TqAuth,TqSim

import datetime
import blrmcore

#api = TqApi(TqAccount("C创元期货", "13000252", "jwz20230301"), auth=TqAuth("billin", "dnadna"))

api = TqApi(TqSim(), auth=TqAuth('billin', 'dnadna'))



account = api.get_account()
print(account.balance)
print(account.float_profit)

#position = api.get_position("SHFE.ag2408")
position = api.get_position()
print("----------------position---------------")
print(position)

# 一键平仓
#blrmcore.blEmpty(api)


"""
quote1 = api.get_quote("SHFE.ag2408")

order1 = api.insert_order(symbol="SHFE.ag2408", direction="BUY", offset="OPEN", limit_price=quote1.ask_price1, volume=2)
while order1.status != "FINISHED":
    api.wait_update()
    print("order1 opend")

quote2 = api.get_quote("SHFE.ru2409")
order2 = api.insert_order(symbol="SHFE.ru2409", direction="BUY", offset="OPEN", limit_price=quote2.ask_price1, volume=2)
while order2.status != "FINISHED":
    api.wait_update()
    print("order2 opend")

"""




position = api.get_position()
print("----------------position---------------")
print(position)


# 监控程序主循环
# 这里依赖一个前面活跃的quote来触发每次循环
while api.wait_update():
    print("----------------kv------------------------------------------------------")
    for n,p in position.items():
        #print("name=",n,"p=",p)
        print("品种:",n,"浮盈：",p.float_profit_long,"   多仓:",p.pos_long,"空仓:",p.pos_short,)
        #print("品种:",n,"浮盈：",p.float_profit_long + p.float_profit_short,"   多仓:",p.pos_long,"空仓:",p.pos_short,)
        quote = api.get_quote(n)
        #print(quote)
        print("合约代码：",quote.instrument_id,"卖1:",quote.ask_price1,"买1:",quote.bid_price1)

    print("账户资金：",account.balance,"账户浮盈:",account.float_profit)



"""
order = api.insert_order(symbol="SHFE.ag2408", direction="SELL", offset="CLOSETODAY", limit_price=quote.bid_price1,
                         volume=2)

while order.status != "FINISHED":
    api.wait_update()
print("closed")
"""
api.close()
