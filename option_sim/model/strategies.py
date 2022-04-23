import numpy as np
from option_sim.model.bs import bs_opt, delta, gamma, vega, theta, rho
import matplotlib.pyplot as plt

class Strategy: 
    """ """
    def __init__(self, *legs):
        if np.shape(legs) == (4,): 
            self.legs_tuple = legs # tuple with a string 
            self.legs_array = np.array(legs[:-1]) # only int from legs
            self.qty_array = np.array(legs[1])
            self.derivative_price_array = np.array(legs[2])

        else: 
            self.legs_tuple = legs
            self.legs_array = np.array(legs)[:,:-1].astype(float)
            self.qty_array = self.legs_array[:,0]
            self.derivative_price_array = self.legs_array[:,2]
            self.initial_investment = self.derivative_price_array * self.qty_array
            self.total_initial_investment = np.sum( self.derivative_price_array * self.qty_array)

    
    def payoff(self):
        qty, strike, derivative_price, option_type = self.legs_tuple

        if option_type == 'c': cp = 1
        else: cp = -1

        underlying_price_range = np.linspace(strike * 0.8, strike * 1.2, 41)
        payoff = np.maximum(
                            cp * (underlying_price_range - cp * derivative_price - strike), 
                            - np.ones_like(underlying_price_range) * derivative_price 
                            )
        return np.stack((underlying_price_range, payoff * qty), axis=1)
            


    def strategy_payoff(self):
        if np.shape(self.legs_tuple) != (4,):
            mean_strike = np.mean(self.legs_array, axis=0)[1]

        else: 
            qty, strike, derivative_price, option_type = self.legs_tuple
           
            return self.payoff()

        underlying_strategy_price_range = np.linspace(mean_strike * 0.8, mean_strike * 1.2, 41)
        strategy_payoff = np.zeros(41)

        for leg in self.legs_tuple:
            qty, strike, derivative_price, option_type = leg
            if option_type == 'c': cp = 1
            else: cp = -1

            single_payoff = np.maximum(
                    cp * (underlying_strategy_price_range - cp * derivative_price - strike), 
                    - np.ones_like(underlying_strategy_price_range) * derivative_price 
                    )

            strategy_payoff = np.add(strategy_payoff, single_payoff * qty)

        return np.stack((underlying_strategy_price_range, strategy_payoff), axis=1)

    @staticmethod
    def _map_bs_formula(x):
        return np.array([bs_opt(*xi) for xi in x])

    

    def derivatives_evolution(self, DTE, vol, rf):
        underlying_strategy_price_range = self.strategy_payoff()[:,0]
        derivative_price_evolution_list = []
        for leg in self.legs_tuple:
            qty = leg[0]
            strike = leg[1]
            if leg[-1] == 'c': cp = 1
            else: cp = -1

            bs_input_matrix = np.stack(
                                        (underlying_strategy_price_range,
                                        np.ones_like(underlying_strategy_price_range) * strike,
                                        np.ones_like(underlying_strategy_price_range) * DTE / 365,
                                        np.ones_like(underlying_strategy_price_range) * vol,
                                        np.ones_like(underlying_strategy_price_range) * rf,
                                        np.ones_like(underlying_strategy_price_range) * cp
                                        ),
                                        axis=1
                                        
                                        )              
            derivative_price_evolution_list.append( np.array([bs_opt(*xi) for xi in bs_input_matrix]))
        
        derivative_price_evolution_array = np.stack(derivative_price_evolution_list, axis = 1)

        return underlying_strategy_price_range, derivative_price_evolution_array

    def strategy_evolution(self, DTE, vol, rf, output_total= True):

        price_range, derivative_price_evolution_array = self.derivatives_evolution(DTE, vol, rf)
        investment_evolution = derivative_price_evolution_array * self.qty_array - self.initial_investment
        
        if output_total == True: investment_evolution = np.sum(investment_evolution, axis = 1)
        
        return np.stack((price_range, investment_evolution), axis=1)

    def plot_strategy(self,vol,rf, *DTE):
        price_range, payoff = self.strategy_payoff().T
        fig, ax = plt.subplots(1,1)

        ax.plot(
            price_range,
            payoff,
            label = 'Strategy Payoff'
        )

        if DTE:
            for dte in DTE[0]:
                price_range, market_price = self.strategy_evolution(dte, vol, rf).T
                ax.plot(
                        price_range,
                        market_price,
                        label = f'Days to expiration {dte}'
                        )

        plt.legend()
        plt.show()

    def greeks(self, spot_price, dte, volatlity, rf):
        greeks_dict = {}
        if np.shape(self.legs_tuple) == (4,):
            qty, strike, derivative_price, option_type = self.legs_tuple

            if option_type == 'c': cp = 1
            else: cp = -1

            greeks_dict[self.legs_tuple] = {
                                            'delta' : delta(spot_price, strike, dte, volatlity, rf, cp) * qty,
                                            'gamma' : gamma(spot_price, strike, dte, volatlity, rf, cp) * qty,
                                            'vega' : vega(spot_price, strike, dte, volatlity, rf, cp) * qty,
                                            'theta' : theta(spot_price, strike, dte, volatlity, rf, cp) * qty,
                                            'rho' : rho(spot_price, strike, dte, volatlity, rf, cp) * qty
                                            }

        else:
            for leg in self.legs_tuple:
                qty, strike, derivative_price, option_type = leg

                if option_type == 'c': cp = 1
                else: cp = -1
                print((spot_price, strike, dte, volatlity, rf, cp))
                greeks_dict[leg] = {
                                    'delta' : delta(spot_price, strike, dte, volatlity, rf, cp) * qty,
                                    'gamma' : gamma(spot_price, strike, dte, volatlity, rf, cp) * qty,
                                    'vega' : vega(spot_price, strike, dte, volatlity, rf, cp) * qty,
                                    'theta' : theta(spot_price, strike, dte, volatlity, rf, cp) * qty,
                                    'rho' : rho(spot_price, strike, dte, volatlity, rf, cp) * qty
                                   }

            greeks_dict['Total'] = {
                                    'delta' : sum(x['delta'] for x in greeks_dict.values()),
                                    'gamma' : sum(x['gamma'] for x in greeks_dict.values()),
                                    'vega' : sum(x['vega'] for x in greeks_dict.values()),
                                    'theta' : sum(x['theta'] for x in greeks_dict.values()),
                                    'rho' : sum(x['rho'] for x in greeks_dict.values()),
                                    }                                    

        return greeks_dict