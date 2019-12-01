import datetime
import requests

def fetch_input(day, session, year=None):

    if year is None:
        year = datetime.datetime.now().year

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    print(url)

    response = requests.get(url, cookies={'session': session})
    return response

def save_input(day, session, year=None):
    response = fetch_input(day, session, year)
    output = open(f"day{day}/input", 'w')
    output.write(response.text)
    output.close()
    
