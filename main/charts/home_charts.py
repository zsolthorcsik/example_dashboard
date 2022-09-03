
from data_handler.handlers.google_sheets_handler import Google_Sheets_Handler
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.io as pio

class Home_Charts(object):

    start_date = None
    end_date = None

    default_colors = None
    sheets_handler = None


    def __init__(self, start_date, end_date):
        print("Home_Charts init")
        self.sheets_handler = Google_Sheets_Handler()
        self.default_colors = list(pio.templates['plotly_template'].layout.colorway)

        self.start_date = start_date
        self.end_date = end_date

    def kpi_time_series(self):
        df = self.sheets_handler.get_df_from_sheets_url('https://docs.google.com/spreadsheets/d/1tsUvF9SivvZotsA_xEmUvgxqnHJFI1M26TuRAGT45-U/')
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.loc[(df['Date']>=self.start_date)&(df['Date']<self.end_date)]
        df = df.replace('', np.nan, regex=True)
        df['Facebook Spending'] = df['Facebook Spending'].str.replace('€', '').astype(float)
        df['Google Ads Spending'] = df['Google Ads Spending'].str.replace('€', '').astype(float)
        fig = px.line(df, y=['Facebook Spending', 'Google Ads Spending'], x="Date")
        fig.update_layout({
            'title':'Examply KPIs',
            'yaxis_title':'Spending (€)',
            'legend_title':'Platform'

        })
        return fig

    def get_colors_for_df_column(self, df, key):
        c = dict(zip(df[key].unique(), self.default_colors))
        return c

    def leads_num_sunburst(self):
        df = self.sheets_handler.get_df_from_sheets_url('https://docs.google.com/spreadsheets/d/1tsUvF9SivvZotsA_xEmUvgxqnHJFI1M26TuRAGT45-U/', worksheet_name="Leads")
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
        count_df = df[['Office', 'Agent']].value_counts().reset_index(name="no_contracts")
        fig = px.sunburst(count_df, path=['Office', 'Agent'], values="no_contracts")
        fig.update_layout({
            'title':'Number of deals by office and agent'
        })
        return fig

    def leads_value_sunburst(self):
        df = self.sheets_handler.get_df_from_sheets_url('https://docs.google.com/spreadsheets/d/1tsUvF9SivvZotsA_xEmUvgxqnHJFI1M26TuRAGT45-U/', worksheet_name="Leads")
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
        df["Lead Value"] = df["Lead Value"].str.replace('€', '').str.replace(',', '').astype(float)
        c = self.get_colors_for_df_column(df, "Office")
        df["c"] = df.apply(lambda r: c[r["Office"]], axis=1)
        fig = px.sunburst(df, path=["Office", "Agent", "Product"], values="Lead Value", color="c")
        fig.update_layout({
            'title':'Deal value by office and agent'
        })
        return fig

    def lead_value_by_country(self):
        df = self.sheets_handler.get_df_from_sheets_url('https://docs.google.com/spreadsheets/d/1tsUvF9SivvZotsA_xEmUvgxqnHJFI1M26TuRAGT45-U/', worksheet_name="Leads")
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
        df["Lead Value"] = df["Lead Value"].str.replace('€', '').str.replace(',', '').astype(float)
        sum_df = df.groupby("Country")[["Country", "Lead Value"]].sum().reset_index()
        fig = px.choropleth(sum_df, locations="Country", locationmode="country names", color="Lead Value", color_continuous_scale=[(0, self.default_colors[1]), (1, self.default_colors[2])])
        fig.update_layout({
            "title":"Lead Value by Countries"
        })
        return fig
