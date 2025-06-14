# Editor
# Eclipse   Patrick Conway   6/13/2025 8:52:29 AM   PROD
# SURFACELAPTOP   qapconway/proaus603
# Voodoo=97a91492-1033-4a96-a546-9bff6df73b08 Buy Limit ARCA at Script Price
# Voodoo=c982d0cd-9be5-4a35-b89f-1f66b2495ec4 Sell Limit ARCA at Script Price

from cloudquant.interfaces import Strategy, Event
import ktgfunc
import math

class Gr8Script25ac3723c613429e98a56039fe1a3227(Strategy):
    __script_name__ = 'Eclipse'

    @classmethod
    def is_symbol_qualified(cls, symbol, md, service, account):
        bars_d = md.bar.daily(-2)
        exclude_list = ['TVIX','LSXMA','LSXMB','LSXMK','LBRDA','LBRDB','LBRDK','BATRA','BATRB',
                        'BATRK','FWONA','FWONB','FWONK', 'LTRPA', 'LTRPB', 'LMCA', 'LMCB', 'LMCK',
                        'LBTYA', 'LBTYB', 'LBTYK', 'LILA', 'LILAK']
        if (md.stat.avol > 400000
            and len(bars_d.close) == 2 
            and (md.stat.avol*md.stat.prev_close) >= 5000000            
            and symbol not in exclude_list
            and 1050 >= md.stat.prev_close >= 3
            and not service.symbol_list.in_list(service.symbol_list.get_handle('82e8721e-d9fe-4ac4-b597-5197a4309a60'), md.symbol)
            and not service.symbol_list.in_list(service.symbol_list.get_handle('288d5e0a-9ab2-4e52-9e10-420eaf2adc2b'), md.symbol) 
            and not service.symbol_list.in_list(service.symbol_list.get_handle('0774ba76-e53e-4293-9674-489e65c2581b'), md.symbol)
            and not service.symbol_list.in_list(service.symbol_list.get_handle('01d32ce7-7e62-4a57-b2fa-a6da1ac0d915'), md.symbol)):
            return True
        else:
            return False
        
    @classmethod
    def backtesting_extra_symbols(cls, symbol, md, service, account):
        return symbol in ['SPY', 'VXX']
    
    def on_timer(self, event, md, order, service, account):
        if event.timer_id == 'covert' and account[self.symbol].position.shares > 0:
            order.algo_sell(md.symbol, self.sell_voodooGuid, 'exit', price = (md.L1.bid - .02))
        if event.timer_id == 'pending' and account[self.symbol].pending.shares_long > 0:
            order.cancel(self.symbol)
        if event.timer_id == 'cancel_covert' and account[self.symbol].position.shares > 0:
            order.cancel(self.symbol)
        if event.timer_id == 'exit' and account[self.symbol].position.shares > 0 and account[self.symbol].pending.shares_short == 0:
            order.algo_sell(md.symbol, self.sell_voodooGuid, 'exit', price=(md.L1.bid - 0.02))           
        if event.timer_id == 'stop' and account[self.symbol].position.shares > 0:
            self.low = md.L1.daily_low
            service.add_time_trigger(event.timestamp, repeat_interval = service.time_interval(0,0,2), timer_id = 'new_lows')
        if event.timer_id == 'new_lows' and md.L1.bid < self.low and account[self.symbol].position.shares > 0 :
            service.add_time_trigger(event.timestamp, repeat_interval = service.time_interval(0,0,2), timer_id = 'exit')
        if event.timer_id == 'start':
            self.start = True
            self.spypre = md["SPY"].L1.acc_volume
            self.spyavol = md["SPY"].stat.avol
            self.mktstart = event.timestamp            
        if event.timer_id == 'end':
            self.start = False
            
    def on_start(self, md, order, service, account):
        self.orderPrice = 0
        self.trade_data = {}
        self.buy_voodooGuid = '{97a91492-1033-4a96-a546-9bff6df73b08}' # Buy Limit ARCA at Script Price
        self.sell_voodooGuid = '{c982d0cd-9be5-4a35-b89f-1f66b2495ec4}' # Sell Limit ARCA at Script Price
        service.add_time_trigger(md.market_open_time, timer_id = 'start')
        service.add_time_trigger(md.market_open_time + service.time_interval(minutes = 20), timer_id = 'end')
        self.start = 0
        self.low = 0
        
        
        self.news_count = 0
        self.hasOrder = 0
        self.actualOrderTime = 0
        self.exitTime = 0
        self.low2min = 999
        self.time = 0
        self.cancelOrder = 0
        self.s_time = 0
        self.shares = 100
        self.cancelExit = 0
        self.order_id = 0
        self.fill = 0
        self.dailyDnRatio = 0.0
        self.dailyMax = 0.0
        self.pointsTotal = 0
        self.tailPct = -100
        self.firstMin = 0
        self.same = 0
        self.ATRPrice = 0
        self.mktstart = 0.0
        self.seconds = -9999
        self.mseconds = -9999
        self.maxmin = 99999
        
        ### ATR
        var =[]
        tr = []
        self.atr = 0
        
        x = md.bar.daily(start = -21, end = -1)
        y = md.bar.daily(start = -22, end = -2)
        high = x.high
        low = x.low
        close = x.close
        prev_close = y.close
        i = 0        
        if len(x.high) == 20 and len(y.high) == 20:
            while i < len(x.high):
                var.append(high[i] - low[i])
                var.append(abs(high[i]-prev_close[i]))
                var.append(abs(low[i]-prev_close[i]))
                tr.append(max(var))
                var = []
                i += 1
            z = tr[:13]
            self.atr = sum(tr, 0.0) / len(tr)
            h = tr[13:]
            q = 0
            while q < len(h):
                self.atr = ((self.atr * 13) + h[q])/14
                q += 1
        
        #Minute Moves over the past 3 days
        x = sorted(md.bar.minute(start=-1438,end = -1, today_only=False).spread)
        if len(x) >= 100:
            self.maxmin =sum(x[-2:])/2          

    def on_trade(self, event, md, order, service, account):
        try:
            # On_trade Variables   
            ask = md.L1.ask
            m_open = md.L1.minute_open
            prev_close = md.stat.prev_close
            bid = md.L1.bid
            last = md.L1.last
            # atr = md.stat.atr
            s_open = md.L1.open
            self.mseconds = ((event.timestamp - md.L1.minute_start_timestamp) / 1000000) + 1
            self.seconds = ((event.timestamp - self.mktstart) / 1000000) + 1
            self.pointsTotal = 0

            # Entry Conditions
            if (self.start
                and self.atr != 0
                and prev_close != 0
                and (m_open-ask)/self.atr >= .25
                and (m_open - ask) >= .35
                and ask <= (prev_close - .4)
                and (prev_close - ask) / ask >= .025
                and s_open - ask >= .2
                and ask/md.bar.daily(-5).close[0] - 1 < 3
                and (m_open - ask)/ask > .01
                and 3 < ask <= 100
                and md.L1.rvol > 1.0
                and md['SPY'].L1.gap < -.54):

                points = 0
                if md.stat.avol >= 5000000:
                    points = 10
                self.pointsTotal += points

                points = 0
                if self.spyavol/self.spypre > 3:
                    points = 21
                if self.spyavol/self.spypre > 12:
                    points = 3
                if self.spyavol/self.spypre > 37 :
                    points = -2
                if self.spyavol/self.spypre > 66 :
                    points =    -6
                self.pointsTotal += points    

                points = 0
                if (m_open - ask) / self.mseconds >= 0.05:
                    points = 23
                self.pointsTotal += points

                points = 0
                if self.maxmin > 0.014:
                    points = 5
                if self.maxmin > 0.16:
                    points = 1.2
                if self.maxmin > 0.46:
                    points = -2.3
                if self.maxmin > 0.9:
                    points = -6
                self.pointsTotal += points    

                points = 0
                if (m_open - ask) / self.atr >= 0.70:
                    points += 5
                self.pointsTotal += points

                points = 0
                if  ask-last >= 0.07:
                    points = -5            
                if  ask-last >= 0.2:
                    points = -24
                self.pointsTotal += points

                points = 0
                if  ask-bid <= 0:
                    points = 12               
                if  ask-bid >= .12:
                    points = -5            
                self.pointsTotal += points

            # Collect Data and Entry (Buy Limit Arca)      
            if (self.pointsTotal >= 4.7
                and self.news_count == 0):
                self.start = False

                orderShares = 100
                self.orderPrice = md.L1.ask + 0.02
                if self.orderPrice >= 50:
                    orderShares=int(5000/self.orderPrice)                        
                self.order_id = order.algo_buy( md.symbol, self.buy_voodooGuid, 'init', order_quantity=orderShares, price=self.orderPrice, collect=self.trade_data )        
                service.add_time_trigger(event.timestamp + service.time_interval(0, 29, 55, 0), timer_id = 'cancel_covert')
                service.add_time_trigger(event.timestamp + service.time_interval(0, 30, 0, 0), timer_id = 'exit')
                service.add_time_trigger(event.timestamp + service.time_interval(0, 15, 0, 0), timer_id = 'covert')

                service.add_time_trigger(event.timestamp + service.time_interval(0, 4, 0, 0), timer_id = 'stop')
                service.add_time_trigger(event.timestamp + service.time_interval(0,0,20,0), timer_id = 'pending')
        except Exception as e: print(e)
