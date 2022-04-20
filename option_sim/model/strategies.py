import numpy as np

class Strategy: 
    """ """
    def __init__(self, *legs):
        if len(legs) == 1: self.legs = legs[0]
        else: self.legs = legs

    @staticmethod
    def payoff(qty, strike, derivative_price):
        underlying_price_range = np.linspace(strike * 0.8, strike * 1.2, 41)
        payoff = np.maximum(
                            underlying_price_range - strike, 
                            - np.ones_like(underlying_price_range) * derivative_price
                            )
        return np.stack((underlying_price_range, payoff * qty), axis=1)
            


    def strategy_payoff(self):
        strategy_payoff = np.zeros(41)
        for leg in self.legs:
            np.add(strategy_payoff, Strategy.payoff(leg))

        return strategy_payoff

print(Strategy.payoff(1,100,1)[:,1])