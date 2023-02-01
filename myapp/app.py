
from pathlib import Path
import numpy as np
import pandas as pd
from shiny import App, render, ui, reactive
from htmltools import css
import plotly.graph_objs as go
from shinywidgets import output_widget, render_widget, register_widget, reactive_read
from shiny.types import ImgData


app_ui = ui.page_fluid(
    ui.tags.style(
    """
    .app-col-custom {
    #     border: 1px solid black;
    #     border-radius: 5px;
    #     background-color: #eee;
    #     padding: 8px;
    #     margin-top: 5px;
        margin-bottom: 50px;
    }
    """
    ),
    # ui.h2({"style": "text-align: center;"}, "WDVP 2023 - Interactive"),
    ui.row(
        ui.column(
            6,
            ui.div(
                {"class": "app-col-custom"},
                # ui.p(
                #     """
                #     """,
                #     ),
                #ui.input_slider("choose", "Select Data", 1, 65, 1),
                ui.input_select("choose", " ", {"1": "Tropical Diseases ~ global deaths",
                                                "2": "Tuberculosis ~ global cases",
                                                "3": "Tuberculosis ~ incidence",
                                                "4": "Tuberculosis ~ deaths",
                                                "5": "Malaria ~ Incidence",
                                                "6": "Malaria ~ deaths",
                                                "7": "Polio ~ Incidence",
                                                "8": "HIV / AIDS ~ Incidence (new cases)",
                                                "9": "HIV / AIDS ~ deaths per 100,000",
                                                "10": "HIV / AIDS ~ total deaths",
                                                "11": "# Countries Who've Eradicated Malaria",
                                                "12": "% Smoking",
                                                "13": "Deaths from Smoking",
                                                "14": "Dementia ~ Incidence",
                                                "15": "Health Expenditure",
                                                "16": "Infant Mortality",
                                                "17": "Maternal Mortality",
                                                "18": "Renewable Energy ~ Share of global electricity production",
                                                "19": "Renewable Energy ~ Share of global primary energy",
                                                "20": "Renewable Energy ~ Global energy-generating capacity",
                                                "21": "Wind Power ~ Share of global electricity production",
                                                "22": "Wind Power ~ Total Electricity generated from Wind",
                                                "23": "Wind Power ~ Share of global primary energy production",
                                                "24": "Solar Power ~ Share of global electricity production",
                                                "25": "Solar Power ~ Share of global primary energy",
                                                "26": "Photovoltaic Solar Power (PV) ~ Cumulative capacity",
                                                "27": "Photovoltaic Solar Power (PV) ~ Installation Cost",
                                                "28": "Renewables ~ New Investment",
                                                "29": "Nuclear Power ~ as % of global electricity production",
                                                "30": "Natural Gas ~ as % of global electricity production",
                                                "31": "Oil ~ as % of global electricity production",
                                                "32": "Coal ~ as % of global electricity production",
                                                "33": "% not in extreme poverty",
                                                "34": "% Access to Electricity",
                                                "35": "% Access to Internet",
                                                "36": "People Using At Least Basic Drinking Water",
                                                "37": "% Access to safely managed Sanitation",
                                                "38": "Life Expectancy at birth",
                                                "39": "Hunger ~ prevalence of undernourishment",
                                                "40": "Air Pollution",
                                                "41": "Road traffic death rate",
                                                "42": "Average Happy Planet Index",
                                                "43": "Human Development Index (HDI)",
                                                "44": "Global Literacy Rate",
                                                "45": "Global Female Adult Literacy Rate",
                                                "46": "Global Male Adult Literacy Rate",
                                                "47": "Gap between Male & Female Adult Literacy",
                                                "48": "% of Girls Not in Primary School",
                                                "49": "% of Boys Not in Primary School",
                                                "50": "% of Children Not in Primary School",
                                                "51": "School Enrollment",
                                                "52": "Girls Secondary School Enrollment",
                                                "53": "Expected Years of Schooling",
                                                "54": "Women's MPs ~ % of representatives",
                                                "55": "Electric Cars ~ as % of new sales",
                                                "56": "Price of Lithium Ion Battery Pack",
                                                "57": "Land covered by trees",
                                                "58": "Global living planet index (1970=100%)",
                                                "59": "Global CO2 emissions",
                                                "60": "Methane emissions",
                                                "61": "Foreign Aid",
                                                "62": "GDP per capita",
                                                "63": "GDP growth per capita",
                                                "64": "Economic Freedom",
                                                "65": "Economic Growth",
                                                }
                                                ),
                style=css(display="flex", justify_content="center", align_items="center", gap="2rem"),
                ),
            ),
    ),
    ui.row(
            ui.column(
                6,
                ui.div(
                    {"class": "app-col"},
                    ui.p(
                       """
                       """,
                       ),
                    ui.output_ui("calc"),
                    ui.output_image("gif"),
                    style=css(display="flex", justify_content="center", align_items="center", gap="2rem"),
                    ),
                    ),
            ui.column(
                6,
                ui.div(
                    {"class": "app-col"},
                    output_widget("spiralPlot"),
                    style=css(display="flex", justify_content="center", align_items="center", gap="2rem"),
                    ),
                    ),  
            ),

)


