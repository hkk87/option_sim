from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.plotting import figure
from bokeh.models import TextInput, ColumnDataSource
import yfinance as yf
import pandas as pd
from option_sim.model.utils import get_price
from option_sim.strategy.strategies import Strategy
import pandas as pd
from option_sim.model.kde import generate_path

text_ticker = TextInput(title= 'Ticker', value='ggal')

df =  yf.Ticker('ggal').history('1y','1d').reset_index()
source = ColumnDataSource(df)



def ticker_update(attr, old, new):
    df= yf.Ticker(new).history('1y','1d').reset_index()
    source.data = df

text_ticker.on_change('value', ticker_update)

print(source.data)

stock_chart = figure(width = 900,
                     height = 500,
                     x_axis_type="datetime",
                     )

stock_chart.line(x= 'Date', y = 'Close', source=source)




stg = Strategy((100,10,1,'c'))


stg_payoff = stg.strategy_payoff()

option_chart = figure(width= 300,
                      height = 500,
                      y_range=stock_chart.y_range,
                      )



option_chart.line(x=stg_payoff[:,1] , y = stg_payoff[:,0])


l = layout([
         [text_ticker],
        [stock_chart, option_chart]
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


