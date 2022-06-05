# wget -O sp500_$(date "+%Y%m%d").html https://www.slickcharts.com/sp500

from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
from urllib.request import Request, urlopen

today = date.today()
today_string = "%d%02d%02d"%(today.year, today.month, today.day)

req = Request("https://www.slickcharts.com/sp500", headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(urlopen(req).read(), features="lxml")
items = soup.find_all('tr')

companies = pd.DataFrame(
    columns=["rank","name","ticker","weight","price","change","change_percentage", "date"]
)

for item in items:
    scoop = BeautifulSoup(str(item), features="lxml")
    cols = scoop.find_all('td')
    if len(cols) == 7:
        rank = int(cols[0].text.strip())
        name = str(cols[1].text.strip())
        ticker = str(cols[2].text.strip())
        weight = float(cols[3].text.strip())
        price = float(cols[4].text.strip().replace(',', ''))
        change = float(cols[5].text.strip())
        change_percentage = float(cols[6].text.lstrip('(').rstrip('%)'))  # percentage
        company = pd.DataFrame(
            [[rank, name, ticker, weight, price, change, change_percentage, today_string]], 
            columns=["rank","name","ticker","weight","price","change","change_percentage", "date"]
        )
        companies = pd.concat([companies, company], ignore_index=True)

companies.to_csv("sp500_data.csv", mode='a')