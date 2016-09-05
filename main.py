import re
import json
import glob

from bs4 import BeautifulSoup

def parse_page(name):

    webpage = open('data/{}.html'.format(name))

    soup = BeautifulSoup(webpage, 'html.parser')

    waypoints = []

    for column in soup.find_all('div',class_='col-sm-4'):

        waypoint = {}

        feature = column.find('div',class_='tux-feature')

        main_content = feature.find('div',class_='feature-title')
        waypoint['name'] = main_content.find('h3').get_text()
        waypoint['category'] = main_content.find('h4').get_text()

        photo_content = feature.find('a',class_='feature-photo')
        photo_match = re.search(r"url\('//(.[^']*)'\);",str(photo_content))

        if (photo_match):
            waypoint['photo'] = 'http://' + photo_match.group(1)

        map_content = column.find('div',class_='map-marker')
        position_match = re.search(r'data-lat="([^"]*)" data-lng="([^"]*)',str(map_content))

        if (position_match):
            waypoint['point'] = {
                'lat': float(position_match.group(1)),
                'lng': float(position_match.group(2))
            }

        waypoints.append(waypoint)

    json.dump(waypoints,open('data/{}.json'.format(name),'w'),indent=4)

    return waypoints

def find_pages():

    waypoints = []

    filepaths = glob.glob('data/*.html')

    for filepath in filepaths:

        match = re.match(r'data/([^.]*)\.html',filepath)
        name = match.group(1)

        waypoints.extend(parse_page(name))

    json.dump(waypoints,open('data/waypoints.json','w'),indent=4)

if (__name__ == "__main__"):
    find_pages()