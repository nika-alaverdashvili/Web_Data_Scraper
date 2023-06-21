
# Data Scraper

## Description

This Python code, `Main.py`, is a web scraping tool that retrieves team data from a specific website and stores it in a SQLite database.
It utilizes the requests library for making HTTP requests, the BeautifulSoup library for parsing HTML content, and the sqlite3 module for interacting with the database.
The script includes methods for connecting to the website, scraping the data, creating a database table, and performing various queries on the stored data.

## Features

- Connects to the website and retrieves team data.

- Stores the scraped data in a SQLite database.

- Creates a table (`team_data`) in the database to store the data.

- Provides methods for querying the database:

 - `max_wins_between_1990_2004`: Returns the team with the maximum wins between 1990 and 2004, along with related information.

 - `get_the_most_scored_goals_year(year)`: Returns the total goals scored in a specific year.

 - `max_losses_greater_than_1990`: Returns the team with the maximum losses after 1990, along with related information.
