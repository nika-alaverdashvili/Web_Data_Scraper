import requests
from bs4 import BeautifulSoup
import sqlite3


class DataScraper:
    base_url = "https://www.scrapethissite.com/pages/forms"
    database_file = "scraped_data.db"

    def __init__(self):
        self._connection = None

    def connect(self):
        self._connection = sqlite3.connect(self.database_file)

    def disconnect(self):
        self._connection.close()

    def commit(self):
        self._connection.commit()

    def create_table(self):
        try:
            self._connection.execute('''
                CREATE TABLE IF NOT EXISTS team_data (
                    club_name TEXT,
                    year INTEGER NOT NULL,
                    wins INTEGER,
                    losses INTEGER,
                    goals_for INTEGER,
                    goals_against INTEGER
                )''')
            self._connection.commit()
        except sqlite3.Error as e:
            print("Error creating table:", e)

    def scrape_website(self):
        page = 1
        while True:
            url = f'{self.base_url}/?page_num={page}&per_page=25'
            response = requests.get(url)
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract data from the current page
            team_trs = soup.find_all("tr", attrs={"class": "team"})
            if not team_trs:
                break  # No more pages to scrape

            self.process_rows(team_trs)
            page += 1

        self.commit()

    def process_rows(self, rows):
        cursor = self._connection.cursor()
        for row in rows:
            club_name = row.find("td", attrs={"class": "name"}).get_text(strip=True)
            year = int(row.find("td", attrs={"class": "year"}).get_text(strip=True))
            wins = int(row.find("td", attrs={"class": "wins"}).get_text(strip=True))
            losses = int(row.find("td", attrs={"class": "losses"}).get_text(strip=True))
            goals_for = int(row.find("td", attrs={"class": "gf"}).get_text(strip=True))
            goals_against = int(row.find("td", attrs={"class": "ga"}).get_text(strip=True))

            # Insert the data into the table
            try:
                cursor.execute(
                    "INSERT INTO team_data (club_name, year, wins, losses, goals_for, goals_against) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (club_name, year, wins, losses, goals_for, goals_against)
                )
            except sqlite3.Error as e:
                print("Error inserting data into the table:", e)

    def max_wins_between_1990_2004(self):
        cursor = self._connection.cursor()
        cursor.execute('''
                SELECT club_name, year, MAX(wins), losses, goals_for
                FROM team_data
                WHERE year BETWEEN 1990 AND 2004;''')
        return cursor.fetchall()

    def get_the_most_scored_goals_year(self, year):
        cursor = self._connection.cursor()
        cursor.execute('''
                SELECT SUM(goals_for)
                FROM team_data
                WHERE year = ?''', (year,))
        return cursor.fetchall()

    def max_losses_greater_than_1990(self):
        cursor = self._connection.cursor()
        cursor.execute('''
                SELECT club_name, year, wins, MAX(losses), goals_for, goals_against
                FROM team_data
                WHERE year >= 1990;''')
        return cursor.fetchall()

    def main(self):
        self.connect()
        self.create_table()
        self.scrape_website()

        max_wins_data = self.max_wins_between_1990_2004()
        print("Max wins between 1990 and 2004:")
        for row in max_wins_data:
            print(row)
        print(50 * "*")

        most_scored_goals_2002 = self.get_the_most_scored_goals_year(2002)
        print("Most scored goals in 2002:")
        print(most_scored_goals_2002)
        print(50 * "*")

        max_losses_data = self.max_losses_greater_than_1990()
        print("Max losses after 1990:")
        for row in max_losses_data:
            print(row)

        self.disconnect()

        print(50 * "*")
        print("Scraping and data insertion completed.")


if __name__ == '__main__':
    data_scraper = DataScraper()
    data_scraper.main()
