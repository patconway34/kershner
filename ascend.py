# Editor
# Ascend   Patrick Conway   6/13/2025 2:33:02 PM   PROD
# SURFACELAPTOP   qapconway/proaus603
# Voodoo=97a91492-1033-4a96-a546-9bff6df73b08 Buy Limit ARCA at Script Price
# Voodoo=c982d0cd-9be5-4a35-b89f-1f66b2495ec4 Sell Limit ARCA at Script Price

from cloudquant.interfaces import Strategy, Event
import ktgfunc

class Gr8Script9c2a8cabec81482c9e93a089f03c811e(Strategy):
    __script_name__ = 'Ascend'

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        if (md.stat.avol >= 100000
            and not service.symbol_list.in_list(service.symbol_list.get_handle('82e8721e-d9fe-4ac4-b597-5197a4309a60'), md.symbol)
            and 'TVIX' not in md.symbol
            and md.stat.prev_close <= 20):
            return True
        else:
            return False

    # called at the beginning of each instance
    def on_start(self, md, order, service, account):
        self.buy_voodooGuid = '{97a91492-1033-4a96-a546-9bff6df73b08}' # Buy Limit ARCA at Script Price
        self.sell_voodooGuid = '{c982d0cd-9be5-4a35-b89f-1f66b2495ec4}' # Sell Limit ARCA at Script Price
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes = 1), timer_id = 'open')
        service.add_time_trigger(md.market_close_time - service.time_interval(minutes = 40), timer_id = 'close')
        self.entry = False
        self.trade_data = {}
        self.ex_trade_data = {}
        self.below_minute = 0
        self.trade_condition = 0
        self.profits = False
        self.ex_profits = 0
        self.bid = 0
        self.min_open = 0

    # called in timer event is received
    def on_timer(self, event, md, order, service, account):
        if event.timer_id == 'exit' and account[self.symbol].position.shares > 0 and account[self.symbol].pending.shares_short < 0:
            order.cancel(self.symbol)
        if event.timer_id == 'exit' and not md.L1.is_halted and account[self.symbol].position.shares > 0 and account[self.symbol].pending.shares_short == 0:
            self.ex_profits = 3
            self.ex_trade_data['Profits'] = self.ex_profits
            order.algo_sell(md.symbol, self.sell_voodooGuid, 'exit', price=(md.L1.bid - 0.02), collect=self.ex_trade_data)
        if event.timer_id == 'pending' and account[self.symbol].pending.shares_long > 0:
            order.cancel(self.symbol)

        if (event.timer_id == 'profits' 
            and account[self.symbol].position.shares > 0 
            and account[self.symbol].pending.shares_long == 0 
            and account[self.symbol].pending.shares_short == 0
            and md.L1.last < (self.bid + (self.min_open - self.bid) * .6667)): 
            self.profits = False
            order.algo_sell(md.symbol, self.sell_voodooGuid, 'exit', price=(md.L1.bid + ((self.min_open - md.L1.bid) * .6667)), collect=self.ex_trade_data) 

        if (event.timer_id == 'profits'
            and account[self.symbol].position.shares > 0 
            and account[self.symbol].pending.shares_long == 0
            and account[self.symbol].pending.shares_short == 0
            and md.L1.last >= (self.bid + (self.min_open - self.bid) * .6667)):
            self.profits = False
            order.algo_sell(md.symbol, self.sell_voodooGuid, 'exit', price=(md.L1.last), collect=self.ex_trade_data)

        if event.timer_id == 'open':
            self.entry = True
        if event.timer_id == 'close':
            self.entry = False
        
    def on_trade(self, event, md, order, service, account):
        try:
            if '5' in md.L1.trade_condition:
                self.entry = False
            
            if (self.entry
                and (md.L1.minute_open/md.L1.bid - 1) >= .04
                and md.L1.minute_open - md.L1.bid > .08
                and md.L1.ask - md.L1.bid < .03
                and md.L1.rvol > 0.8
                and  .3 <= md.L1.bid <= 5
                and md.L1.bid <= md.stat.prev_close
                and account[self.symbol].position.shares == 0
                and account[self.symbol].pending.shares_long == 0
                and account[self.symbol].pending.shares_short == 0):
                self.entry = False          

                self.bid = md.L1.bid
                self.min_open = md.bar.minute(-1, include_extended = True).open[-1]
                
                order.algo_buy( md.symbol, self.buy_voodooGuid, 'init', order_quantity=100, price = (md.L1.bid - 0.02), collect=self.trade_data, allow_multiple_pending = 8 )
                order.algo_buy( md.symbol, self.buy_voodooGuid, 'increase', order_quantity=100, price = (md.L1.bid * .95), collect=self.trade_data, allow_multiple_pending = 8)
                order.algo_buy( md.symbol, self.buy_voodooGuid, 'increase', order_quantity=100, price = (md.L1.bid * .90), collect=self.trade_data, allow_multiple_pending = 8)
                order.algo_buy( md.symbol, self.buy_voodooGuid, 'increase', order_quantity=100, price = (md.L1.bid * .85), collect=self.trade_data, allow_multiple_pending = 8)
                order.algo_buy( md.symbol, self.buy_voodooGuid, 'increase', order_quantity=100, price = (md.L1.bid * .80), collect=self.trade_data, allow_multiple_pending = 8)
                order.algo_buy( md.symbol, self.buy_voodooGuid, 'increase', order_quantity=100, price = (md.L1.bid * .75), collect=self.trade_data, allow_multiple_pending = 8)

                service.add_time_trigger(event.timestamp + service.time_interval(minutes=20),repeat_interval = service.time_interval(0,0,15), timer_id = 'exit')
                service.add_time_trigger(event.timestamp + service.time_interval(minutes = 3), timer_id = 'pending')
                service.add_time_trigger(event.timestamp + service.time_interval(minutes = 3, seconds = 2), timer_id = 'profits')
                
                _alertList = [('Model', "Ascend")]
                service.alert( md.symbol, '96877154-c925-49fa-9537-ac6d29e0c0f6', _alertList, 3 )
                
        except Exception as e: print(e)
