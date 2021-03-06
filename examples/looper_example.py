from ctpbee.looper import LooperApi, Vessel
from ctpbee.qa_support import QADataSupport

from ctpbee.indicator.ta_lib import ArrayManager



class DoubleMa(LooperApi):
    def __init__(self, name):
        super(DoubleMa, self).__init__(name)
        # self.manager = ArrayManager()
        self.instrument_set = ["rb2010.SHFE", "ag2010.SHFE"]
        self.fast_window = 10
        self.slow_window = 20
        self.pos = 0
        self.open = False

    def on_bar(self, bar):
        print(bar.local_symbol, bar.datetime)
        # self.manager.update_bar(bar)
        # if not self.manager.inited:
        #     return
        # # print(self.position_manager.get_all_positions())
        # # print(bar.close_price)
        # fast_ma = self.manager.sma(self.fast_window, array=True)
        # self.fast_ma0 = fast_ma[-1]
        # self.fast_ma1 = fast_ma[-2]
        #
        # slow_ma = self.manager.sma(self.slow_window, array=True)
        # self.slow_ma0 = slow_ma[-1]
        # self.slow_ma1 = slow_ma[-2]
        #
        # cross_over = self.fast_ma0 > self.slow_ma0 and self.fast_ma1 < self.slow_ma1
        # cross_below = self.fast_ma0 < self.slow_ma0 and self.fast_ma1 > self.slow_ma1
        #
        # if cross_over and not self.open:
        #     self.action.buy(bar.close_price, 1, bar)
        #     self.open = True
        # elif cross_below and self.open:
        #     self.action.cover(bar.close_price, 1, bar)
        #     self.open = False
        # elif cross_below:
        #     if self.pos == 0:
        #         self.action.short(bar.close_price, 1, bar)
        #     elif self.pos > 0:
        #         self.action.sell(bar.close_price, 1, bar)
        #         self.action.short(bar.close_price, 1, bar)

    def on_tick(self, tick):
        pass


if __name__ == '__main__':
    data_support = QADataSupport(host="quantaxis.tech", port=27027)
    runnning = Vessel()
    strategy = DoubleMa("ma")
    data = data_support.get_future_min("rb2010.SHFE", frq="1min", start="2019-08-01", end="2020-07-15")
    ag_data = data_support.get_future_min("ag2010.SHFE", frq="1min", start="2019-08-01", end="2020-07-15")
    print(data)
    runnning.add_data(data, ag_data)
    params = {
        "looper":
            {
                "initial_capital": 100000,
                "commission": 0.005,
                "deal_pattern": "price",
                "size_map": {"rb2010.SHFE": 10},
                "today_commission": 0.005,
                "yesterday_commission": 0.02,
                "close_commission": 0.005,
                "slippage_sell": 0,
                "slippage_cover": 0,
                "slippage_buy": 0,
                "slippage_short": 0,
                "close_pattern": "yesterday",
            },
        "strategy":
            {
            }
    }
    runnning.add_strategy(strategy)
    runnning.params = params
    runnning.run()
    result = runnning.get_result(report=True)
