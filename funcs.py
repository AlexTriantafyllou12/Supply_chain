import pandas as pd
from datetime import datetime


def generate_demand(
        start_date = "2023-08-01",
        time_periods = 90
):
    
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    demand = pd.DataFrame()
    demand["date"] = pd.date_range(start_date, periods=time_periods, freq='D')

    return demand

generate_demand()