def server(input, output, session):

    infile = Path(__file__).parent / "wdv_2023_wjhl10y.csv"
    wdv_2023_wjhl10y = pd.read_csv(infile)
    infile = Path(__file__).parent / "data_descs.csv"
    types = pd.read_csv(infile)
    types= types.replace('', np.nan, regex=True)
    types = types.astype(str)

    @output
    @render.ui
    def calc():
      choose = int(input.choose())-1
      perc_diff = types["ten_yr_diff"][choose]
      return [perc_diff if perc_diff!='' and perc_diff!='nan' else ""][0]

    #@output
    #@render.image
    #def gif() -> ImgData:
    #  choose = int(input.choose())
    #  return {"src": "gifs/wdv_2023_wjhl10y_"+str(choose)+".gif", "height": "100%", "width": "75%"}
    
    @output
    @render.image
    def gif():
        from pathlib import Path
        choose = str(int(input.choose()))
        fname = "wdv_2023_wjhl10y_"+choose+".gif"
        infile = Path(__file__).parent / fname
        img: ImgData = {"src": infile, "height": "100%", "width": "75%"}
        return img

    @reactive.Effect
    def _():
        choose = int(input.choose())-1

        met = types["metric"][choose]
        met = [" ("+met+")" if met!='' and met!='nan' else ""][0]
        desc = types["type2"][choose]
        desc  = [": "+desc if desc !='' and desc!='nan' else ""][0]
        type_title = types["type1"][choose]

        t_data = pd.DataFrame(np.c_[wdv_2023_wjhl10y["data_year"],wdv_2023_wjhl10y.index,wdv_2023_wjhl10y.iloc[:,choose+1],np.arange(1,12)])
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
        t_data['label'] = t_data["year"].astype(str) + ": " + t_data["t_diff"].astype(str)
        # t_data['label'] = t_data["month"] + " " + t_data["year"].astype(str) + ": " + t_data["t_diff"].astype(str)

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
            layout={'title':type_title+desc+met},
        )
        spiralPlot.update_layout(scene = dict(xaxis = dict(backgroundcolor="rgb(0, 0, 0)",
                                                           gridcolor="white",
                                                           showbackground=False,
                                                           zerolinecolor="white",
                                                           showticklabels=True,
                                                           title='',
                                                           tickmode='auto',
                                                           nticks=4,
                                                           ),
                                              yaxis = dict(backgroundcolor="rgb(0, 0, 0)",
                                                           gridcolor="white",
                                                           showbackground=False,
                                                           zerolinecolor="white",
                                                           showticklabels=False,
                                                           title='',
                                                           tickmode='auto',
                                                           nticks=4,
                                                           ),
                                              zaxis = dict(backgroundcolor="rgb(0, 0, 0)",
                                                           gridcolor="white",
                                                           showbackground=True,
                                                           zerolinecolor="white",
                                                           showticklabels=True,
                                                           title='',
                                                           tickmode='linear',
                                                           nticks=10,
                                                           ),
                                               ),
                                 )
        spiralPlot.layout.height = 500
        spiralPlot.layout.width = 750

        register_widget("spiralPlot", spiralPlot)


app = App(app_ui, server, static_assets=Path(__file__).parent / "")
