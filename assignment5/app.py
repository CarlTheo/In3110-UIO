"""
strompris fastapi app entrypoint
"""
import datetime
import os
from typing import List, Optional

import altair as alt
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)

app = FastAPI()
templates = Jinja2Templates(directory= "templates")

sphinx_docs_path = r"C:\Users\ca-th\Universitet\Høst 2023\In3110\Innleveringer\RepoCopy\assignment5\documentation\_build"

app.mount("/documentation", StaticFiles(directory=sphinx_docs_path), name="documentation")

@app.get("/", response_class=HTMLResponse)
async def render_webpage(request: Request, locations: List[str] = Query([])):
    today = datetime.date.today()
    return templates.TemplateResponse(
        "strompris.html",
        {"request": request, "location_codes": LOCATION_CODES, "today": today},
    )

@app.get("/plot_prices.json")
async def get_plot_prices(
    locations: List[str] = Query([]),
    end: Optional[datetime.date] = None,
    days: int = 7,
):
    if not locations:
        locations = list(LOCATION_CODES.keys())

    data = fetch_prices(end_date=end, days=days, locations=locations)
    chart = plot_prices(data)
    chart_dict = chart.to_dict()
    return chart_dict

# Task 5.6 (bonus):
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date


...

# Task 5.6:
# `GET /plot_activity.json` should return vega-lite chart JSON (alt.Chart.to_dict())
# from `plot_activity_prices`
# with inputs:
# - location (single, default=NO1)
# - activity (str, default=shower)
# - minutes (int, default=10)


...


# mount your docs directory as static files at `/help`

...


def main():
    """Launches the application on port 5000 with uvicorn"""
    # use uvicorn to launch your application on port 5000
    ...


if __name__ == "__main__":
    main()
