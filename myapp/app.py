# %%writefile app.py

from pathlib import Path
import numpy as np
import pandas as pd
from shiny import App, render, ui, reactive
import plotly.graph_objs as go
from shinywidgets import output_widget, render_widget, register_widget, reactive_read


app_ui = ui.page_fluid(
    ui.input_slider("choose", "Data", 1, 65, 1),
    output_widget("spiralPlot")
)


def server(input, output, session):

    infile = Path(__file__).parent / "wdv_2023_wjhl10y.csv"
    wdv_2023_wjhl10y = pd.read_csv(infile)
    types=wdv_2023_wjhl10y.columns

    @reactive.Effect
    def _():
        choose = input.choose()

        t_data = pd.DataFrame(np.c_[wdv_2023_wjhl10y["data_year"],wdv_2023_wjhl10y.index,wdv_2023_wjhl10y.iloc[:,choose],np.arange(1,12)])
        t_data.columns = ["year", "year_id", "t_diff", "year_number"]
        t_data = t_data.ffill(axis = 0)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        t_data = pd.DataFrame(np.c_[np.repeat(t_data["year"],12), np.tile(months,11), np.repeat(t_data["t_diff"],12)])
        t_data.columns = ["year", "month", "t_diff"]
        t_data = t_data.ffill(axis = 0)
        t_data['month_number'] = np.tile(np.arange(1,12),12)
        t_data['year'] = t_data['year'].astype(float)
        t_data['year'] = t_data['year'].astype(int)
        t_data['month_number'] = t_data['month_number'].astype(int)
        t_data['t_diff'] = t_data['t_diff'].astype(float)
        t_data['radius'] = t_data['t_diff'].values + 1.5
        t_data['theta'] = 2 * np.pi * (t_data['month_number']-1)/12
        t_data['x'] = t_data['radius'] * np.sin(t_data['theta'])
        t_data['y'] = t_data['radius'] * np.cos(t_data['theta'])
        t_data['z'] = t_data['year']
        #t_data['label'] = t_data["month"] + " " + t_data["year"].astype(str) + " : " + t_data["t_diff"].astype(str)
        t_data['label'] = t_data["year"].astype(str) + " : " + t_data["t_diff"].astype(str)

        spiralPlot = go.FigureWidget(
            data=[
                go.Scatter3d(
                    x = t_data.x, 
                    y = t_data.y, 
                    z = t_data.z,
                    connectgaps = True,
                    showlegend = False,
                    text = t_data.label,
                    hoverinfo = "text",
                    mode = 'lines',
                            )
            ],
        )
        spiralPlot.update_layout(scene = dict(xaxis = dict(backgroundcolor="rgb(200, 200, 230)",
                                                           gridcolor="white",
                                                           showbackground=False,
                                                           zerolinecolor="white",
                                                           showticklabels=False,
                                                           title='',
                                                           ),
                                              yaxis = dict(backgroundcolor="rgb(230, 200,230)",
                                                           gridcolor="white",
                                                           showbackground=False,
                                                           zerolinecolor="white",
                                                           showticklabels=False,
                                                           title='',
                                                           ),
                                              zaxis = dict(backgroundcolor="rgb(230, 230,200)",
                                                           gridcolor="white",
                                                           showbackground=False,
                                                           zerolinecolor="white",
                                                           showticklabels=True,
                                                           title='',
                                                           ),
                                               ),
                                 )

        register_widget("spiralPlot", spiralPlot)


app = App(app_ui, server)