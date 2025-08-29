import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

import time
from functools import reduce

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
options = Options()

user_agent = os.environ.get("USER_AGENT")
options.add_argument("user-agent=" + user_agent)

options.binary_location = os.environ.get("CHROME_DRIVER_PATH")

google_url = "https://www.google.com"

team = "bayer04"
team_code = {"spurs": "361ca564", "bayer04": "c7a9f859"}
season = "2023-2024"
competition = {
    "all": "all_comps",
    "bundesliga": "c20",
    "europa-league": "c19",
    "DFB-Pokal": "c521",
}
category = ["", "shooting", "passing", "passing_types", "defense", "possession", "misc"]

service = Service()
browser = webdriver.Chrome(service=service, options=options)

dataframes = []

for i in range(7):
    print(f"-----------------------------{category[i]}-------------------------------")
    fbref_Leverkusen_url = f"https://fbref.com/en/squads/{team_code[team]}/{season}/matchlogs/{competition["all"]}/{category[i]}/"
    browser.get(fbref_Leverkusen_url)
    time.sleep(3)

    # Accessing table
    table = browser.find_element(By.ID, "matchlogs_for")

    thead = table.find_element(By.TAG_NAME, "thead")
    header_rows = thead.find_elements(By.TAG_NAME, "tr")

    main_header_row = header_rows[-1]
    header_cells = main_header_row.find_elements(By.CLASS_NAME, "poptip")
    columns = [
        cell.get_attribute("data-stat") for cell in header_cells if cell.text.strip()
    ]

    tbody = table.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    # storing data
    data = []
    for j, row in enumerate(rows):
        date = row.find_element(By.TAG_NAME, "th").text.strip()
        if date == "date":
            continue

        cells = row.find_elements(By.TAG_NAME, "td")
        row_data = [date] + [cell.text.strip() for cell in cells]

        if row_data and any(cell for cell in row_data):
            data.append(row_data)
            # print(row_data)

    df = pd.DataFrame(data, columns=columns)
    dataframes.append(df)
    print(df.head())

# merging data
merged_df = reduce(
    lambda left, right: pd.merge(
        left, right, on="date", how="outer", suffixes=("", "_dup")
    ),
    dataframes,
)
# remove duplicates
merged_df = merged_df.loc[:, ~merged_df.columns.str.endswith("_dup")]

print(merged_df.head())

csv_path = f"data/{team}_{season.replace('-', '_')}_matchlog.csv"
merged_df.to_csv(csv_path, index=False)
print("Success!")

time.sleep(300)
browser.quit()
