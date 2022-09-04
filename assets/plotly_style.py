
import os
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.io as pio
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

def plotly_styles_setup():
    pio.templates["plotly_template"] = go.layout.Template(
        layout=go.Layout(
            colorway=['#5577AA', '#E6642F', '#EFB250', '#D8E2EF', '#AAC8F2'],
            height=500,
            width=1000,
            plot_bgcolor= '#FFFFFF',
            paper_bgcolor= '#FFFFFF',
            font_color= '#000000',
            title_font_color= '#000000'
        )
    )
    pio.templates.default = "plotly_template"
