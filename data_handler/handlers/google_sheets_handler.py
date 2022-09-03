import pandas as pd
import requests

import gspread
from google.oauth2.service_account import Credentials



class Google_Sheets_Handler(object):
    def __init__(self):
        print('Google_Sheets_Handler init')

    """docstring for Sheets_Handler."""
    service_account = None

    def __init__(self):
        self.service_account = gspread.service_account(filename='access/example_dash_service_account.json')

    # Share the table with this user:
    # top3-sheets@top3-sheets.iam.gserviceaccount.com
    def get_df_from_sheets_url(self, url, worksheet_name = None):
        sh = self.service_account.open_by_url(url)
        if worksheet_name:
            wks = sh.worksheet(worksheet_name)
        else:
            wks = sh.get_worksheet(0)
        df = pd.DataFrame(wks.get_all_values())
        return df
