import datetime
import requests
import os
from .session import session as saved_session

def fetch_input(day, session=None, year=None):

    if year is None:
        year = datetime.datetime.now().year

    if session is None:
        session = saved_session

    url = f"https://adventofcode.com/{year}/day/{day}/input"

    response = requests.get(url, cookies={'session': session})
    return response

def save_input(path, contents):
    output = open(path, 'w')
    output.write(contents)
    output.close()
    
def load_input(day, session=None, year=None, force_reload=False):
    response = fetch_input(day, session, year)
    output_path = f"day{day}/input"

    if not os.path.exists(output_path) or force_reload:
        response = fetch_input(day, session, year)
        contents = response.text
        output = save_input(output_path, contents)
    else:
        input_file = open(output_path)
        contents = input_file.read()

    return contents


def get_adjacents(pt):
    return (
        (pt[0]+1, pt[1]),
        (pt[0]-1, pt[1]),
        (pt[0], pt[1]+1),
        (pt[0], pt[1]-1)
    )


def vector_add(pt1, pt2):
    return (pt1[0] + pt2[0], pt1[1] + pt2[1])


def vector_sub(pt1, pt2):
    return (pt1[0] - pt2[0], pt1[1] - pt2[1])
