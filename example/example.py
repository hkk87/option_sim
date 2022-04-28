from bokeh.io import curdoc
from bokeh.layouts import column, layout
from bokeh.plotting import figure
from bokeh.models import TextInput, ColumnDataSource, Slider, TextAreaInput, CheckboxGroup,BoxSelectTool
from option_sim.model.utils import get_price, change_float
from option_sim.strategy.strategies import Strategy
import pandas as pd
from option_sim.model.kde import generate_path_date
from datetime import timedelta, datetime
import numpy as np

df = get_price('spy','1y','1d').reset_index()
source = ColumnDataSource(df)

expiration_date = datetime.today() + timedelta(days=59)
path = generate_path_date(df, expiration_date)
source_path = ColumnDataSource(data=dict())

stg = Strategy((100,10,1,'c'))
stg_payoff = stg.strategy_payoff()
source_payoff = ColumnDataSource(data=dict())




# Ticker input
text_ticker = TextInput(title= 'Ticker', value='SPY')

def ticker_update(attr, old, new):
    global df
    df= get_price(new,'1y','1d').reset_index()
    global path
    path = generate_path_date(df, expiration_date)
    source.data = df
    # source_path.data = path


text_ticker.on_change('value', ticker_update)

checkbox = CheckboxGroup(labels=['Simulated Path'], active=[0], margin=(30,5,5,5))
def checkbox_update(attr, old, new):
    if new == [0]:
        stock_chart.select(name='path').visible = True
    else:
        stock_chart.select(name='path').visible = False

checkbox.on_change('active',checkbox_update)

#Stock chart
stock_chart = figure(width = 900,
                     height = 500,
                     x_axis_type="datetime",
                     title= 'Chart'
                     )

stock_chart.line(x= 'Date', y = 'Close', source=source)


# Slider
slider = Slider(start = -len(path), end=0, value=-len(path), step=1, title = 'DTE days to expiration')
def path_update(attr, old, new):
    source_path.data = path[:len(path)+new]

slider.on_change('value', path_update)

stock_chart.line(x= 'index',
                 y = 'Close',
                 source=source_path,
                 color= 'red',
                 name= 'path')


# Expiration date
expiration = TextInput(title= 'Expiration date (YYYY/MM/DD)', value= expiration_date.strftime("%Y/%m/%d"))

def expdate_update(attr, old, new):
    input_date = datetime.strptime(new, "%Y/%m/%d")
    global expiration_date
    expiration_date = input_date
    global path
    path = generate_path_date(df, expiration_date)
    source_path.data = path
    slider.update(start=-len(path), value=-len(path))
    # stock_chart.add_layout(Span(
    #                         location = expiration_date,
    #                         dimension = 'height',
    #                         line_color = 'green',
    #                         line_width = 1.3,
    #                         line_dash = 'dashed'
    #                         ))

expiration.on_change('value', expdate_update)

# Strategy Area input
strategy_input = TextAreaInput(title = 'Strategy')

def strategy_update(attr, old, new):
    
    data_input = [tuple(x.split(',')) for x in new.split('\n')]
    data_formatted = tuple([[change_float(x) for x in y] for y in data_input])

    stg = Strategy(*data_formatted)
    stg_payoff = stg.strategy_payoff()
    source_payoff.data = {'x_values': stg_payoff[:,1],
                            'y_values': stg_payoff[:,0]}

strategy_input.on_change('value',strategy_update)

option_chart = figure(width= 300,
                      height = 500,
                      y_range=stock_chart.y_range,
                      title= 'Strategy Payoff'
                      )
option_chart.line(x='x_values', y='y_values', source=source_payoff)

# PreText

# pretxt = DataTable(text ='Greeks')

col = column(slider, expiration)

l = layout([
         [text_ticker,checkbox],
        [stock_chart, option_chart],
        [col,strategy_input]
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


