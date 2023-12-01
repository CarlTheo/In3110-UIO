#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""

import datetime
import warnings

from typing import List
import altair as alt
import pandas as pd
import requests
import requests_cache

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()

# suppress a warning with altair 4 and latest pandas
warnings.filterwarnings("ignore", ".*convert_dtype.*", FutureWarning)


# task 5.1:

def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch electricity prices for a day and location from hvakosterstrommen.no API.

    Args:
        date (datetime.date, optional): Date to fetch prices. Defaults to current date.
        location (str, optional): Location code (e.g., "NO1" for Oslo). Defaults to "NO1".

    Returns:
        pd.DataFrame: Prices DataFrame with columns - NOK_per_kWh (float), time_start (datetime).

    Note:
        Handles Daylight Saving Time adjustments.

    Example:
        >>> fetch_day_prices()  # Fetch prices for Oslo on the current date
        >>> fetch_day_prices(date=datetime.date(2023, 11, 6), location="NO3")  # Fetch prices for Trondheim on a specific date
    """
    if date is None:
        date = datetime.date.today()

    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year}/{date.strftime('%m-%d')}_{location}.json"
    r = requests.get(url)

    if r.status_code != 200:
        raise ValueError(f"Failed to fetch data. Status code: {r.status_code}")

    data = r.json()
    df = pd.DataFrame.from_dict(data)
    df['time_start'] = pd.to_datetime(df['time_start'], utc=True).dt.tz_convert("Europe/Oslo")

    return df[['NOK_per_kWh', 'time_start']]

LOCATION_CODES = {"NO1": "Oslo", "NO2": "Kristiansand", "NO3": "Trondheim", "NO4": "Tromsø", "NO5": "Bergen"}

def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations: List[str] = list(LOCATION_CODES.keys())
) -> pd.DataFrame:
    """Fetch electricity prices for multiple days and locations.

    Args:
        end_date (datetime.date, optional): End date for fetching prices. Defaults to today.
        days (int, optional): Number of days to fetch data. Defaults to 7.
        locations (List[str], optional): List of location codes. Defaults to all locations.

    Returns:
        pd.DataFrame: DataFrame with electricity prices, time intervals, location codes, and names.

    Example:
        >>> fetch_prices()  # Latest 7 days for all locations
        >>> fetch_prices(end_date=datetime.date(2023, 11, 15), days=5, locations=["NO1", "NO3"])  # Specific date range and locations
    """
    if end_date is None:
        end_date = datetime.date.today()

    df_combined = pd.concat(
        [
            pd.concat([fetch_day_prices(date=d, location=location) for d in pd.date_range(end=end_date, periods=days)])
            .assign(location_code=location, location=LOCATION_CODES[location])
            for location in locations
        ], ignore_index=True
    )

    return df_combined[['NOK_per_kWh', 'time_start', 'location_code', 'location']]

# task 5.1:

def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time.

    Args:
        df (pd.DataFrame): DataFrame containing electricity prices, time intervals, and location information.

    Returns:
        alt.Chart: Altair Chart displaying a line plot of energy prices over time for each location.
    """
    chart = alt.Chart(df).mark_line().encode(
        x='time_start:T',
        y='NOK_per_kWh:Q',
        color='location:N',
        tooltip=['time_start:T', 'NOK_per_kWh:Q']
    ).properties(
        title='Energy Prices Over Time',
        width=800,
        height=400
    )

    return chart
 
# Task 5.4

def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    raise NotImplementedError("Remove me when you implement this task (in4110 only)")
    ...


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """
    raise NotImplementedError("Remove me when you implement this optional task")

    ...


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
