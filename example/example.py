from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.plotting import figure
from bokeh.models import TextInput, ColumnDataSource, Slider, TextAreaInput
import yfinance as yf
import pandas as pd
from option_sim.model.utils import get_price, change_float
from option_sim.strategy.strategies import Strategy
import pandas as pd
from option_sim.model.kde import generate_path


import numpy as np

df = get_price('ggal','1y','1d').reset_index()
source = ColumnDataSource(df)

path = generate_path(df, 60)
source_path = ColumnDataSource(path)

stg = Strategy((100,10,1,'c'))
stg_payoff = stg.strategy_payoff()
print()
source_payoff = ColumnDataSource(data={
                                  'x_values' : stg_payoff[:,1],
                                  'y_values': stg_payoff[:,0]
                                  })

# Ticker input
text_ticker = TextInput(title= 'Ticker', value='ggal')

def ticker_update(attr, old, new):
    df= get_price(new,'1y','1d').reset_index()
    global path
    path = generate_path(df, 40)
    source.data = df
    source_path.data = path

text_ticker.on_change('value', ticker_update)

#Stock chart

stock_chart = figure(width = 900,
                     height = 500,
                     x_axis_type="datetime",
                     )

stock_chart.line(x= 'Date', y = 'Close', source=source)

# Slider
slider = Slider(start = 0, end=len(path), value=0, step=1, title = 'DTE days to expiration')
def path_update(attr, old, new):
    path_copy = path.copy()
    sliced_path = path_copy[:len(path)-new]
    source_path.data = sliced_path

slider.on_change('value', path_update)

stock_chart.line(x= 'index',
                 y = 'Close',
                 source=source_path,
                 color= 'red')

# Strategy Area input
strategy_input = TextAreaInput(title = 'Strategy')
def strategy_update(attr, old, new):
    
    data_input = [tuple(x.split(',')) for x in new.split('\n')]
    data_formated = tuple([[change_float(x) for x in y] for y in data_input])

    stg = Strategy(*data_formated)
    stg_payoff = stg.strategy_payoff()
    source_payoff.data = {'x_values': stg_payoff[:,1],
                            'y_values': stg_payoff[:,0]}

strategy_input.on_change('value',strategy_update)


option_chart = figure(width= 300,
                      height = 500,
                      y_range=stock_chart.y_range,
                      )

option_chart.line(x='x_values', y='y_values', source=source_payoff)



l = layout([
         [text_ticker],
        [stock_chart, option_chart],
        [slider,strategy_input]
        ])


curdoc().add_root(l)


# stg = Strategy((200, 220, 3.35, 'c'),(-300, 230, 2.13, 'c'))
# poff = stg.strategy_payoff()

# # dte = (5,10,20,30)
# # stg.plot_strategy(0.5,0.4,dte)

# greek = stg.greeks(193.1,55/365,.28,.4)
# df = pd.DataFrame.from_dict(greek)
# print(df)

# df = get_price('ggal','1y','1d')
# path = generate_path(df,30)


