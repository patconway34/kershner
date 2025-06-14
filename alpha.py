# Editor
# Alpha   Patrick Conway   6/11/2025 4:32:14 PM   PROD
# SURFACELAPTOP   qapconway/proaus603
# Voodoo=c982d0cd-9be5-4a35-b89f-1f66b2495ec4 Sell Limit ARCA at Script Price
# Voodoo=97a91492-1033-4a96-a546-9bff6df73b08 Buy Limit ARCA at Script Price

from cloudquant.interfaces import Strategy, Event
import ktgfunc

class Gr8Script0658c52b281847fba905540262d3be47(Strategy):
    __script_name__ = 'Alpha'

    @classmethod
    def on_strategy_start(cls, md, service, account):
        cls.sell_voodooGuid = '{c982d0cd-9be5-4a35-b89f-1f66b2495ec4}'  # Sell Limit ARCA at Script Price
        cls.buy_voodooGuid = '{97a91492-1033-4a96-a546-9bff6df73b08}'  # Buy Limit ARCA at Script Price
        cls.etf_list = service.symbol_list.get_handle('82e8721e-d9fe-4ac4-b597-5197a4309a60')
        cls.yest_after = service.symbol_list.get_handle('288d5e0a-9ab2-4e52-9e10-420eaf2adc2b')
        cls.ern_before = service.symbol_list.get_handle('0774ba76-e53e-4293-9674-489e65c2581b')
        cls.reverse_split = service.symbol_list.get_handle('01d32ce7-7e62-4a57-b2fa-a6da1ac0d915')
        
    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        if (md.stat.avol > 300000
            and md.stat.prev_close > 5
            and not service.symbol_list.in_list(cls.etf_list, md.symbol)
            and not service.symbol_list.in_list(cls.yest_after, md.symbol)
            and not service.symbol_list.in_list(cls.ern_before, md.symbol)
            and not service.symbol_list.in_list(cls.reverse_split, md.symbol)):
            return True

    def on_start(self, md, order, service, account):
        service.add_time_trigger(md.market_open_time, repeat_interval = service.time_interval(0,0,1,0), timer_id = 'reset')
        service.add_time_trigger(md.market_open_time, timer_id = 'open')
        service.add_time_trigger(md.market_close_time - service.time_interval(0,35,0,0), timer_id = 'close')
        self.count = 0
        self.count2 = 0
        self.count3 = 0
        self.bid = 0
        self.ask = 0
        self.entry = False
        self.trade_data = {}
        self.trade_count = 0
        self.news = 0

    def on_timer(self, event, md, order, service, account):
        id = event.timer_id
        
        if id == 'reset':
            self.count = 0
            self.trade_count = 0
            self.count3 = 0
        if id == 'open':
            self.entry = True
        if id == 'close':
            self.entry = False
        if id == 'pending' and account[self.symbol].pending.shares_long > 0:
            order.cancel(md.symbol)
        if id == 'pending' and account[self.symbol].pending.shares_short < 0:
            order.cancel(md.symbol)
            
        if id == 'exit':
            if account[self.symbol].position.shares > 0 and account[self.symbol].pending.shares_short == 0:
                print(md.symbol, service.time_to_string(event.timestamp), "exit order sent")
                order.algo_sell( md.symbol, self.__class__.sell_voodooGuid, 'exit', price=md.L1.ask - 0.02)
            if account[self.symbol].position.shares > 0 and account[self.symbol].pending.shares_short < 0:
                self.count2 += 1
                if self.count2 >= 5:
                    print(md.symbol, service.time_to_string(event.timestamp), "cancel exit order sent")
                    order.cancel(self.symbol)
                    self.count2 = 0
            if account[self.symbol].position.shares == 0 and account[self.symbol].pending.shares_short == 0:
                service.terminate()
                print(md.symbol, service.time_to_string(event.timestamp), "terminate symbol", account[self.symbol].position.shares)
            if account[self.symbol].position.shares < 0 and account[self.symbol].pending.shares_long == 0:
                print(md.symbol, service.time_to_string(event.timestamp), "exit order sent")
                order.algo_buy( md.symbol, self.__class__.buy_voodooGuid, 'exit', price=md.L1.bid + 0.02)
            if account[self.symbol].position.shares < 0 and account[self.symbol].pending.shares_long > 0:
                self.count2 += 1
                if self.count2 >= 5:
                    print(md.symbol, service.time_to_string(event.timestamp), "cancel exit order sent")
                    order.cancel(self.symbol)
                    self.count2 = 0
            if account[self.symbol].position.shares == 0 and account[self.symbol].pending.shares_short == 0:
                service.terminate()
                print(md.symbol, service.time_to_string(event.timestamp), "terminate symbol", account[self.symbol].position.shares)
            
    def on_minute_bar(self, event, md, order, service, account, bar):
        pass

    def on_trade(self, event, md, order, service, account):
        try:
            self.trade_count += 1
            if self.bid != md.L1.bid:
                self.bid = md.L1.bid
                self.count += 1
            if self.ask != md.L1.ask:
                self.ask = md.L1.ask
                self.count3 += 1
            if (self.entry
                and self.count > 70
                and (md.L1.minute_open - md.L1.ask)/md.stat.atr > 0.1
                and md.L1.rvol > 1.2
                and self.news == 0):
                self.entry = False

                print(md.symbol, service.time_to_string(event.timestamp), self.count, md.L1.bid)

                self.trade_data['(md.L1.minute_open - md.L1.ask)/md.stat.atr'] = (md.L1.minute_open - md.L1.ask)/md.stat.atr
                self.trade_data['(md.bar.minute(-2).open[0] - md.L1.ask)/md.stat.atr'] = (md.bar.minute(-2, include_extended = True).open[0] - md.L1.ask)/md.stat.atr
                self.trade_data['(md.L1.minute_open - md.L1.bid)/md.stat.atr'] = (md.L1.minute_open - md.L1.ask)/md.stat.atr
                self.trade_data['(md.bar.minute(-2).open[0] - md.L1.bid)/md.stat.atr'] = (md.bar.minute(-2, include_extended = True).open[0] - md.L1.bid)/md.stat.atr
                self.trade_data['bid_updates'] = self.count
                self.trade_data['ask_updates'] = self.count3
                self.trade_data['bid/ask'] = self.count/(self.count3 + 0.0)
                self.trade_data['avol'] = md.stat.avol
                self.trade_data['self.trade_count'] = self.trade_count
                self.trade_data['md.L1.minute_count'] = md.L1.minute_count
                self.trade_data['self.count/md.L1.daily_count'] = self.count/(md.L1.daily_count + 0.0)
                self.trade_data['news'] = self.news

                shares = (2000 / md.L1.bid) if md.L1.bid >= 20 else 100

                order.algo_buy(md.symbol, self.__class__.buy_voodooGuid, 'init', order_quantity=shares,
                               price=(md.L1.bid * .98), allow_multiple_pending = 3, collect=self.trade_data)
                order.algo_buy(md.symbol, self.__class__.buy_voodooGuid, 'increase', order_quantity=shares,
                               price=(md.L1.bid * .96), allow_multiple_pending = 3, collect=self.trade_data)
                order.algo_buy(md.symbol, self.__class__.buy_voodooGuid, 'increase', order_quantity=shares,
                               price=(md.L1.bid * .94), allow_multiple_pending = 3, collect=self.trade_data)

                service.add_time_trigger(event.timestamp + service.time_interval(0, 20, 0, 0), repeat_interval=service.time_interval(0, 0, 1), timer_id='exit')
                service.add_time_trigger(event.timestamp + service.time_interval(0, 0, 20, 0), timer_id='pending')
            
            if (self.entry
                and self.count3 > 70
                and (md.L1.minute_open - md.L1.bid)/md.stat.atr < -0.2
                and md.L1.rvol > 1.2
                and self.news == 0):
                self.entry = False

                print(md.symbol, service.time_to_string(event.timestamp), self.count, md.L1.bid, 'Short')

                self.trade_data['(md.L1.minute_open - md.L1.ask)/md.stat.atr'] = (md.L1.minute_open - md.L1.ask)/md.stat.atr
                self.trade_data['(md.bar.minute(-2).open[0] - md.L1.ask)/md.stat.atr'] = (md.bar.minute(-2, include_extended = True).open[0] - md.L1.bid)/md.stat.atr
                self.trade_data['(md.L1.minute_open - md.L1.bid)/md.stat.atr'] = (md.L1.minute_open - md.L1.ask)/md.stat.atr
                self.trade_data['(md.bar.minute(-2).open[0] - md.L1.bid)/md.stat.atr'] = (md.bar.minute(-2, include_extended = True).open[0] - md.L1.bid)/md.stat.atr
                self.trade_data['bid_updates'] = self.count
                self.trade_data['ask_updates'] = self.count3
                self.trade_data['bid/ask'] = self.count/(self.count3 + 0.0)
                self.trade_data['avol'] = md.stat.avol
                self.trade_data['self.trade_count'] = self.trade_count
                self.trade_data['md.L1.minute_count'] = md.L1.minute_count
                self.trade_data['self.count/md.L1.daily_count'] = self.count/(md.L1.daily_count + 0.0)
                self.trade_data['news'] = self.news

                shares = (2000 / md.L1.ask) if md.L1.ask >= 20 else 100

                order.algo_sell(md.symbol, self.__class__.sell_voodooGuid, 'init', order_quantity=shares,
                               price=(md.L1.ask * 1.02), allow_multiple_pending = 3, collect=self.trade_data)
                order.algo_sell(md.symbol, self.__class__.sell_voodooGuid, 'increase', order_quantity=shares,
                               price=(md.L1.ask * 1.04), allow_multiple_pending = 3, collect=self.trade_data)
                order.algo_sell(md.symbol, self.__class__.sell_voodooGuid, 'increase', order_quantity=shares,
                               price=(md.L1.ask * 1.06), allow_multiple_pending = 3, collect=self.trade_data)

                service.add_time_trigger(event.timestamp + service.time_interval(0, 20, 0, 0), repeat_interval=service.time_interval(0, 0, 1), timer_id='exit')
                service.add_time_trigger(event.timestamp + service.time_interval(0, 0, 20, 0), timer_id='pending')
        except Exception as e: print(e, md.symbol, service.time_to_string(event.timestamp))
            
            
    def on_news(self, event, md, order, service, account):
        self.news += 1
