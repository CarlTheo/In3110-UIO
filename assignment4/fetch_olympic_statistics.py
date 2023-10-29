"""
Task 4

collecting olympic statistics from wikipedia
"""

from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup

import re

import matplotlib.pyplot as plt

import requests

# Countries to submit statistics for
scandinavian_countries = ["Norway", "Sweden", "Denmark"]

# Summer sports to submit statistics for
summer_sports = ["Sailing", "Athletics", "Handball", "Football", "Cycling", "Archery"]


def report_scandi_stats(url: str, sports_list: list[str], work_dir: str | Path) -> None:
    """
    Given the url, extract and display following statistics for the Scandinavian countries:

      -  Total number of gold medals for for summer and winter Olympics
      -  Total number of gold, silver and bronze medals in the selected summer sports from sport_list
      -  The best country in number of gold medals in each of the selected summer sports from sport_list

    Display the first two as bar charts, and the last as an md. table and save in a separate directory.

    Parameters:
        url (str) : url to the 'All-time Olympic Games medal table' wiki page
        sports_list (list[str]) : list of summer Olympic games sports to display statistics for
        work_dir (str | Path) : (absolute) path to your current working directory

    Returns:
        None
    """

    # Make a call to get_scandi_stats
    # Plot the summer/winter gold medal stats
    # Iterate through each sport and make a call to get_sport_stats
    # Plot the sport specific stats
    # Make a call to find_best_country_in_sport for each sport
    # Create and save the md table of best in each sport stats

    work_dir = Path(work_dir)
    stats_dir = work_dir / "olympic_games_results"
    stats_dir.mkdir(parents=True, exist_ok=True)

    # Get the country urls and total medal count
    country_stats = get_scandi_stats(url)

    # Plot the summer/winter gold medal stats
    plot_scandi_stats(country_stats, stats_dir)

    sport_medal_stats = {}

    # Iterate through each sport and make a call to get_sport_stats
    for sport in sports_list:
        sport_medal_stats[sport] = {}
        for country, data in country_stats.items():
            sport_medal_stats[sport][country] = get_sport_stats(data["url"], sport)

        # Plot the sport specific stats
        plot_sport_medals(sport_medal_stats[sport], sport, stats_dir)

    # Create and save the md table of best in each sport stats
    # Save results to markdown for best country in each sport by Gold medals
    with open(stats_dir / "best_of_sport_by_Gold.md", 'w') as file:
        header = "| Sport     | Best country   |\n"
        file.write("Best Scandinavian country in Summer Olympic sports, based on most number of Gold medals\n")
        file.write(header)
        file.write("|:----------|:---------------|\n")

        for sport in sports_list:
            best_country = find_best_country_in_sport(sport_medal_stats[sport])
            file.write(f"| {sport:<10} | {best_country:<15} |\n")

def get_scandi_stats(
    url: str,
) -> dict[str, dict[str, str | dict[str, int]]]:
    
    """Given the url, extract the urls for the Scandinavian countries,
       as well as number of gold medals acquired in summer and winter Olympic games
       from 'List of NOCs with medals' table.

    Parameters:
      url (str): url to the 'All-time Olympic Games medal table' wiki page

    Returns:
      country_dict: dictionary of the form:
        {
            "country": {
                "url": "https://...",
                "medals": {
                    "Summer": 0,
                    "Winter": 0,
                },
            },
        }

        with the tree keys "Norway", "Denmark", "Sweden".
    """
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", {"class": "wikitable"})
    base_url = "https://en.wikipedia.org"

    rows = table.find_all('tr')
    country_dict: dict[str, dict[str, str | dict[str, int]]] = {}

    for row in rows:
        anchors = row.find_all('a')
        country_anchor = None
        for anchor in anchors:
            if "at_the_Olympics" in anchor.get('href', ''):
                country_anchor = anchor
                break

        if not country_anchor:
            continue

        country_name = country_anchor.get_text()

        if country_name in ["Norway", "Denmark", "Sweden"]:
            country_url = base_url + country_anchor["href"]
            cols = row.find_all('td')
            summer_golds = int(cols[2].get_text().replace(',', ''))  # convert to integer after removing commas
            winter_golds = int(cols[7].get_text().replace(',', ''))

            country_dict[country_name] = {
                "url": country_url,
                "medals": {
                    "Summer": summer_golds,
                    "Winter": winter_golds
                }
            }

    return country_dict    

