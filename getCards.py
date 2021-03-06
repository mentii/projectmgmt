import sys
import requests
import ConfigParser
import csv
import re

projectsURL =  'https://api.github.com/repos/mentii/mentii/projects'

configFile = sys.argv[1]
config = ConfigParser.ConfigParser()
config.read(configFile)
username = config.get('login', 'username')
password = config.get('login', 'password')

s = requests.Session()
s.auth = (username, password)
s.headers.update({'Accept': 'application/vnd.github.inertia-preview+json'})
response = s.get(projectsURL)
projects = response.json()

with open('stories.csv', 'wt') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow( ('#', 'Name', 'Points') )

    for p in projects:
        print p['name']
        columnsURL =  p['columns_url']
        response = s.get(columnsURL)
        columns = response.json()

        columnPoints = {}

        for col in columns:
            colName = col['name']
            print '\t', colName
            writer.writerow('')
            writer.writerow([colName])

            cardURL =  col['cards_url']
            response = s.get(cardURL)
            cards = response.json()
            colPoints = 0

            for card in cards:
                note = card['note']
                number = ''
                if not note:
                    contentURL = card['content_url']
                    response = s.get(contentURL)
                    content = response.json()
                    note = content['title']
                    number = content['number']
                note = note.rsplit('(', 1)
                name = note[0]
                points = None
                if len(note) == 2:
                    points = note[1]
                    points = re.sub('[^0-9]', '', points)
                if points:
                    points = int(points)
                    colPoints += points
                    print '\t\t', name, points
                    writer.writerow([number, name, points])
                else:
                    print '#### NO POINTS: ####'
                    print name,
                    print '#### NO POINTS: ####'

            print '\t', 'Total', colName, 'Points:', colPoints, '\n'
            columnPoints[colName] = colPoints

        print columnPoints
