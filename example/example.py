from option_sim.model import bs
from option_sim.model.strategies import Strategy
import matplotlib.pyplot as plt
import pandas as pd



stg = Strategy((200, 220, 3.35, 'c'),(-300, 230, 2.13, 'c'))
poff = stg.strategy_payoff()

# dte = (5,10,20,30)
# stg.plot_strategy(0.5,0.4,dte)

greek = stg.greeks(193.1,55/365,.28,.4)
df = pd.DataFrame.from_dict(greek)
print(df)