


def blEmpty(api:any):
    position = api.get_position()
    #print("----------------position---------------")
    #print(position)

    print("----------------1 检测当前仓位信息------------------------------------------------------")
    for n,p in position.items():
        #print("name=",n,"p=",p)
        print("品种:",n,"浮盈：",p.float_profit_long + p.float_profit_short,"   多仓:",p.pos_long,"空仓:",p.pos_short)
        quote = api.get_quote(n)
        #print(quote)
        print("合约代码：",quote.instrument_id,"卖1:",quote.ask_price1,"买1:",quote.bid_price1)
        
        print("开始平仓：",quote.instrument_id,"------------------------------------------------")

        if p.pos_long>0:
            print("需要平仓多仓",p.pos_long,"手")
            order = api.insert_order(symbol=quote.instrument_id, direction="SELL", offset="CLOSETODAY", limit_price=quote.bid_price1-2,
                volume=p.pos_long)

            while order.status != "FINISHED":
                api.wait_update()
                print("合约代码：",quote.instrument_id,"已平仓")


        if p.pos_short>0:
            print("需要平仓空仓",p.pos_short,"手")
            order = api.insert_order(symbol=quote.instrument_id, direction="BUY", offset="CLOSETODAY", limit_price=quote.ask_price1+2,
                volume=p.pos_short)

            while order.status != "FINISHED":
                api.wait_update()
                print("合约代码：",quote.instrument_id,"已平仓")