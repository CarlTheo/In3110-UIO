"""
Task 3

Collecting anniversaries from Wikipedia
"""
from __future__ import annotations

import tabulate

from pathlib import Path

import pandas as pd

from bs4 import BeautifulSoup

import re

from urllib.parse import urljoin

import requests

# Month names to submit for, from Wikipedia:Selected anniversaries namespace
months_in_namespace = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def extract_anniversaries(html: str, month: str) -> list[str]:
    """Extract all the passages from the html which contain an anniversary, and save their plain text in a list.
        For the pages in the given namespace, all the relevant passages start with a month href
         <p>
            <b>
                <a href="/wiki/April_1" title="April 1">April 1</a>
            </b>
            :
            ...
        </p>

    Parameters:
        - html (str): The html to parse
        - month (str): The month in interest, the page name of the Wikipedia:Selected anniversaries namespace

    Returns:
        - ann_list (list[str]): A list of the highlighted anniversaries for a given month
                                The format of each element in the list is:
                                '{Month} {day}: Event 1 (maybe some parentheses); Event 2; Event 3, something, something\n'
                                {Month} can be any month in the namespace and {day} is a number 1-31
    """
    # parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Get all the paragraphs:
    paragraphs = soup.find_all('p')

    # Filter the passages to keep only the highlighted anniversaries
    ann_list = []

    for para in paragraphs:
        link = para.find('a', href = True)
        if link and link['href'].startswith(f'/wiki/{month}_'):

            stripped_text = ' '.join(para.stripped_strings)
            if stripped_text.startswith(link.get_text()):
                ann_list.append(stripped_text)

    return ann_list


def anniversary_list_to_df(ann_list: list[str]) -> pd.DataFrame:
    """Transform the list of anniversaries into a pandas dataframe.

    Parameters:
        ann_list (list[str]): A list of the highlighted anniversaries for a given month
                                The format of each element in the list is:
                                '{Month} {day}: Event 1 (maybe some parenthesis); Event 2; Event 3, something, something\n'
                                {Month} can be any month in months list and {day} is a number 1-31
    Returns:
        df (pd.Dataframe): A (dense) dataframe with columns ["Date"] and ["Event"] where each row represents a single event
    """

    # Store the split parts of the string as a table
    ann_table = []

    for ann in ann_list:
        date, _, events = ann.partition(':')
        date = date.strip()

        for event in re.split(r';(?![^()]*\))', events):
            event = event.strip()
            if event:
                ann_table.append([date, event])
        

    # Headers for the dataframe
    headers = ["Date", "Event"]
    df = pd.DataFrame(ann_table, columns=headers)

    return df


def anniversary_table(
    namespace_url: str, month_list: list[str], work_dir: str | Path
) -> None:
    """Given the namespace_url and a month_list, create a markdown table of highlighted anniversaries for all of the months in list,
        from Wikipedia:Selected anniversaries namespace

    Parameters:
        - namespace_url (str):  Full url to the "Wikipedia:Selected_anniversaries/" namespace
        - month_list (list[str]) - List of months of interest, referring to the page names of the namespace
        - work_dir (str | Path) - (Absolute) path to your working directory

    Returns:
        None
    """
    # Loop through all months in month_list
    # Extract the html from the url (use one of the already defined functions from earlier)
    # Gather all highlighted anniversaries as a list of strings
    # Split into date and event
    # Render to a df dataframe with columns "Date" and "Event"
    # Save as markdown table

    work_dir = Path(work_dir)
    output_dir = work_dir / "tables_of_anniversaries"
    output_dir.mkdir(parents=True, exist_ok=True)

    for month in month_list:
        page_url = namespace_url + month
        response = requests.get(page_url)
        html = response.text

        # Get the list of anniversaries
        ann_list = extract_anniversaries(html, month)

        # Render to a dataframe
        df = anniversary_list_to_df(ann_list)

        # Convert to an .md table
        table = tabulate.tabulate(df, headers='keys', tablefmt='pipe', showindex=False)

        # Save the output
        output_file = output_dir / f"anniversaries_{month.lower()}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(table)


if __name__ == "__main__":
    # make tables for all the months
    work_dir = Path.cwd()  # Current working directory or specify another path if needed
    namespace_url = "https://en.wikipedia.org/wiki/Wikipedia:Selected_anniversaries/"
    months_in_namespace = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    anniversary_table(namespace_url, months_in_namespace, work_dir)

    