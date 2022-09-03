import dash
import datetime
from  dash.dependencies import Input, Output
from dash import dcc, html

import assets.plotly_style as ps
from main.charts.home_charts import Home_Charts


import plotly.express as px

import pandas as pd
import numpy as np
from django_plotly_dash import DjangoDash

app = DjangoDash('Example_Home')   # replaces dash.Dash
ps.plotly_styles_setup()

app.layout = html.Div(
    [
        dcc.DatePickerRange(
            id='date_input',
            min_date_allowed=datetime.datetime(2022, 1, 1),
            max_date_allowed=datetime.datetime.today(),
            initial_visible_month=datetime.datetime(2022, 8, 5),
            start_date=datetime.datetime(2022, 8, 1).date(),
            end_date=datetime.datetime(2022, 8, 25).date(),
        ),
        html.Div(id='output-date'),
        dcc.Graph(id='kpi_line_chart'),
        html.Div(id='leads', children=[
            dcc.Graph(id='lead_num_by_office_and_agent', style={"width":"50%", "display":"inline-block"}),
            dcc.Graph(id='lead_value_by_office_and_agent', style={"width":"50%", "display":"inline-block"})
        ]),
        dcc.Graph('lead_value_by_country')

    ],
    style={"margin":"auto","text-align":"center", "width":"100%"}

)


@app.callback(
    [
        Output('output-date', 'children'),
        Output('kpi_line_chart', 'figure'),
        Output('lead_num_by_office_and_agent', 'figure'),
        Output('lead_value_by_office_and_agent', 'figure'),
        Output('lead_value_by_country', 'figure')
    ],

    [
        Input('date_input', 'start_date'),
        Input('date_input', 'end_date')
    ]
)
def callback_date(start_date_input, end_date_input):
    start_date = datetime.datetime.strptime(start_date_input, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_input, "%Y-%m-%d")

    figs = []
    home_charts = Home_Charts(start_date=start_date, end_date=end_date)
    # Getting the report
    figs.append(home_charts.kpi_time_series())
    figs.append(home_charts.leads_num_sunburst())
    figs.append(home_charts.leads_value_sunburst())
    figs.append(home_charts.lead_value_by_country())
    text = "Data shown: {} - {}".format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

    return [text] + figs
