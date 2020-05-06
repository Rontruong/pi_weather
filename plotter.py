# https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#custom-tooltip
# https://stackoverflow.com/questions/28694025/converting-a-datetime-column-back-to-a-string-columns-pandas-python
# https://discourse.bokeh.org/t/hovertool-displaying-image/1198/6
# https://github.com/jni/blob-explorer/blob/master/picker.py#L119
# https://stackoverflow.com/questions/52921711/embedding-local-images-with-relative-paths-using-hovertool-in-bokeh
# https://stackoverflow.com/questions/39672499/bokeh-displaying-images-with-hovertool

import numpy as np
import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from bokeh.io import curdoc
from bokeh.layouts import column, layout
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput,HoverTool
from bokeh.plotting import figure
from dateutil.parser import parse

with psycopg2.connect(dbname='') as conn:
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    with conn.cursor() as cur:
        sql = 'SELECT * from periodic'
        data = pd.read_sql_query(sql, conn)

def c_to_f(val):
    return val * 9 / 5 + 32

data['temp_humidity_f'] = c_to_f(data.temp_humidity_c)
data['temp_pressure_f'] = c_to_f(data.temp_pressure_c)
data['cpu_temp_f'] = c_to_f(data.cpu_temp_c)
# https://github.com/jni/blob-explorer/blob/master/picker.py#L119
# data['imgs'] = ['https://scontent-sjc3-1.xx.fbcdn.net/v/t1.15752-9/90003999_234628344248646_2024713382233374720_n.jpg?_nc_cat=102&_nc_sid=b96e70&_nc_ohc=ljmXIRaXFS0AX_pX5XA&_nc_ht=scontent-sjc3-1.xx&oh=acf8c16a04c97a50a83faae8baa5d5f1&oe=5ECF10F0'] * len(data)
# Create Column Data Source that will be used by the plot
# data['imgs'] = ['https://scontent-sjc3-1.xx.fbcdn.net/v/t1.15752-9/78148969_744783592704971_5265587135611666432_n.jpg?_nc_cat=105&_nc_sid=b96e70&_nc_ohc=M78zakQgGRQAX94xGaF&_nc_ht=scontent-sjc3-1.xx&oh=c5e7861d39e77550e30af51d3656991f&oe=5ED066B6'] * len(data)

source = ColumnDataSource(data)

# https://stackoverflow.com/questions/51496142/formatting-pandas-datetime-in-bokeh-hovertool
hover = HoverTool(
        tooltips=[
            ("timestamp", "@timestamp{%Y-%m-%d %H:%M:%S}"),
        ],
        formatters={'@timestamp': 'datetime'}
    )

# https://docs.bokeh.org/en/latest/docs/user_guide/tools.html#custom-tooltip
# TOOLTIPS = """
#     <div>
#         <img
#             src="@imgs" height="661" alt="@imgs" width="300"
#             style="float: top; margin: 0px 50px 50px 0px;"
#             border="2"
#         ></img>
#     </div>
# """

TOOLTIPS = None

p1 = figure(plot_height=600, title="Temperature", sizing_mode="stretch_width", x_axis_type="datetime", tooltips=TOOLTIPS)
p1.xaxis.axis_label = 'Timestamp'
p1.yaxis.axis_label = 'Temp [C]'
p1.circle(x='timestamp', y='temp_humidity_c', source=source, legend_label='temp from humidty sensor', color='green')
p1.circle(x='timestamp', y="temp_pressure_c", source=source, legend_label='temp from pressure sensor', color='blue')
p1.circle(x='timestamp', y="cpu_temp_c", source=source, legend_label='cpu temp', color='red')
p1.legend.click_policy = "hide"

p5 = figure(plot_height=600, title="Temperature", sizing_mode="stretch_width", x_axis_type="datetime", tooltips=TOOLTIPS)
p5.xaxis.axis_label = 'Timestamp'
p5.yaxis.axis_label = 'Temp [F'
p5.circle(x='timestamp', y='temp_humidity_f', source=source, legend_label='temp from humidty sensor', color='green')
p5.circle(x='timestamp', y="temp_pressure_f", source=source, legend_label='temp from pressure sensor', color='blue')
p5.circle(x='timestamp', y="cpu_temp_f", source=source, legend_label='cpu temp', color='red')
p5.legend.click_policy="hide"

p2 = figure(x_range=p1.x_range, plot_height=600, title="Humidity", sizing_mode="stretch_width", x_axis_type="datetime", tooltips=TOOLTIPS)
p2.xaxis.axis_label = 'Timestamp'
p2.yaxis.axis_label = 'Relative Humidity [%]'
p2.circle(x='timestamp', y="humidty_rh", source=source, legend_label='humidity')

p3 = figure(x_range=p1.x_range, plot_height=600, plot_width=700, title="CPU Load", sizing_mode="stretch_width", x_axis_type="datetime", tooltips=TOOLTIPS)
p3.xaxis.axis_label = 'Timestamp'
p3.yaxis.axis_label = 'CPU Load [%]'
p3.circle(x='timestamp', y="load_avg_percent", source=source, legend_label='cpu load')

p4 = figure(x_range=p1.x_range, plot_height=600, plot_width=700, title="Ping", sizing_mode="stretch_width", x_axis_type="datetime", tooltips=TOOLTIPS)
p4.xaxis.axis_label = 'Timestamp'
p4.yaxis.axis_label = 'Ping [ms]'
p4.circle(x='timestamp', y="avg_ping_google_ms", source=source, legend_label='avg ping', color='green')
p4.circle(x='timestamp', y="min_ping_google_ms", source=source, legend_label='min ping', color='blue')
p4.circle(x='timestamp', y="max_ping_google_ms", source=source, legend_label='max ping', color='red')
p4.legend.click_policy="hide"

p1.add_tools(hover)
p2.add_tools(hover)
p3.add_tools(hover)
p4.add_tools(hover)
p5.add_tools(hover)


final = column(p5, p1, p2, p3, p4)
final.sizing_mode = 'stretch_width'
curdoc().add_root(final)