def get_sport_stats(country_url: str, sport: str) -> dict[str, int]:
    """Given the url to country specific performance page, get the number of gold, silver, and bronze medals
      the given country has acquired in the requested sport in summer Olympic games.

    Parameters:
        - country_url (str) : url to the country specific Olympic performance wiki page
        - sport (str) : name of the summer Olympic sport in interest. Should be used to filter rows in the table.

    Returns:
        - medals (dict[str, int]) : dictionary of number of medal acquired in the given sport by the country
                          Format:
                          {"Gold" : x, "Silver" : y, "Bronze" : z}
    """
    
    response = requests.get(country_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("span", id=re.compile("^Medals_by_summer_sport$", re.I)).find_next("table")

    medals = {
        "Gold": 0,
        "Silver": 0,
        "Bronze": 0,
    }

    rows = table.find_all('tr')

    for row in rows:
        sport_name_cell = row.find('th')  # Extract the sport name cell
        if sport_name_cell and sport in sport_name_cell.get_text():
            cols = row.find_all('td')
            medals["Gold"] = int(cols[0].get_text().strip())
            medals["Silver"] = int(cols[1].get_text().strip())
            medals["Bronze"] = int(cols[2].get_text().strip())
            break


    return medals


def find_best_country_in_sport(
    results: dict[str, dict[str, int]], medal: str = "Gold"
) -> str:
    """Given a dictionary with medal stats in a given sport for the Scandinavian countries, return the country
        that has received the most of the given `medal`.

    Parameters:
        - results (dict) : a dictionary of country specific medal results in a given sport. The format is:
                        {"Norway" : {"Gold" : 1, "Silver" : 2, "Bronze" : 3},
                         "Sweden" : {"Gold" : 1, ....},
                         "Denmark" : ...
                        }
        - medal (str) : medal type to compare for. Valid parameters: ["Gold" | "Silver" |"Bronze"]. Should be used as a key
                          to the medal dictionary.
    Returns:
        - best (str) : name of the country(ies) leading in number of gold medals in the given sport
                       If one country leads only, return its name, like for instance 'Norway'
                       If two countries lead return their names separated with '/' like 'Norway/Sweden'
                       If all or none of the countries lead, return string 'None'
    """
    valid_medals = {"Gold", "Silver", "Bronze"}
    if medal not in valid_medals:
        raise ValueError(
            f"{medal} is invalid parameter for ranking, must be in {valid_medals}"
        )

    # Get the requested medals and determine the best
    medal_counts = {country: data[medal] for country, data in results.items()}
    max_medal_count = max(medal_counts.values())
    leading_countries = [country for country, count in medal_counts.items() if count == max_medal_count]

    if len(leading_countries) == 1:
        best = leading_countries[0]
    elif len(leading_countries) == 2:
        best = f"{leading_countries[0]}/{leading_countries[1]}"
    else:
        best = "None"

    return best

# Define your own plotting functions and optional helper functions
def plot_scandi_stats(
    country_dict: dict[str, dict[str, str | dict[str, int]]],
    output_parent: str | Path | None = None
) -> None:
    """
    Plot the number of gold medals in summer and winter games for each of the scandi countries as bars.
    """
    
    # Assign color for each Scandinavian country
    color_table = {
        "Norway": "red",
        "Sweden": "blue",
        "Denmark": "green"
    }
    
    bar_width = 0.35
    countries = list(country_dict.keys())
    summer_medals = [details["medals"]["Summer"] for details in country_dict.values()]
    winter_medals = [details["medals"]["Winter"] for details in country_dict.values()]

    r1 = range(len(countries))
    r2 = [x + bar_width for x in r1]

    bars1 = plt.bar(r1, summer_medals, color=[color_table[country] for country in countries], width=bar_width, edgecolor='white', label='Summer')
    bars2 = plt.bar(r2, winter_medals, color=[color_table[country] for country in countries], width=bar_width, edgecolor='white', label='Winter', alpha=0.7)

    # Adding numbers on top of each bar
    for bar in bars1:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.3, round(yval, 2), ha='center', va='bottom')

    for bar in bars2:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.3, round(yval, 2), ha='center', va='bottom')

    plt.xlabel('Countries', fontweight='bold', fontsize=15)
    plt.xticks([r + bar_width for r in range(len(countries))], countries)
    plt.legend()

    plt.title("Gold Medals by Country and Season")
    filename = output_parent / "total_medal_ranking.png" if output_parent else "total_medal_ranking.png"
    print(f"Creating {filename}")
    plt.savefig(filename)
    plt.close()

def plot_sport_medals(data: dict[str, dict[str, int]], sport: str, output_parent: str | Path) -> None:
    """Plot medals for a given sport for the scandi countries."""
    
    colors = {
        "Gold": "yellow",
        "Silver": "silver",
        "Bronze": "saddlebrown"
    }

    # Set up the bar width and positions
    bar_width = 0.25
    r1 = range(len(data))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]

    # Extract medal counts for each country
    golds = [data[country]['Gold'] for country in scandinavian_countries]
    silvers = [data[country]['Silver'] for country in scandinavian_countries]
    bronzes = [data[country]['Bronze'] for country in scandinavian_countries]
    
    bars_gold = plt.bar(r1, golds, width=bar_width, color=colors['Gold'], edgecolor='grey', label='Gold')
    bars_silver = plt.bar(r2, silvers, width=bar_width, color=colors['Silver'], edgecolor='grey', label='Silver')
    bars_bronze = plt.bar(r3, bronzes, width=bar_width, color=colors['Bronze'], edgecolor='grey', label='Bronze')
    
    # Adding numbers on top of each bar
    for bars in [bars_gold, bars_silver, bars_bronze]:
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.3, round(yval, 2), ha='center', va='bottom')

    # Set the tick labels
    plt.xlabel('Countries', fontweight='bold')
    plt.xticks([r + bar_width for r in range(len(golds))], scandinavian_countries)
    
    plt.legend()
    plt.title(f"{sport} Medals by Scandinavian Countries")
    
    # Save the plot
    filename = output_parent / f"{sport}_medal_ranking.png"
    plt.savefig(filename)
    plt.close()

# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table"
    work_dir = Path.cwd()
    report_scandi_stats(url, summer_sports, work_dir)
